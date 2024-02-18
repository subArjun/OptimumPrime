/*
Code to connect to Jetson Orin Nano over serial and actuate a gripper using PWM and the Servo library. 
The state of 4 dispensers are read and transmitted over serial. THey use limit switches and interrupts.
*/
#include <Servo.h>

// #define USE_TIMER_2     true
// // Init timer ITimer2
// ITimer2.init();
// void TimerHandler();
void recvOneChar();
void showNewData();

Servo gripper; 

char receivedChar;
boolean newData = false;

const unsigned int limit_A = 14; //A0 Dispenser A
const unsigned int limit_B = 15;  //A1 Dispenser B
const unsigned int limit_C = 16; //A2 Dispenser C
const unsigned int limit_D = 17; //A3 Dispenser D

const unsigned int gripperPin = 9; // D9 PWM Gripper Pin

void setup() {
    Serial.begin(9600);
    while (!Serial) {
  ; // wait for serial port to connect. Needed for native USB
  }
  gripper.attach(gripperPin);
  
}

void loop() {
    recvOneChar();
    showNewData();
}

void recvOneChar() {
    if (Serial.available() > 0) {
        receivedChar = Serial.read();
        newData = true;
    }
}

void showNewData() {
    if (newData == true) {
        if (receivedChar == 'c') {
          gripper.write(20);
          Serial.println("CLose");
        }
        else if (receivedChar == 'o') {
          gripper.write(175);
          Serial.println("Open");
        }
        newData = false;
    }
}