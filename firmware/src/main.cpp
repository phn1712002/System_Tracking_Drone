//pio run --target upload --upload-port /dev/ttyUSB0 -e nanoatmega328new -d $TRACKING_DRONE_WS/firmware/


//
#include <Arduino.h>
#include <ros.h>
#include <std_msgs/String.h>
#include <std_msgs/Bool.h>
#include <geometry_msgs/Twist.h>
#include <ErriezLCDKeypadShield.h>

//
#include "tools.hpp"
#include "motor.hpp"`

// ROS 
ros::NodeHandle nh;

// DEBUG
std_msgs::String debug_mcu_msg;
ros::Publisher debug_mcu_pub("/debug_mcu", &debug_mcu_msg);
void view_debug_mcu(const char* msg){
  debug_mcu_msg.data = msg;
  debug_mcu_pub.publish(&debug_mcu_msg);
}

geometry_msgs::Twist value_motor_current_msg;
ros::Publisher value_motor_current_pub("/value_motor_current", &value_motor_current_msg);
void publish_value_motor_current(float angle_link_0, int angle_link_1, int angle_link_2)
{
  value_motor_current_msg.linear.x = angle_link_0;
  value_motor_current_msg.angular.x = angle_link_2;
  value_motor_current_msg.angular.z = angle_link_1;
  
  value_motor_current_pub.publish(&value_motor_current_msg);
}

// TOOLS
ExecutionTimer timer;

// SWITCHw
# define PIN_SWITCH_FW 9
# define PIN_SWITCH_BW 10

// MOTOR
# define PIN_PWM_LINK_2 12
# define PIN_PWM_LINK_1 11
# define PIN_DIR_LINK_0 2
# define PIN_STEP_LINK_0 6
# define PULSES_PER_REVOLUTION 3200
# define ANGLE_MIN_PER_STEP 0
# define ANGLE_MAX_PER_STEP 10
ServoMotor link_2;
ServoMotor link_1;
StepperMotor link_0;


// VALUES
unsigned long const time_delay_spin_once = 1;
unsigned long const time_delay_get_param = 15;
int value_reset_link_0;
int angle_reset_link_1;
int angle_reset_link_2;
unsigned long const time_out_set_angle_link_start = 1000;
unsigned long const time_delay_control_link_12 = 15;
unsigned long const time_delay_control_link_0 = 30;


// SUBSCRIBER
void cb_velocity_control_with_ui(const geometry_msgs::Twist& msg) 
{
  if(msg.linear.x != 0)
  {
    float value = msg.linear.x;
    int sign = value / abs(value);
    float abs_value = abs(value);
    
    // Calc dir with sign value
    int dir = STEPPER_MOTOR_BW;
    if(sign == 1) dir = STEPPER_MOTOR_FW;

    link_0.step_rotations(dir, abs_value, time_delay_control_link_0);
  }
  if(msg.angular.z != 0) link_1.write(int(msg.angular.z));
  if(msg.angular.x != 0) link_2.write(int(msg.angular.x));
}
ros::Subscriber<geometry_msgs::Twist> velocity_control_with_ui_sub("velocity_control_with_ui", &cb_velocity_control_with_ui);

void cb_velocity_control_with_model(const geometry_msgs::Twist& msg) 
{
  float num_rotation_step = 0;
  // Control Link 0
  if(msg.linear.x != 0)
  {
    float value_control = msg.linear.x;
    int sign = value_control / abs(value_control);
    float abs_value_control = abs(value_control);
    int dir = STEPPER_MOTOR_BW;
    if(sign == 1) dir = STEPPER_MOTOR_FW;

    num_rotation_step = link_0.step_rotations(dir, abs_value_control, time_delay_control_link_0);
  }

  // Control Link 1
  if(msg.angular.z != 0)
  {
    int angle_current = link_1.read();
    int value_control = int(msg.angular.z);
    int abs_value_control = abs(value_control);
    int sign = value_control / abs_value_control;

    int value_control_current = map(abs_value_control, 0, 1, ANGLE_MIN_PER_STEP, ANGLE_MAX_PER_STEP);
    link_1.write(angle_current + (value_control_current * sign));
  }

  // Control Link 2
  if(msg.angular.x != 0)
  {
    int angle_current = link_2.read();
    int value_control = int(msg.angular.x);
    int abs_value_control = abs(value_control);
    int sign = value_control / abs_value_control;

    int value_control_current = map(abs_value_control, 0, 1, ANGLE_MIN_PER_STEP, ANGLE_MAX_PER_STEP);
    link_2.write(angle_current + (value_control_current * sign));
  }

  publish_value_motor_current(num_rotation_step, link_1.read(), link_2.read());
}

ros::Subscriber<geometry_msgs::Twist> velocity_control_with_model_sub("velocity_control_with_model", &cb_velocity_control_with_model);

void cb_reset_vx(const std_msgs::Bool& msg)
{
    if(msg.data)
    {
      while(link_0.step(value_reset_link_0))
      { 
        delayMicroseconds(time_delay_control_link_0);
      }
    }
}
ros::Subscriber<std_msgs::Bool> reset_vx("reset_vx", &cb_reset_vx);

void cb_reset_wx(const std_msgs::Bool& msg)
{
    if(msg.data)
    {
      link_2.write(angle_reset_link_2);
    }
}
ros::Subscriber<std_msgs::Bool> reset_wx("reset_wx", &cb_reset_wx);

void cb_reset_wz(const std_msgs::Bool& msg)
{
    if(msg.data)
    {
      link_1.write(angle_reset_link_1);
    }
}
ros::Subscriber<std_msgs::Bool> reset_wz("reset_wz", &cb_reset_wz);


void setup() {
  // Init
  nh.initNode();
  nh.advertise(debug_mcu_pub);
  nh.advertise(value_motor_current_pub);
  nh.subscribe(velocity_control_with_ui_sub);
  nh.subscribe(velocity_control_with_model_sub);
  nh.subscribe(reset_vx);
  nh.subscribe(reset_wx);
  nh.subscribe(reset_wz);
  
  // Get param from ROS
  while (!nh.getParam("value_reset_link_0", &value_reset_link_0))
  {
    delay(time_delay_get_param);
  }
  while (!nh.getParam("angle_reset_link_1", &angle_reset_link_1))
  {
    delay(time_delay_get_param);
  }
  while (!nh.getParam("angle_reset_link_2", &angle_reset_link_2))
  {
    delay(time_delay_get_param);
  }
  
  // Set bound min max for link 1 and link 2
  link_2.attach(PIN_PWM_LINK_2);
  link_1.attach(PIN_PWM_LINK_1);

  // Reset angle for link 1 and link 2 of robot in time_out_set_angle_link_start ms
  timer.start();
  while (timer.getElapsedTime() < time_out_set_angle_link_start)
  {
    link_1.write(angle_reset_link_1);
    link_2.write(angle_reset_link_2);
    delay(time_delay_control_link_12);
    timer.stop();
  }
  
  // Setting link 0
  link_0.begin(PIN_DIR_LINK_0, PIN_STEP_LINK_0, PIN_SWITCH_FW, PIN_SWITCH_BW, PULSES_PER_REVOLUTION);
  while(link_0.step(value_reset_link_0))
  {
    delayMicroseconds(time_delay_control_link_0);
  }
}

void loop() 
{
  nh.spinOnce();
  delay(time_delay_spin_once);  
}