import rospy
import ast
from geometry_msgs.msg import Point, Twist

class CalculatorControl:
    def __init__(self):
        rospy.init_node('calculator_control_model_node', anonymous=True)
        self.center_bbox_tracking_sub = rospy.Subscriber("/center_bbox_tracking", Point, self.calculator_callback)
        self.velocity_control_pub = rospy.Publisher("/velocity_control", Twist, queue_size = 10)
        self.velocity_max = 1
        
    def function_calculator_velocity(self, error, velocity_max, error_max):
        error = abs(error)
        if error >= (error_max / 2):
            velocity = float(velocity_max)
        elif (error_max / 10) < error < (error_max / 2):
            # Tính toán velocity tăng tuyến tính từ 0 đến velocity_max
            velocity = ((error - (error_max / 10)) / ((error_max / 2) - (error_max / 10))) * velocity_max
        else:
            velocity = 0
        return velocity
    
    def calculator_callback(self, msg):
        x, y = msg.x , msg.y
        imgsz = ast.literal_eval(rospy.get_param('/imgsz', '[640, 640]'))  # Chuyển đổi chuỗi thành danh sách
        x_max, y_max = imgsz
        x_center, y_center = int(x_max / 2), int(y_max / 2)
        
        x_error = x_center - x
        y_error = y_center - y 
        
        if x_error > 0:
            w_x = -self.function_calculator_velocity(x_error, velocity_max = self.velocity_max , error_max=(x_max/2))
        else:
            w_x = self.function_calculator_velocity(x_error, velocity_max = self.velocity_max , error_max=(x_max/2))

        if y_error > 0:
            t_y = -self.function_calculator_velocity(y_error, velocity_max = self.velocity_max , error_max=(x_max/2))
        else:
            t_y = self.function_calculator_velocity(y_error, velocity_max = self.velocity_max , error_max=(x_max/2))
        w_z = v_x = float(t_y / 2)

        msg_value_control = Twist()
        msg_value_control.linear.x = v_x
        msg_value_control.angular.x = w_x
        msg_value_control.angular.z = w_z
        self.velocity_control_pub.publish(msg_value_control)
        
if __name__ == '__main__':
    try:
        cal_control_node = CalculatorControl()
        rospy.spin()
    except rospy.ROSInterruptException:
        pass