#include "communication.h"

TXDataPacket tx_packet;
RXDataPacket rx_packet;

void send_data()
{
    // Packet metadata
    uint8_t size = sizeof(TXDataPacket);
    uint8_t checksum = 0;

    // Payload buffer
    uint8_t buff[size];

    // Convert struct to bytes
    memcpy(buff, &tx_packet, size);

    // Send header
    Serial.print("$>");

    // Send data length
    Serial.write(size);

    // Send byte array and update checksum
    for (int i = 0; i < size; i++) {
        Serial.write(buff[i]);
        checksum ^= buff[i];
    }

    // Send checksum
    Serial.write(checksum);
}

void clear_buffer()
{
    while (Serial.available()) {
        Serial.read();
        Serial.flush();
    }
}

int recieve_data()
{
    // Packet metadata
    uint8_t size = sizeof(RXDataPacket);
    uint8_t checksum = 0;

    // Payload buffer
    uint8_t buff[size];

    // Check (frame + header) length
    if (Serial.available() >= size + 4) {

        Serial.println("Here");
        Serial.println(Serial.read());

        // Check header of data frame
        if (Serial.read() != '$') {
            Serial.println("\n$ failed");
            clear_buffer();
            return 4;
        }
        if (Serial.read() != '<') {
            Serial.println("\n< failed");
            clear_buffer();
            return 5;
        }

        // Data length byte
        Serial.read();

        // Read data bytes
        for (int i = 0; i < size; i++) {
            buff[i] = Serial.read();
            checksum ^= buff[i];
        }

        // Discard frame if checksum does not match
        if (Serial.read() != checksum) {
            Serial.println("Checksum failed");
            Serial.println(checksum);
            clear_buffer();
            return 6;
        }

        // Convert bytes to struct
        memcpy(&rx_packet, buff, size);

        // Success
        clear_buffer();
        return 7;
    }

    clear_buffer();
    return 2;
}
