//
#include <Arduino.h>
#include <ros.h>
#include <std_msgs/String.h>
#include <geometry_msgs/Twist.h>
#include <ErriezLCDKeypadShield.h>

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

# define DEBUG_WITH_LCD true
LCDKeypadShield shield;
void view_debug_mcu_in_lcd(const char* msg){
  if(DEBUG_WITH_LCD){
    shield.clear();
    shield.print(F(msg));
  }
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

int angle_link_0_current = 0;
int angle_link_1_current = 0;
int angle_link_2_current = 0;


// SUBSCRIBER
void callback(const geometry_msgs::Twist& msg) 
{
  linear_x_current = msg.linear.x;
  angular_x_current = msg.angular.x;
  angular_z_current = msg.angular.z;

  int angle_1 = angle_link_1_current + angular_z_current;
  link_1.write(angle_1)

  int angle_2 = angle_link_2_current + angular_x_current;
  link_2.write(angle_2)  
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


  // LCD Debug
  if(DEBUG_WITH_LCD)
  {
    shield.backlightOn();
  }
}


void loop() 
{
  nh.spinOnce();
  delay(time_delay_spin_once);  
}