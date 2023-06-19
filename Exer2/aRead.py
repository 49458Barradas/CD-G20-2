import serial

###############################################################
# COM TÉCNICA FLETCHER SUM
###############################################################

porta_serial = "COM3"
ser = serial.Serial(porta_serial, 9600, timeout=1)

def main():
    stop = False
    while not stop:
        data = ""
        end = False
        while not end:
            temp = ser.read()
            if temp == "#":
                break
            if temp != ",":
                data+=temp
            if temp == ",":
                end = True
        print(data)
        if temp == "#":
            break


if __name__ == '__main__':
    main()