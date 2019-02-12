/******************************************************************************
  Teaam Delta Autonomy - Sensors and Motors Assignment
******************************************************************************/
#include "communication.h"
#include <Servo.h>

#define step_stp 4
#define step_dir 5
#define step_MS1 3
#define step_MS2 48
#define step_EN  46
#define photo_in 8
#define photo_out A0

#define buttonPin 2

#define servoin 9
#define flexpin A4

int circuitState = HIGH; 

struct Button
{
    int state;
    int last_state = LOW;
    int time = millis();
}; 

volatile Button button;

unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers

Servo servo1;

int mode = 0;//temp 


/************************** Stepper **************************/

//Reset Stepper pins to default states
void resetStepperPins()
{
  digitalWrite(step_stp, LOW);
  digitalWrite(step_dir, LOW);
  digitalWrite(step_MS1, LOW);
  digitalWrite(step_MS2, LOW);
  digitalWrite(step_EN, HIGH);
}

//Microstep function for stepper
void StepperStep()
{
  for (int x = 1; x < 1000; x++) //Loop the forward stepping enough times for motion to be visible
  {
    Serial.println("Motor");
    digitalWrite(step_stp, HIGH); //Trigger one step forward
    delay(1);
    digitalWrite(step_stp, LOW); //Pull step pin low so it can be triggered again
    delay(1);
  }
}

//Stepper Function with Slot Encoder
void StepperMain()
{
  digitalWrite(photo_in, HIGH);
  uint8_t val = analogRead(photo_out);
  tx_packet.slot_encoder  = val;
  Serial.print("Slot Encoder");
  Serial.println(val);
  
  if (val > 5)
  {
    digitalWrite(step_EN, LOW);                   //Pull enable pin low to allow motor control
    StepperStep();
  }
  else
  {
    digitalWrite(step_EN, HIGH);
  }
  resetStepperPins();
}


//Microstep function for stepper
void StepperPosStep(uint8_t angle, uint8_t dir)
{
  if (dir == 0)
    digitalWrite(step_dir, HIGH); //Pull direction pin low to move "forward" and high to move "reverse"
  else
    digitalWrite(step_dir, LOW);
  int t = map(angle, 0, 360, 1, 1600);
  for (int x = 1; x < t; x++) //Loop the forward stepping enough times for motion to be visible
  {
    digitalWrite(step_stp, HIGH); //Trigger one step forward
    delay(1);
    digitalWrite(step_stp, LOW); //Pull step pin low so it can be triggered again
    delay(1);
  }
}

// Stepper function for position control
void StepperPos()
{
  uint16_t angle = rx_packet.stepper_value;
  uint8_t dir = rx_packet.stepper_dir;
  //tx_packet.slot_encoder  = val;
  digitalWrite(step_EN, LOW); //Pull enable pin low to allow motor control
  StepperPosStep(angle, dir);
  resetStepperPins();
}

/************************** Button **************************/

void button_isr()
{
  noInterrupts();
  button.state = digitalRead(buttonPin);
  if (button.state == button.last_state) {
    button.time = millis();
    return;
  }
  if (!button.state) 
    button.time = millis();
  if (button.state && (millis() - button.time > debounceDelay)) {
    button.time = millis();
    circuitState = !circuitState;

  }

  button.last_state = button.state;
  delay(5);
  interrupts();
}

/************************** Servo **************************/

void ServoMain()
{
  //servoposition = rx_packet.servoangle
  uint16_t flexposition = analogRead(flexpin);
  int servoposition = map(flexposition, 10, 1023, 0, 90);
  servoposition = constrain(servoposition, 0, 90);
  servo1.write(servoposition);
  delay(1000);
  //  tx_packet./
}


/************************** Setup **************************/
void setup() {
  // stepper code
  pinMode(step_stp, OUTPUT);
  pinMode(step_dir, OUTPUT);
  pinMode(step_MS1, OUTPUT);
  pinMode(step_MS2, OUTPUT);
  pinMode(step_EN, OUTPUT);

  // slot encoder code
  pinMode(photo_in, OUTPUT);
  pinMode(photo_out, INPUT);
  resetStepperPins(); //Set step, direction, microstep and enable pins to default states

  // push button code
  pinMode(buttonPin, INPUT_PULLUP);
  attachInterrupt(digitalPinToInterrupt(buttonPin), button_isr, CHANGE);

  Serial.begin(9600); //Open Serial connection for debugging
  servo1.attach(servoin);
}

//Main loop
void loop() {

  recieve_data();
  if (circuitState == HIGH) { //&&(rx_packet.global_switch == 1)
    switch (mode)   //rx_packet.state
    {
      case 0:
        {
          StepperMain();
        }
        break;
      case 1:
        {
          StepperPos();
        }
        break;
      case 2:
        {
          ServoMain();
        }
        break;
      case 3:
        {
          //ServoPos();
        }
        break;
      case 4:
        {
          //DC Motor Sensor 1
        }
        break;
      case 5:
        {
          //DC Motor Sensor 2
        }
        break;
      case 6:
        {
          //DC Motor Sensor 3
        } break;
      default:
        break;
    }
  }
  send_data();
}
