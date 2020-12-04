#include <Servo.h>

Servo My_servo;
Servo My_servo1;
int PotValue = 0;
int Down = 120;
int Up = 30;
int Still = 90;

void setup() {
  My_servo.attach(12);
  My_servo1.attach(14);
  Serial.begin(9600);
  delay(7000);
}

void loop() {
   My_servo1.write(Down);
   delay(6200);
   My_servo1.write(Still);
   My_servo.write(Up);
   delay(1000);
   My_servo.write(Still);
   delay(5000);
   My_servo1.write(Up);
   delay(6200);
   My_servo1.write(Still);
   delay(5000);
   My_servo1.write(Down);
   delay(6200);
   My_servo1.write(Still);
   My_servo.write(Down);
   delay(1000);
   My_servo.write(Still);
   delay(5000);
   My_servo1.write(Up);
   delay(6200);
}

