

import rospy
from sensor_msgs.msg import Image
from cv_bridge import CvBridge
import cv2

def camera_publisher():
    rospy.init_node('camera_publisher_node')
    pub = rospy.Publisher('/camera/image_raw', Image, queue_size=10)
    rate = rospy.Rate(30)  # 30Hz
    cap = cv2.VideoCapture(0)
    bridge = CvBridge()

    while not rospy.is_shutdown():
        ret, frame = cap.read()
        if ret:
            msg = bridge.cv2_to_imgmsg(frame, encoding="bgr8")
            pub.publish(msg)
        rate.sleep()

    cap.release()

if __name__ == '__main__':
    try:
        camera_publisher()
    except rospy.ROSInterruptException:
        pass
