#include "Arduino.h"

class MySwitch
{
  private:
  uint8_t __pin;

  public:
    MySwitch(){};
    void set(uint8_t pin);
    bool get_stats();
};
void MySwitch::set(uint8_t pin){

  pinMode(pin, INPUT_PULLUP);
  this->__pin = pin;
}

bool MySwitch::get_stats()
{
  return digitalRead(this->__pin) == LOW ? true : false;
}

