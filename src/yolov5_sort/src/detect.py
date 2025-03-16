import rospy
import ast
from sensor_msgs.msg import Image
from geometry_msgs.msg import Point
from cv_bridge import CvBridge
from std_msgs.msg import Int32

import cv2
import torch
import numpy as np
import torch.backends.cudnn as cudnn
from yolov5_sort.models.common import DetectMultiBackend
from yolov5_sort.utils.dataloaders import LoadImages, LoadStreams
from yolov5_sort.utils.general import (check_img_size, non_max_suppression, scale_coords)
from yolov5_sort.utils.torch_utils import select_device
from yolov5_sort.sort import *

@torch.no_grad()
def detect_publisher():
    rospy.init_node('yolov5_sort_node')
    
    # Init ROS
    img_detect_pub = rospy.Publisher('/image_detect', Image, queue_size=10)
    center_bbox_tracking_pub = rospy.Publisher('/center_bbox_tracking', Point, queue_size=10)
    count_detect_pub = rospy.Publisher('/count_detect', Int32, queue_size=10)
    bridge = CvBridge()
    msg_center_center_bbox_tracking = Point()
    
    # Paramter
    weights = rospy.get_param("~weights", "best.pt")
    source = rospy.get_param("~source", "0")
    data = rospy.get_param("~data", "drone_coco128.yaml")
    device = rospy.get_param("~device", "cpu")
    classes = rospy.get_param("~classes", 0)
    agnostic_nms = rospy.get_param('~agnostic_nms', False)
    half = rospy.get_param('~half', False)
    dnn = rospy.get_param('~dnn', False)
    imgsz = ast.literal_eval(rospy.get_param('/imgsz', '[640, 640]'))  # Chuyển đổi chuỗi thành danh sách
    conf_thres = rospy.get_param('~conf_thres', 0.25)
    iou_thres = rospy.get_param('~iou_thres', 0.45)
    max_det = rospy.get_param('~max_det', 1000)
    color_bbox_tracking = ast.literal_eval(rospy.get_param('~color_bbox_tracking', '[0, 0, 255]'))
    color_bbox_untracking = ast.literal_eval(rospy.get_param('~color_bbox_untracking', '[0, 0, 0]'))
    sort_max_age = rospy.get_param('~sort_max_age', 5)
    sort_min_hits = rospy.get_param('~sort_min_hits', 2)
    sort_iou_thresh = rospy.get_param('~sort_iou_thresh', 0.2)
    flip_image = rospy.get_param('~flip_image ', 0)
    
    # ID tracking
    rospy.set_param("/id_tracking_object", -1)
    count_bbox_detect = 0
    
    
    sort_tracker = Sort(max_age=sort_max_age,
                       min_hits=sort_min_hits,
                       iou_threshold=sort_iou_thresh) 
    
    webcam = source.isnumeric() or source.endswith('.txt') or source.lower().startswith(('rtsp://', 'rtmp://', 'http://', 'https://'))

    device = select_device(device)
    half &= device.type != 'cpu'  

    device = select_device(device)
    model = DetectMultiBackend(weights, device=device, dnn=dnn, data=data)
    stride, pt, jit, onnx, engine = model.stride, model.pt, model.jit, model.onnx, model.engine
    imgsz = check_img_size(imgsz, s=stride)  

    half &= (pt or jit or onnx or engine) and device.type != 'cpu'  
    if pt or jit:
        model.model.half() if half else model.model.float()

    if webcam:
        cudnn.benchmark = True  
        dataset = LoadStreams(source, img_size=imgsz, stride=stride, auto=pt, flip_sources=bool(flip_image))
    else:
        dataset = LoadImages(source, img_size=imgsz, stride=stride, auto=pt, flip_sources=bool(flip_image))
    
    for _, im, im0s, vid_cap, _ in dataset:
        im = torch.from_numpy(im).to(device)
        im = im.half() if half else im.float()  # uint8 to fp16/32
        im /= 255  # 0 - 255 to 0.0 - 1.0
        if len(im.shape) == 3:
            im = im[None]  # Expand for batch dim

        # Inference
        pred = model(im)

        # NMS
        pred = non_max_suppression(pred, conf_thres, iou_thres, classes, agnostic_nms, max_det=max_det)

        # Per image
        for i, det in enumerate(pred):  
            if webcam:  # Batch_size >= 1
                im0 = im0s[i].copy()
            else:
                im0 = im0s.copy()
            
            if len(det):
                det[:, :4] = scale_coords(im.shape[2:], det[:, :4], im0.shape).round()
                
            dets_to_sort = np.empty((0,6)) # Pass an empty array to sort
            
            for x1, y1, x2, y2, conf, detclass in det.cpu().detach().numpy():
                dets_to_sort = np.vstack((dets_to_sort, 
                                            np.array([x1, y1, x2, y2, 
                                                    conf, detclass])))
            
            # SORT
            tracked_dets = sort_tracker.update(dets_to_sort)
                    
            if len(tracked_dets) > 0:
                bbox_xyxy = tracked_dets[:,:4]
                identities = tracked_dets[:, 8]
                
                if count_bbox_detect != len(identities):
                    count_detect_pub.publish(len(identities))
                
                for i, box in enumerate(bbox_xyxy):
                    x1, y1, x2, y2 = [int(i) for i in box]
                    id = int(identities[i]) if identities is not None else 0
                    label = str(id)
                    
                    # Send msg center box of object tracking
                    color_bbox = color_bbox_untracking
                    id_tracking_object = rospy.get_param("/id_tracking_object")
                    if id_tracking_object is not None:
                        if id == int(id_tracking_object):
                            color_bbox = color_bbox_tracking
                            msg_center_center_bbox_tracking.x = int((x1 + x2)/2)
                            msg_center_center_bbox_tracking.y = int((y1 + y2)/2)
                            center_bbox_tracking_pub.publish(msg_center_center_bbox_tracking)
                    
                    # Draw box 
                    (w, _), _ = cv2.getTextSize(label, cv2.FONT_HERSHEY_SIMPLEX, 0.6, 1)
                    cv2.rectangle(im0, (x1, y1), (x2, y2), color_bbox, 2)
                    cv2.rectangle(im0, (x1, y1 - 20), (x1 + w, y1), color_bbox, -1)
                    cv2.putText(im0, label, (x1, y1 - 5), cv2.FONT_HERSHEY_SIMPLEX, 0.6, [255, 255, 255], 1)
            
            # Send msg image    
            msg = bridge.cv2_to_imgmsg(im0, encoding="bgr8")
            img_detect_pub.publish(msg)
            
    if vid_cap:
        vid_cap.release()

if __name__ == '__main__':
    try:
        detect_publisher()
    except rospy.ROSInterruptException:
        pass