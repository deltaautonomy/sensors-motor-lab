#ifndef CONTROLLER_H_
#define CONTROLLER_H_

// Structure to handle the various outputs to the GUI
typedef struct TXDataPacket {
    // Boolean data
    bool button1;
    bool button2;
    bool slot_encoder;

    // Encoder data
    uint32_t encoder_count;
    float encoder_velocity;

    // Temperature sensor
    uint8_t temperature;

    // Sharp sensor
    uint16_t sharp_distance;

    // Ultrasonic sensor
    uint16_t ultrasonic_distance;

    // Filtered angles
    float pitch_angle;
    float roll_angle;
    float yaw_angle;

    // Raw accelerometer data
    uint16_t accel_x;
    uint16_t accel_y;
    uint16_t accel_z;

    // Raw gyroscope data
    uint16_t gyro_x;
    uint16_t gyro_y;
    uint16_t gyro_z;
} __attribute__((__packed__));

// Structure to handle the various inputs from the GUI
typedef struct RXDataPacket {
    // Enable for demo
    bool global_switch;

    // State select
    uint8_t state;

    // Input servo angle
    uint8_t servo_angle;

    // Input servo angle
    uint16_t motor_angle;

    // DC motor PID gains
    float motor_kp;
    float motor_ki;
    float motor_kd;
} __attribute__((__packed__));

extern TXDataPacket tx_packet;
extern RXDataPacket rx_packet;

#endif
