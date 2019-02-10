#include <PID_v1.h>
#define encoder_ch1 19 // Quadrature encoder A pin
#define encoder_ch2 20 // Quadrature encoder B pin
#define Motor1_enable 44 // PWM outputs to L298N H-Bridge motor driver module
#define Motor1_A1 51
#define Motor1_A2 53
#define Pot_Pin A15
#define MIN_RPM 65
#define ROT_FACTOR 1

volatile double encoder_count = 0;
volatile double left_prev_count = 0;
double RPM;

// Position Control Initialization
double kp_pos = 0.8, ki_pos = 0, kd_pos = 0; // modify for optimal performance
double input_pos = 0, output_pos = 0, setpoint_pos = 0;
PID position_PID(&input_pos, &output_pos, &setpoint_pos, kp_pos, ki_pos, kd_pos, DIRECT);

// Velocity Control Initialization
double kp_vel = 0, ki_vel = 0, kd_vel = 0.0; // modify for optimal performance
double input_vel = 0, output_vel = 0, setpoint_vel = 0;
PID velocity_PID(&input_vel, &output_vel, &setpoint_vel, kp_vel, ki_vel, kd_vel, DIRECT);

void PID_Setup_Position()
{
    position_PID.SetMode(AUTOMATIC);
    position_PID.SetSampleTime(10);
    position_PID.SetOutputLimits(-255, 255);
}

void Motor_Setup()
{
    pinMode(encoder_ch1, INPUT_PULLUP); // quadrature encoder input A
    pinMode(encoder_ch2, INPUT_PULLUP);
    pinMode(Motor1_A1, OUTPUT);
    pinMode(Motor1_A2, OUTPUT);
    pinMode(Motor1_enable, OUTPUT);

    digitalWrite(Motor1_A1, LOW);
    digitalWrite(Motor1_A2, LOW);
    analogWrite(Motor1_enable, 0);

    attachInterrupt(digitalPinToInterrupt(encoder_ch1), Encoder_ISR, CHANGE);
    TCCR5C = TCCR5C & 0b11111000 | 1; // set 31KHz PWM to prevent motor noise
}

void pwmOut(int out)
{ // to H-Bridge board
    if (out > 0) {
        Set_Motor_Direction(0, 1);
    } else {
        Set_Motor_Direction(1, 0);
    }

    out = map(abs(out), 0, 255, MIN_RPM, 255);
    analogWrite(Motor1_enable, out);
}
void Set_Motor_Direction(int A, int B)
{
    //  Update new direction
    digitalWrite(Motor1_A1, A);
    digitalWrite(Motor1_A2, B);
}
void Encoder_ISR()
{
    //  encoder_count++;
    int state = digitalRead(encoder_ch1);
    if (digitalRead(encoder_ch2))
        state ? encoder_count-- : encoder_count++;
    else
        state ? encoder_count++ : encoder_count--;
}
void PID_Loop()
{
    setpoint_pos = analogRead(Pot_Pin); // modify to fit motor and encoder characteristics, potmeter connected to A0
    setpoint_pos = map(setpoint_pos, 0, 1024, -360 * ROT_FACTOR, 360 * ROT_FACTOR);
    setpoint_pos = map(setpoint_pos, -360 * ROT_FACTOR, 360 * ROT_FACTOR, -378 * ROT_FACTOR, 378 * ROT_FACTOR);
    input_pos = encoder_count; // data from encoder
    // Serial.println(encoderPos);                      // monitor motor position
    position_PID.Compute(); // calculate new output
    pwmOut(output_pos);
}
void timer4_init()
{
    TCCR4B = 0x00; // Stop Timer
    TCNT4 = 0xFB80; // 0.02s
    OCR4A = 0x0000; // Output Compare Register (OCR) - Not used
    OCR4B = 0x0000; // Output Compare Register (OCR) - Not used
    OCR4C = 0x0000; // Output Compare Register (OCR) - Not used
    ICR4 = 0x0000; // Input Capture Register (ICR)  - Not used
    TCCR4A = 0x00;
    TCCR4C = 0x00;
}

/**********************************
  Function name : start_timer4
  Functionality : Start timer 4
  Arguments   : None
  Return Value  : None
  Example Call  : start_timer4()
***********************************/
void start_timer4()
{
    TCCR4B = 0x04; // Prescaler 256 1-0-0
    TIMSK4 = 0x01; // Enable Timer Overflow Interrupt
}

ISR(TIMER4_OVF_vect)
{
    TCNT4 = 0xFB80;

    // Make a local copy of the global encoder count
    volatile double left_current_count = encoder_count;
    //     (Change in encoder count) * (60 sec/1 min)
    // RPM = __________________________________________
    //     (Change in time --> 20ms) * (PPR --> 840)
    RPM = (float)(((left_current_count - left_prev_count) * 60) / (0.02 * 420));

    // Store current encoder count for next iteration
    left_prev_count = left_current_count;
}

void setup()
{
    PID_Setup_Position();
    Motor_Setup();
    Serial.begin(115200);

    delay(5000);
    Serial.println("Starting now");
}

unsigned long last_time = 0;

void loop()
{
    if (millis() - last_time > 200) {
        last_time = millis();
        Serial.print(encoder_count);
        Serial.print('\t');
        Serial.print(output_pos);
        Serial.print('\t');
        Serial.print(abs(encoder_count + output_pos));
        Serial.print('\t');
        Serial.println(setpoint_pos);
    }
    PID_Loop();
}
