#include <Servo.h>

#define numVals 5
#define digitsPerValue 1
int valuesReceived[numVals];

int stringLength = numVals + 1; //$00000
int counter = 0;
bool counterStart = false;
string receivedString;

void setup() {
  Serial.begin(9600);

}

void receiveData() {
  while(Serial.available()) {
    char c = Serial.read();
    if(c == '$'){
      counterStart = true;
    }
    if(counterStart){
      if(counter < stringLength){
         receivedString = String(receivedString + c);
         counter++; 
      }
      if(counter >= stringLength){
        for(int i = 0; i < numVals; i++){
          int num = (i * digitsPerValue) + 1;
          valuesReceived[i] = receivedString.substring(num,num+digitsPerValue).toInt();
        }
        receivedString = "";
        counter = 0;
        counterStart = false;
      }
    }
  }
}

void loop() {
  // put your main code here, to run repeatedly:

}
