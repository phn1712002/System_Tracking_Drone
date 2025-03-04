import rospy
import ast
from std_msgs.msg import Int32
from geometry_msgs.msg import Twist
import numpy as np

class CalculatorControl:
    def __init__(self):
        rospy.init_node('calculator_control_ui_node', anonymous=True)
        self.sli_vx_sub = rospy.Subscriber("/sli_vx", Int32, lambda msg: self.calculator_callback(msg, 'vx'))
        self.sli_vx_sub = rospy.Subscriber("/sli_wx", Int32, lambda msg: self.calculator_callback(msg, 'wx'))
        self.sli_vx_sub = rospy.Subscriber("/sli_wz", Int32, lambda msg: self.calculator_callback(msg, 'wz'))
        self.velocity_control_pub = rospy.Publisher("/velocity_control", Twist, queue_size = 10)
        self.velocity_control = 1
        
    def calculator_callback(self, msg, mode = 'vx'):
        value = msg.data
        dir = np.sign(value)
        
        msg_value_control = Twist()
        if mode == 'vx':  msg_value_control.linear.x = dir * self.velocity_control
        elif mode == 'wx': msg_value_control.angular.x = dir * self.velocity_control
        elif mode == 'wz': msg_value_control.angular.z = dir * self.velocity_control
        
        self.velocity_control_pub.publish(msg_value_control)
        
        
if __name__ == '__main__':
    try:
        calculator_control_ui_node = CalculatorControl()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass