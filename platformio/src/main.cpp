#include <Arduino.h>
#include <Time.h>

double sensorValue1;
double sensorValue2;
double sensorValue3;
double millivolt1;
double millivolt2;
double millivolt3;
double t;

void setup()
{
    Serial.begin(9600); //28800
}

void loop()
{
    sensorValue1 = analogRead(A0);
    millivolt1 = (sensorValue1 / 1023) * 5000;
    // Serial.println(millivolt1);

    sensorValue2 = analogRead(A1);
    millivolt2 = (sensorValue2 / 1023) * 5000;

    sensorValue3 = analogRead(A2);
    millivolt3 = (sensorValue3 / 1023) * 5000;

    t = millis() / 1000.0;

    Serial.print(t);
    Serial.print(" ");
    Serial.print(millivolt1);
    Serial.print(" ");
    Serial.print(millivolt2);
    Serial.print(" ");
    Serial.println(millivolt3);
    delay(1);

}
