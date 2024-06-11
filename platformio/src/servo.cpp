// #include <Arduino.h>
// #include <Time.h>
// #include <Servo.h>

// Servo left_servo;  // create servo object to control a servo
// Servo right_servo;

// double sensorValue;
// double millivolt;

// void setup()
// {
//     Serial.begin(9600);
//     left_servo.attach(9);  // attaches the left servo to pin 9 to the servo object
//     right_servo.attach(10);
// }

// void loop()
// {
//     sensorValue = analogRead(A0);
//     millivolt = (sensorValue / 1023) * 5000;

//     if (millivolt >= 2000)
//     {
//         right_servo.write(85);
//         left_servo.write(95);
//         // delay(500);
//     }
//     else{
//         right_servo.write(0);
//         left_servo.write(180);
//         // delay(500);
//     }
//     delay(100);
    
//     /* Servo test */
//     // right_servo.write(85);
//     // left_servo.write(95);
//     // delay(5000);
//     // right_servo.write(0);
//     // left_servo.write(180);
//     // delay(5000);
// }
