#include "Arduino.h"


void setup() {
    Serial.begin(9600); // khởi tạo cổng serial xuất ra thông tin
  }
  void loop() {
    Serial.println("Testing"); // in ra dòng chữ Hello World
    delay(1000); // tạm dừng chương trình 1 giây
  }