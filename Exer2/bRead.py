import serial

###############################################################
# COM TÉCNICA FLETCHER SUM
###############################################################

porta_serial = "COM3"
ser = serial.Serial(porta_serial, 9600, timeout=1)


def get_fletcher32(data: str):
    """
    Accepts a string as input.
    Returns the Fletcher32 checksum value in decimal and hexadecimal format.
    16-bit implementation (32-bit checksum)
    """
    sum1, sum2 = int(), int()
    data = data.encode()
    for index in range(len(data)):
        sum1 = (sum1 + data[index]) % 65535
        sum2 = (sum2 + sum1) % 65535
    result = (sum2 << 16) | sum1
    return result


def main():
    received_data = ""
    while len(received_data)!=6*16 + 32*6:
        temp = ser.read()
        if str(temp) != "b''":
            received_data += str(temp)[2]
    i = 0
    idx = 0
    data = []
    chks = []
    while i <= len(received_data) -1:
        data.append(received_data[i:i+16])
        chks.append(received_data[i+16:i+48])
        temp_checksum = get_fletcher32(data[idx])
        temp = int(chks[idx], 2)
        if temp_checksum != temp:
            print(f"Received checksum is {temp} but calculated was {temp_checksum}")
        idx += 1
        i += 48
    print(received_data)

if __name__ == '__main__':
    main()
