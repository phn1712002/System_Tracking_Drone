//
#include <Arduino.h>
#include <ros.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Twist.h>

//
#include "motor.hpp"

// ROS 
ros::NodeHandle nh;

// DEBUG
std_msgs::String debug_mcu_msg;
ros::Publisher debug_mcu_pub("/debug_mcu", &debug_mcu_msg);
void view_debug_mcu(const char* msg){
  debug_mcu_msg.data = msg;
  debug_mcu_pub.publish(&debug_mcu_msg);
}

// MOTOR
# define PIN_PWM_LINK_2 12
# define PIN_PWM_LINK_1 11
ServoMotor link_2;
ServoMotor link_1;

// VALUES
unsigned long time_delay_spin_once = 1;

unsigned long time_delay_get_param = 1;
int bound_min_wx = -1;
int bound_max_wx = -1;
int bound_min_wz = -1;
int bound_max_wz = -1;

float linear_x_current = 0;
float angular_x_current = 0;
float angular_z_current = 0;

// SUBSCRIBER
void callback(const geometry_msgs::Twist& msg) 
{
  linear_x_current = msg.linear.x;
  angular_x_current = msg.angular.x;
  angular_z_current = msg.angular.z;
}
ros::Subscriber<geometry_msgs::Twist> velocity_control_sub("velocity_control", &callback);


void setup() {

  // Init
  nh.initNode();
  nh.advertise(debug_mcu_pub);
  nh.subscribe(velocity_control_sub);

  // Get param from ROS
  while (!nh.getParam("bound_min_wx", &bound_min_wx))
  {
    delay(time_delay_get_param);
  }
  while (!nh.getParam("bound_max_wx", &bound_max_wx))
  {
    delay(time_delay_get_param);
  }
  while (!nh.getParam("bound_min_wz", &bound_min_wz))
  {
    delay(time_delay_get_param);
  }
  while (!nh.getParam("bound_min_wz", &bound_min_wz))
  {
    delay(time_delay_get_param);
  }
  
  // Set bound min max for link 1 and link 2
  link_2.attach(PIN_PWM_LINK_2, bound_min_wx, bound_max_wx);
  link_1.attach(PIN_PWM_LINK_1, bound_min_wz, bound_max_wz);
}


void loop() 
{
  nh.spinOnce();
  delay(time_delay_spin_once);  
}