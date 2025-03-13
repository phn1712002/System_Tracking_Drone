#include <Arduino.h>

class ExecutionTimer
{
private:
    unsigned long start_time;
    unsigned long end_time;
public:
    ExecutionTimer();
    void start();
    void stop();
    unsigned long getElapsedTime();
};

ExecutionTimer::ExecutionTimer() : start_time(0), end_time(0) {}

void ExecutionTimer::start()
{
    this->start_time = millis();
}

void ExecutionTimer::stop()
{
    this->end_time = millis();
}

unsigned long ExecutionTimer::getElapsedTime()
{   
    if(this->end_time < this->start_time)
    {
        return 0;
    }
    else
    {
        return this->end_time - this->start_time;
    }
}