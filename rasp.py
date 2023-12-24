import serial
import time

def main():
    ser = serial.Serial('/dev/ttyUSB0', 9600, timeout=1)
    time.sleep(3)
    ser.reset_input_buffer()
    print("SERIAL OK")

    while True:
        time.sleep(0.01)
        if ser.in_waiting > 0:
            line = ser.readline().decode('utf-8').rstrip()
            print(line)

if __name__ == "__main__":
    main()