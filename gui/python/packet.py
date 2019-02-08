import time
import serial
import struct
import traceback


class Packet:
    def __init__(self):
        # TX data
        self.tx_button1 = False
        self.tx_button2 = False
        self.tx_slot_encoder = False

        self.tx_encoder = {'encoder_count': 0, 'encoder_velocity': 0}
        self.tx_temperature = 0
        self.tx_sharp_distance = 0
        self.tx_ultrasonic_distance = 0

        self.tx_angles = {'pitch': 0, 'roll': 0, 'yaw': 0}
        self.tx_accel = {'x': 0, 'y': 0, 'z': 0}
        self.tx_gyro = {'x': 0, 'y': 0, 'z': 0}

        # RX data
        self.rx_global_switch = False
        self.rx_state = 0
        self.rx_servo_angle = 0
        self.rx_motor_angle = 0
        self.rx_motor_PID = {'kp': 0, 'ki': 0, 'kd': 0}

    def start(self, com_port, baud=115200, timeout=0):
        # Configure serial port
        self.ser = serial.Serial()
        self.ser.port = com_port
        self.ser.baudrate = baud
        self.ser.timeout = timeout

        # Time to wait until the board becomes operational
        wakeup = 2
        try:
            self.ser.open()
            print("\n>>> Opening COM Port: " + self.ser.port)
            for i in range(1, wakeup):
                time.sleep(1)
        except Exception as error:
            traceback.print_tb(error.__traceback__)
            self.ser.close()

        # Clear buffer
        self.ser.flushInput()
        self.ser.flushOutput()

    def close(self):
        self.ser.close()

    def generate_frame(self, data, data_format, mode):
        checksum = 0
        frame = ''
        direc = {'tx': '<', 'rx': '>'}

        # Pack data into bytes
        header = struct.pack('cc', '$', direc[mode])
        payload = struct.pack(data_format, *data)
        data_length = struct.pack('B', len(payload))

        # Calculate checksum
        for byte in payload:
            checksum ^= ord(byte)
        checksum = struct.pack('B', checksum)

        # Complete frame
        frame = header + payload + checksum
        return frame

    def send(self, data, data_format, mode='tx'):
        # Make frame
        tx_frame = self.generateFrame(data, data_format, mode)

        # Send data
        try:
            self.ser.write(tx_frame)
            return tx_frame

        except Exception as error:
            traceback.print_tb(error.__traceback__)

    def recieve(self, data_format, data_length):
        checksum = 0
        calcsum = 0
        payload = ''
        rx_data = []

        # Recieve data
        try:
            if self.ser.inWaiting() >= (data_length + 4):
                # Verify header
                if self.ser.read(1).decode('utf-8') != '$':
                    # print('Header failed $')
                    return None
                if self.ser.read(1).decode('utf-8') != '>':
                    # print('Header failed >')
                    return None

                # Verify data length
                data = int(ord(self.ser.read(1).decode('utf-8')))
                if data != data_length:
                    # print('Data length failed')
                    return None

                payload = self.ser.read(data_length)
                checksum = self.ser.read(1)

                # Clear buffer
                self.ser.flushInput()
                self.ser.flushOutput()

                # Verify checksum
                for byte in payload:
                    calcsum ^= byte
                if calcsum != ord(checksum):
                    # print('Checksum failed')
                    # print(calcsum, checksum)
                    return None

                # Unpack data
                rx_data = list(struct.unpack(data_format, payload))
                return rx_data

        except Exception as error:
            traceback.print_tb(error.__traceback__)

        # Clear buffer
        self.ser.flushInput()
        self.ser.flushOutput()

        return None

    def recieve_blocking(self, delay=2):
        data = None
        while not data:
            time.sleep(delay)
            data = self.recieve('<BBBifBHHfffHHHHHH', 40)

        self.parse_data(data)
        self.display()

    def parse_data(self, data):
        # Boolean data
        self.tx_button1 = bool(data[0])
        self.tx_button2 = bool(data[1])
        self.tx_slot_encoder = bool(data[2])

        # Encoder data
        self.tx_encoder['encoder_count'] = data[3]
        self.tx_encoder['encoder_velocity'] = data[4]

        # Sensors data
        self.tx_temperature = data[5]
        self.tx_sharp_distance = data[6]
        self.tx_ultrasonic_distance = data[7]

        # Filtered angles
        self.tx_angles['roll'] = data[8]
        self.tx_angles['pitch'] = data[9]
        self.tx_angles['yaw'] = data[10]

        # Raw accelerometer data
        self.tx_accel['x'] = data[11]
        self.tx_accel['y'] = data[12]
        self.tx_accel['z'] = data[13]

        # Raw gyroscope data
        self.tx_gyro['x'] = data[14]
        self.tx_gyro['y'] = data[15]
        self.tx_gyro['z'] = data[16]

    def display(self):
        print('tx_button1:', self.tx_button1)
        print('tx_button2:', self.tx_button2)
        print('tx_slot_encoder:', self.tx_slot_encoder)
        print('tx_encoder:', self.tx_encoder)
        print('tx_temperature:', self.tx_temperature)
        print('tx_sharp_distance:', self.tx_sharp_distance)
        print('tx_ultrasonic_distance:', self.tx_ultrasonic_distance)
        print('tx_angles:', self.tx_angles)
        print('tx_accel:', self.tx_accel)
        print('tx_gyro:', self.tx_gyro)


if __name__ == '__main__':
    packet = Packet()
    packet.start('/dev/ttyACM0')

    while True:
        packet.recieve_blocking()
