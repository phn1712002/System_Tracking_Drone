

import rospy
import cv2
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class ImageViewer:
    def __init__(self):
        rospy.init_node('image_viewer_node', anonymous=True)

        self.bridge = CvBridge()

        self.image_sub = rospy.Subscriber("/image_detect", Image, self.image_callback)

    def image_callback(self, msg):
        try:
            cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")

            cv2.imshow("Camera View", cv_image)
            cv2.waitKey(1)

        except CvBridgeError as e:
            rospy.logerr(f"CvBridge Error: {e}")

if __name__ == '__main__':
    try:
        viewer = ImageViewer()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass
    finally:
        cv2.destroyAllWindows()
