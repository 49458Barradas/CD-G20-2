import serial

porta_serial = "COM3"

ser = serial.Serial(porta_serial)

if not ser.isOpen():
    ser.open()


def main():
    while True:
        linha = ser.read().strip().decode('utf-8')
        if linha:
            print(f"Dado recebido: {linha}")

if __name__ == '__main__':
    main()