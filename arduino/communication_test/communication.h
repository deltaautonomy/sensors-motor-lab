#include <Arduino.h>
#include <stdint.h>

#ifndef CONTROLLER_H_
#define CONTROLLER_H_

// Structure to handle the various outputs to the GUI
typedef struct TXDataPacket {
    // Boolean data
    uint8_t button1;
    uint8_t button2;
    uint8_t slot_encoder;

    // Encoder data
    int32_t encoder_count;
    float encoder_velocity;

    // Temperature sensor
    uint8_t temperature;

    // Sharp sensor
    uint16_t sharp_distance;

    // Ultrasonic sensor
    uint16_t ultrasonic_distance;

    // Flex sensor
    uint16_t flex_sensor;

    // Filtered angles
    float roll_angle;
    float pitch_angle;
    float yaw_angle;

    // Raw accelerometer data
    uint16_t accel_x;
    uint16_t accel_y;
    uint16_t accel_z;

    // Raw gyroscope data
    uint16_t gyro_x;
    uint16_t gyro_y;
    uint16_t gyro_z;

    // Ouput servo angle
    uint8_t servo_angle;
} __attribute__((__packed__));

// Structure to handle the various inputs from the GUI
typedef struct RXDataPacket {
    // Enable for demo
    uint8_t global_switch;

    // State select
    uint8_t state;

    // Input servo angle
    uint8_t servo_angle;

    // Input motor angle
    uint16_t motor_angle;

    // DC motor PID gains
    float motor_kp;
    float motor_ki;
    float motor_kd;
} __attribute__((__packed__));

extern TXDataPacket tx_packet;
extern RXDataPacket rx_packet;

void send_data();
bool recieve_data();
void clear_buffer();

#endif
