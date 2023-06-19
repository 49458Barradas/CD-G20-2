import serial

###############################################################
# COM TÉCNICA FLETCHER SUM
###############################################################

porta_serial = "COM3"
ser = serial.Serial(porta_serial, 9600, timeout=1)


def get_fletcher32(data):
    """
    Accepts a string as input.
    Returns the Fletcher32 checksum value as an integer.
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
    while True:
        temp = ser.read().decode('utf-8')
        if temp == "#":
            received_data += temp
            break
        else:
            received_data += temp
    #received_data aqui deve ser igual a "2,_16580861_6,_17105153_18_458760_,5_33161472_4,_16843007_16_327686_2,_16580861_48_851979_6,_17105153_"
    checks = []
    temp = received_data.split("_")
    for i in range(1, len(temp), 2):
        checks.append(temp[i])
    received_data_no_chksum = ""
    i = 0
    chk = False
    while i < len(received_data):
        if i < len(received_data) and not chk and received_data[i] == "_":
            chk = True
            i += 1
        if i < len(received_data) and chk and received_data[i] == "_":
            chk = False
            i += 1
        if i < len(received_data) and not chk and received_data[i] != "_":
            received_data_no_chksum += received_data[i]
            i += 1
        if i < len(received_data) and chk and received_data[i] != "_":
            i += 1
    received_data_no_chksum = received_data_no_chksum[:-1]
    calc_cheks = []
    i = 0
    while i < len(received_data_no_chksum):
        temp = received_data_no_chksum[i] + received_data_no_chksum[i+1]
        chksc = get_fletcher32(temp)
        calc_cheks.append(chksc)
        i += 2



if __name__ == '__main__':
    main()
