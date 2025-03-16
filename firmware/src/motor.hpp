#include "Arduino.h"
#include "DRV8825.h"
#include "Servo.h"
#include "switch.hpp"
/////////////////////////////////////////ServoMotor/////////////////////////////////////////
class ServoMotor
{
  private:
    int __bound_min;
    int __bound_max;
    uint8_t __pin;
    Servo servo;
    int __angle_current = -1;
  public:
    ServoMotor();
    void attach(uint8_t pin);
    void write(int angle);
    int read();
};
ServoMotor::ServoMotor(){}
void ServoMotor::attach(uint8_t pin)
{
    this->__pin = pin;
    this->servo.attach(pin);
    this->__angle_current = 0;
};
void ServoMotor::write(int angle)
{
    this->servo.write(angle);
    this->__angle_current = angle;
}
int ServoMotor::read()
{
    return this->__angle_current;
}
/////////////////////////////////////////StepperMotor/////////////////////////////////////////

const uint8_t STEPPER_MOTOR_FW = 0;  
const uint8_t STEPPER_MOTOR_BW = 1;

class StepperMotor
{
  private:
    uint8_t __dir_pin;
    uint8_t __step_pin;
    MySwitch __fw;
    MySwitch __bw;
    uint8_t __direction_current = 0;
    int   __pul_per_rev;

  public:
    DRV8825 stepper;
    StepperMotor(){};
    begin(uint8_t dir_pin, uint8_t step_pin, uint8_t fw_pin, uint8_t bw_pin, int pul_per_rev);
    bool step(uint8_t direction);
    float step_rotations(uint8_t direction, float num_rotations, unsigned int time_delay_control_us);
};
StepperMotor::begin(uint8_t dir_pin, uint8_t step_pin, uint8_t fw_pin, uint8_t bw_pin, int pul_per_rev)
{   
    this->__dir_pin = dir_pin;
    this->__step_pin = step_pin;
    this->stepper.begin(dir_pin, step_pin);
    this->__fw.set(fw_pin);
    this->__bw.set(bw_pin);
    this->__pul_per_rev = pul_per_rev;
};

bool StepperMotor::step(uint8_t direction = STEPPER_MOTOR_FW)
{
  if(this->__direction_current != direction) 
  {
    stepper.setDirection(direction);
    this->__direction_current = direction;
  }

  if(direction == DRV8825_CLOCK_WISE && this->__fw.get_stats() == false)
  {
    stepper.step();
    return true;
  }
  else if (direction == DRV8825_COUNTERCLOCK_WISE && this->__bw.get_stats() == false)
  {
    stepper.step();
    return true;
  }

  return false;
};

float StepperMotor::step_rotations(uint8_t direction = STEPPER_MOTOR_FW, float num_rotations = 1, unsigned int time_delay_control_us = 30)
{
  float rotaions_current = 0;
  for (unsigned int pulse = 0; pulse < (num_rotations * this->__pul_per_rev); pulse++)
  {
    if(this->step(direction))
    {
      rotaions_current = float(pulse / this->__pul_per_rev);
      delayMicroseconds(time_delay_control_us);
    }
    else
    {
      return rotaions_current;
    }
    
  }
  return rotaions_current;
};



