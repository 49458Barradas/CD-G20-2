import random
import codecs

import numpy as np


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
'''
def binario_para_utf8(binario):
    bytes_utf8 = [binario[i:i+8] for i in range(0, len(binario), 8)]
    bytes_decimais = [int(byte, 2) for byte in bytes_utf8]
    utf8_bytes = bytes(bytes_decimais)
    utf8_string = utf8_bytes.decode('utf-8')
    return utf8_string
'''
def binario_para_utf8(binario):
    bytes_utf8 = [binario[i:i+8] for i in range(0, len(binario), 8)]
    bytes_decimais = [int(byte, 2) for byte in bytes_utf8]

    utf8_bytes = bytearray(bytes_decimais)
    try:
        utf8_string = utf8_bytes.decode('utf-8', errors='replace')
        return utf8_string
    except UnicodeDecodeError:
        print("Não foi possível decodificar a sequência binária como UTF-8.")
        return ""

def exeri(input, ber):
    #conversao para string binario
    binario = ""
    for caracter in input:
        valor_numerico = ord(caracter)
        binario += bin(valor_numerico)[2:].zfill(8)  # Adiciona zeros à esquerda se necessário

    if len(binario) % 8 != 0:
        binario = binario.zfill(
            (len(binario) // 8 + 1) * 8)  # Completa com zeros à esquerda se a sequência não for múltipla de 8
    #tecnica de repetição
    cod = ""
    for i in binario:
        cod += i
        cod += i
        cod += i
    #print(cod)
    #bsc
    bsc_val = bsc(cod, ber)
    #print(bsc_val)
    #decod
    decod = ""
    i = 0
    while(i != len(bsc_val)):
        ones = 0
        zeros = 0
        for v in range(i, i+2):
            if(bsc_val[v]=="1"):
                ones+=1
            else:
                zeros+=1
        if(zeros>ones):
            decod += "0"
        else:
            decod += "1"
        i += 3
    #MEDIÇÃO ERROS COMPARADO AO BER
    length = len(decod)
    count = 0
    for i in range(0, length):
        if binario[i] != decod[i]:
            count += 1
    new_ber = count/length
    print(f"Input Ber is {ber} and after method is {new_ber}")
    #bin to utf-8
    rtn = binario_para_utf8(decod)
    #print(rtn)

def exerii(input, ber):
    # conversao para string binario
    binario = ""
    for caracter in input:
        valor_numerico = ord(caracter)
        binario += bin(valor_numerico)[2:].zfill(8)  # Adiciona zeros à esquerda se necessário

    if len(binario) % 8 != 0:
        binario = binario.zfill(
            (len(binario) // 8 + 1) * 8)  # Completa com zeros à esquerda se a sequência não for múltipla de 8
    #print(binario)
    #H(7,4)
    temp = 0
    cod = ""
    while temp != len(binario):
        temp += 4
        if temp % 4 == 0:
            m0 = int(binario[temp-4])
            m1 = int(binario[temp-3])
            m2 = int(binario[temp-2])
            m3 = int(binario[temp-1])
            b0 = m1 ^ m2 ^ m3
            b1 = m0 ^ m1 ^ m3
            b2 = m0 ^ m2 ^ m3
            cod += str(m0) + str(m1) + str(m2) + str(m3) + str(b0) + str(b1) + str(b2)
    #print(cod)
    #bsc
    bsc_ret = bsc(cod, ber)
    #print(bsc_ret)
    #decod
    temp = 0
    decod = ""
    while temp != len(bsc_ret):
        temp += 7
        m3 = int(bsc_ret[temp - 4])
        m2 = int(bsc_ret[temp - 5])
        m1 = int(bsc_ret[temp - 6])
        m0 = int(bsc_ret[temp - 7])
        b0 = int(bsc_ret[temp-3])
        b1 = int(bsc_ret[temp-2])
        b2 = int(bsc_ret[temp-1])
        b0_recalc = m1 ^ m2 ^ m3
        b1_recalc = m0 ^ m1 ^ m3
        b2_recalc = m0 ^ m2 ^ m3
        sindroma = [None] * 3
        sindroma[2] = str(b2 ^ b2_recalc)
        sindroma[1] = str(b1 ^ b1_recalc)
        sindroma[0] = str(b0 ^ b0_recalc)
        sindroma = ''.join(sindroma)
        if sindroma == "011":
            if m0 == "0":
                m0 = 1
            else:
                m0 = "0"
            decod += str(m0) + str(m1) + str(m2) + str(m3)
        if sindroma == "110":
            if m1 == "0":
                m1 = 1
            else:
                m1 = "0"
            decod += str(m0) + str(m1) + str(m2) + str(m3)
        if sindroma == "101":
            if m2 == "0":
                m2 = 1
            else:
                m2 = "0"
            decod += str(m0) + str(m1) + str(m2) + str(m3)
        if sindroma == "111":
            if m3 == "0":
                m3 = 1
            else:
                m3 = "0"
            decod += str(m0) + str(m1) + str(m2) + str(m3)
    #print(sindroma)
    # bin to utf-8
    rtn = binario_para_utf8(decod)
    print(rtn)


def read_file(path_to_file):
    with open(path_to_file, 'r') as f:
        data = f.read()
        f.close()
    return data

def main():
    file_data = read_file("alice29.txt")
    #print(file_data)
    #exeri(file_data, 10 ** -1)
    #exeri(file_data, 10 ** -2)
    #exeri(file_data, 10 ** -3)
    #exeri(file_data, 10 ** -4)
    #exeri(file_data, 10 ** -5)
    exerii("a", 0)


if __name__ == '__main__':
    main()