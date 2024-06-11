#include <Servo.h>
Servo servo1;
Servo servo2;
Servo servo3;
Servo servo4;
Servo servo5;
void setup() {
  // put your setup code here, to run once:
  Serial.begin(9600);
  pinMode(A0, OUTPUT);
  pinMode(A1, OUTPUT);
  pinMode(A2, OUTPUT);
  pinMode(A3, OUTPUT);
  pinMode(A4, OUTPUT);
  servo1.attach(A0);
  servo2.attach(A1);
  servo3.attach(A2);
  servo4.attach(A3);
  servo5.attach(A4);
  servo1.write(0);
  servo2.write(0);
  servo3.write(0);
  servo4.write(0);
  servo5.write(0);
}

int state = 0;
int x = 0;
void loop() {
  // put your main code here, to run repeatedly:
  int input = Serial.read();
  if(input == 114){
    servo1.write(180);
    servo2.write(120);
    servo3.write(180);
    servo4.write(150);
    servo5.write(135);
  }
  else if(input == 112){
    servo1.write(0);
    servo2.write(0);
    servo3.write(0);
    servo4.write(0);
    servo5.write(0);
    }
  else if(input == 115){
    servo1.write(180);
    servo2.write(120);
    servo3.write(0);
    servo4.write(0);
    servo5.write(135);
    }
}
