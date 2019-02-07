#include "communication.h"

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

    // Update checksum
    checksum = code ^ size;

    // Send byte array and update checksum
    for (int i = 0; i < size; i++) {
        Serial.write(data[i]);
        checksum ^= data[i];
    }

    // Send checksum
    Serial.write(checksum);
}

bool recieve_data()
{
    // Packet metadata
    uint8_t size = sizeof(RXDataPacket);
    uint8_t checksum = 0;

    // Payload buffer
    uint8_t buff[size];

    // Check (frame + header) length
    if (Serial.available() >= size + 3) {

        // Check header of data frame
        if (Serial.read() != '$')
            return false;
        if (Serial.read() != '<')
            return false;

        for (int i = 0; i < size; i++) {
            buff[i] = Serial.read();
            checksum ^= buff[i];
        }
    }

    // Discard frame if checksum does not match
    if (Serial.read() != checksum)
        return false;

    // Convert bytes to struct
    memcpy(&rx_packet, buff, size);

    // Success
    return true;
}
