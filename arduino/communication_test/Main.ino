/****************************************************************************** 
SparkFun Easy Driver Basic Demo
Toni Klopfenstein @ SparkFun Electronics
March 2015
https://github.com/sparkfun/Easy_Driver

Simple demo sketch to demonstrate how 5 digital pins can drive a bipolar stepper motor,
using the Easy Driver (https://www.sparkfun.com/products/12779). Also shows the ability to change
microstep size, and direction of motor movement.

Development environment specifics:
Written in Arduino 1.6.0

This code is beerware; if you see me (or any other SparkFun employee) at the local, and you've found our code helpful, please buy us a round!
Distributed as-is; no warranty is given.

Example based off of demos by Brian Schmalz (designer of the Easy Driver).
http://www.schmalzhaus.com/EasyDriver/Examples/EasyDriverExamples.html
******************************************************************************/
//Declare pin functions on Redboard
#define stp 4
#define dir 5
#define MS1 3
#define MS2 44
#define EN  46
#define in_photo 8
#define out_photo A0
#define buttonPin 2

int circuitState = HIGH;         // the current state of the output pin
int buttonState;             // the current reading from the input pin
int lastButtonState = LOW;   // the previous reading from the input pin

unsigned long lastDebounceTime = 0;  // the last time the output pin was toggled
unsigned long debounceDelay = 50;    // the debounce time; increase if the output flickers

int mode;

void setup() {
  // stepper code
  pinMode(stp, OUTPUT);
  pinMode(dir, OUTPUT);
  pinMode(MS1, OUTPUT);
  pinMode(MS2, OUTPUT);
  pinMode(EN, OUTPUT);

  // slot encoder code
  pinMode(in_photo, OUTPUT);
  pinMode(out_photo, INPUT);
  resetStepperPins(); //Set step, direction, microstep and enable pins to default states

  // push button code
  pinMode(buttonPin, INPUT);
  
  Serial.begin(9600); //Open Serial connection for debugging

}

//Main loop
void loop() {

  buttonPush();
    
  switch (mode)
  {
    case 0:
      {
        StepperMain();
      }
      break;
    default:
      break;
  }
  
}

//Reset Easy Driver pins to default states
void resetStepperPins()
{
  digitalWrite(stp, LOW);
  digitalWrite(dir, LOW);
  digitalWrite(MS1, LOW);
  digitalWrite(MS2, LOW);
  digitalWrite(EN, HIGH);
}

//Microstep mode function
void StepperStep()
{
  Serial.println("Moving forward at default step mode.");
  digitalWrite(dir, LOW); //Pull direction pin low to move "forward" and high to move "reverse"
  digitalWrite(MS1, LOW); //Pull MS1, and MS2 high to set logic to 1/8th microstep resolution
  digitalWrite(MS2, LOW);
  for(int x= 1; x<1000; x++)  //Loop the forward stepping enough times for motion to be visible
  {
    digitalWrite(stp,HIGH); //Trigger one step forward
    delay(1);
    digitalWrite(stp,LOW); //Pull step pin low so it can be triggered again
    delay(1);
  }
}

void StepperMain()
{
  if(circuitState == HIGH){
    digitalWrite(in_photo, HIGH);
    int val = analogRead(out_photo);
    Serial.println(val);
    if (val > 15)
    {
      digitalWrite(EN, LOW); //Pull enable pin low to allow motor control
      StepperStep();
    }
    else
    {
      digitalWrite(EN, HIGH);
    }
  }
  resetStepperPins();
}

void buttonPush()
{
  int reading = digitalRead(buttonPin);
  
  if (reading != lastButtonState) {
    lastDebounceTime = millis();
  }

  // Code for switching the states between button push
  if ((millis() - lastDebounceTime) > debounceDelay) {

    if (reading != buttonState) {
      buttonState = reading;

      // Toggle the Enable Pin if the new button state is HIGH
      if (buttonState == HIGH) {
        circuitState = !circuitState;
      }
    }
  }
  // save the button reading as last button reading
  lastButtonState = reading;
}
