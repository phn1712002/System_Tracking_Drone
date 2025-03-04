#include "Arduino.h"
#include "DRV8825.h"
#include "Servo.h"
/////////////////////////////////////////ServoMotor/////////////////////////////////////////
class ServoMotor
{
  private:
    int __bound_min;
    int __bound_max;
    uint8_t __pin;
    Servo servo;
  public:
    ServoMotor();
    void attach(uint8_t pin, int bound_min, int bound_max);
    void write(int angle);
};
ServoMotor::ServoMotor(){}
void ServoMotor::attach(uint8_t pin, int bound_min, int bound_max)
{
    this->__pin = pin;
    this->__bound_min = bound_min;
    this->__bound_max = bound_max;
    this->servo.attach(pin, bound_min ,bound_max);
};
void ServoMotor::write(int angle)
{
    this->servo.write(angle);
}
/////////////////////////////////////////StepperMotor/////////////////////////////////////////
class StepperMotor
{
  private:
    uint8_t __dir_pin;
    uint8_t __step_pin;

  public:
    DRV8825 stepper;
    StepperMotor(uint8_t dir_pin, uint8_t step_dir);
    void step(uint8_t vector, int sleep);
};
StepperMotor::StepperMotor(uint8_t dir_pin, uint8_t step_dir)
{   
    this->__dir_pin = dir_pin;
    this->__step_pin = step_dir;
    this->stepper.begin(dir_pin, step_dir);
};
void StepperMotor::step(uint8_t vector, int sleep = 50)
{
    if (vector != 0)
    {
        uint8_t clock_wire = vector > 0 ? DRV8825_CLOCK_WISE: DRV8825_COUNTERCLOCK_WISE;
        stepper.setDirection(clock_wire);
        delay(sleep);
        stepper.step();
        delay(sleep);
    }
}



