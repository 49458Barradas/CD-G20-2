import serial
import time

serialcomm = serial.Serial('COM3', 9600)
serialcomm.timeout = 1

while True:
    i = input("input(on/off): ").strip()
    if i == "done":
        break
    serialcomm.write(i.encode() + b'\n')
    time.sleep(1)
    print(serialcomm.readline().decode('ascii'))

serialcomm.close()