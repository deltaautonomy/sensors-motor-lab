#include "communication.h"
#include <Servo.h>

#define stp 4
#define dir 5
#define MS1 3
#define MS2 44
#define EN 46
#define in_photo 8
#define out_photo A0
#define buttonPin 2

#define servoin 9
#define flexpin A4

int circuitState = HIGH; // the current state of the output pin
int buttonState; // the current reading from the input pin
int lastButtonState = LOW; // the previous reading from the input pin

unsigned long lastDebounceTime = 0; // the last time the output pin was toggled
unsigned long debounceDelay = 50; // the debounce time; increase if the output flickers

int mode;

Servo servo1;

void setup()
{
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
    servo1.attach(servoin);
}

//Main loop
void loop()
{

    recieve_data();
    buttonPush();
    if (circuitState == HIGH) { //&&(rx_packet.global_switch == 1)
        switch (mode) //rx_packet.state
        {
        case 0: {
            StepperMain();
        } break;
        case 1: {
            ServoMain();
        } break;
        case 2: {
            //DC Motor Prateek
        } break;
        case 3: {
            //DC Motor Shubham
        } break;
        default:
            break;
        }
    }
    send_data();
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
    for (int x = 1; x < 50; x++) //Loop the forward stepping enough times for motion to be visible
    {
        digitalWrite(stp, HIGH); //Trigger one step forward
        delay(1);
        digitalWrite(stp, LOW); //Pull step pin low so it can be triggered again
        delay(1);
    }
}

void StepperMain()
{
    digitalWrite(in_photo, HIGH);
    uint8_t val = analogRead(out_photo);
    Serial.println(val); //tx_packet.slot_encoder  = val;
    if (val > 15) {
        digitalWrite(EN, LOW); //Pull enable pin low to allow motor control
        StepperStep();
    } else {
        digitalWrite(EN, HIGH);
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
