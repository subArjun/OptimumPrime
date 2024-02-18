/*
*/

#include <L298NX2.h>

// Pin definition
const unsigned int left_EN_A = 10;  //D10 Left Front PWM
const unsigned int left_IN1_A = 14; //A0
const unsigned int left_IN2_A = 15;  //A1

const unsigned int left_IN1_B = 16; //A2 Back Left
const unsigned int left_IN2_B = 17; //A3
const unsigned int left_EN_B = 9; // D9 PWM

const unsigned int right_EN_A = 6; //D6 Front Right PWM
const unsigned int right_IN1_A = 18; //A4
const unsigned int right_IN2_A = 19;  //A5

const unsigned int right_IN1_B = 3;  //A6 Back Right
const unsigned int right_IN2_B = 4;  //A7
const unsigned int right_EN_B = 5; //D5 PWM

const unsigned int interruptPin = 2; //E-stop Pin
const unsigned int powertrainPin = A6;
const unsigned int electronicPin = A7;

unsigned int ctr = 0;

// Initialize both motors
L298NX2 left_motors(left_EN_A, left_IN1_A, left_IN2_A, left_EN_B, left_IN1_B, left_IN2_B);
L298NX2 right_motors(right_EN_A, right_IN1_A, right_IN2_A, right_EN_B, right_IN1_B, right_IN2_B);

const byte numChars = 64;
char receivedChars[numChars]; 
char speedChars[32];
boolean newData = false;
volatile byte Estop = false;
bool rightData = false;

int left = 0; 
int right = 0;

void setup() {
  Serial.begin(9600);
  while (!Serial) {
  ; // wait for serial port to connect. Needed for native USB
  }
  pinMode(7, OUTPUT);
  digitalWrite(7, HIGH);
  pinMode(2, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(interruptPin), estop, CHANGE);
}

void loop() {
  while (!Serial) {
  ; // wait for serial port to connect. Needed for native USB
  }
  while (!Estop){
    // left_motors.setSpeed(100);
    // right_motors.setSpeed(100);
    // left_motors.forward();
    // right_motors.forward();
    // delay(3000);
    // left_motors.stop();
    // right_motors.stop();
    // left_motors.setSpeed(100);
    // right_motors.setSpeed(100);
    // left_motors.forward();
    // right_motors.backward();
    // delay(3000);
    // left_motors.stop();
    // right_motors.stop();
    // left_motors.forward();
    // right_motors.forward();
    // delay(5000);
    // left_motors.stop();
    // right_motors.stop();
    
    recvWithEndMarker();
    showNewNumber();
    //readVoltage();
  }
  //readVoltage();
}

void recvWithEndMarker() {
    static byte ndx = 0;
    static byte ndx2 = 0;
    char endMarker = '\n';
    char middleMarker = 'o';
    char rc;
    
    
    if (Serial.available() > 0) {
        rc = Serial.read();
        
        if (rc == endMarker) {
          receivedChars[ndx] = '\0'; // terminate the string
          speedChars[ndx2] = '\0'; // terminate the string
          ndx2 = 0;
          ndx = 0;
          newData = true;
          rightData = false;
        }
        else if ((rc != middleMarker) && (!rightData)) {
            receivedChars[ndx] = rc;
            
            ndx++;
            if (ndx >= numChars) {
                ndx = numChars - 1;
            }
        }
        else if (rc != endMarker) {
            
            rightData = true;
            if (rc != middleMarker){
              speedChars[ndx2] = rc;
              ndx2++;
              if (ndx2 >= numChars) {
                  ndx2 = numChars - 1;
              }
            }
        }
    }
}

void showNewNumber() {
    if (newData == true) {
        left = 0;             // new for this version
        left = atoi(receivedChars);   // new for this version
        
        right = 0;
        right = atoi(speedChars);
        
        if (right > 0){
          right_motors.forward();
          right_motors.setSpeed(right);
        }
        else if (right < 0){
          right_motors.backward();
          right_motors.setSpeed(right);
        }
        else {
          right_motors.stop();
        }
        
        if (left > 0){
          left_motors.forward();
          left_motors.setSpeed(left);
        }
        else if (right < 0){
          left_motors.backward();
          left_motors.setSpeed(left);
        }
        else {
          left_motors.stop();
        }
        //Serial.println("This just in ... ");
       // Serial.println(speedChars, receivedChars);
        //Serial.print("Data as Number ... ");    // new for this version
        Serial.println(right);     // new for this version
        Serial.println(left);
        newData = false;
    }
}

void estop() {
  Estop = false;
  Serial.println("hello");
}

void readVoltage() {
  if (ctr == 60000 ) {
    float powertrain = analogRead(powertrainPin);
    float electronics = analogRead(electronicPin);
    Serial.print(powertrain);
    Serial.print(',');
    Serial.print(electronics);
    Serial.print(',');
    if (Estop){
      Serial.println("true");
    }
    else{
      Serial.println("false");
    }
    ctr++;
  }
  else if (ctr > 60000) {
    ctr = 0;
  }
  else {
    ctr++;
  }
}


