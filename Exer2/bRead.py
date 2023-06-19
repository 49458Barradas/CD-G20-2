import random

import serial

###############################################################
# COM TÉCNICA FLETCHER SUM
###############################################################

porta_serial = "COM3"
ser = serial.Serial(porta_serial, 9600, timeout=1)


# Fletcher baseado na biblioteca fornecida no enunciado
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


def bsc(binSeq, BER):
    seqL = len(str(binSeq))
    p = BER
    output = []
    for i in range(seqL):
        temp = random.random()
        if temp < p:
            if binSeq[i] == '1':
                output.append('0')
            else:
                output.append('1')
        else:
            output.append(binSeq[i])
    return ''.join(output)


def main():
    ber = 0.01
    # RECEBER DATA
    received_data = ""
    while len(received_data) != 6 * 16 + 32 * 6:
        temp = ser.read()
        if str(temp) != "b''":
            received_data += str(temp)[2]
    # SIMULAÇÃO ERRO ALEATORIO
    binSeqBSC = bsc(received_data, ber)
    # SIMULAÇÃO DE RECEÇÃO DE DATA SEGUIDA DE COMPARAÇÃO CHECKSUM
    i = 0
    idx = 0
    data = []
    chks = []
    while i <= len(binSeqBSC) - 1:
        data.append(binSeqBSC[i:i + 16])
        chks.append(binSeqBSC[i + 16:i + 48])
        temp_checksum = get_fletcher32(data[idx])
        temp = int(chks[idx], 2)
        # QUANDO DETETADO ERRO É ABORTADA A TRANSMISSÃO
        if temp_checksum != temp:
            print(f"Received checksum is {temp} but calculated was {temp_checksum}")
            #break
        idx += 1
        i += 48



if __name__ == '__main__':
    main()
