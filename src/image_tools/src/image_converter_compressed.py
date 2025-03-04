import rospy
from sensor_msgs.msg import Image, CompressedImage
import cv2
from cv_bridge import CvBridge

class ImageConverter:
    def __init__(self):
        rospy.init_node("image_converter_compressed_node", anonymous=True)
        
        # Sử dụng CvBridge để chuyển đổi giữa OpenCV và ROS Image
        self.bridge = CvBridge()
        
        # Publisher sử dụng image_transport để gửi ảnh dưới dạng CompressedImage
        self.pub = rospy.Publisher("/camera/image_compressed", CompressedImage, queue_size=10)
        
        # Subscriber nhận ảnh từ topic /image_raw
        self.sub = rospy.Subscriber("/camera/image_raw", Image, self.image_callback)

    def image_callback(self, msg):
        try:
            # Chuyển đổi từ ROS Image sang OpenCV Image
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

            # Nén ảnh thành định dạng JPEG
            _, compressed_image = cv2.imencode(".jpg", cv_image, [int(cv2.IMWRITE_JPEG_QUALITY), 90])

            # Tạo message CompressedImage
            compressed_msg = CompressedImage()
            compressed_msg.header = msg.header
            compressed_msg.format = "jpeg"
            compressed_msg.data = compressed_image.tobytes()

            # Publish ảnh đã nén
            self.pub.publish(compressed_msg)

        except Exception as e:
            rospy.logerr("Error in image conversion: %s", str(e))

if __name__ == "__main__":
    try:
        converter = ImageConverter()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
