import random
import numpy as np


###############################################################
# PARA LEITURA COM FICHEIRO
###############################################################

# Binary Simetric Channel
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


# File to String
def read_file(path_to_file):
    with open(path_to_file, 'r') as f:
        data = f.read()
        f.close()
    return data


# Escreve o ficheiro de output (transmitido)
def write_file(path_to_file, content, encoding='utf-8'):
    with open(path_to_file, 'w', encoding=encoding) as f:
        f.write(content)
        f.close()


# Conversão para String sobre forma binária
def binConvert(strng):
    binario = ""
    for caracter in strng:
        valor_numerico = ord(caracter)
        binario += bin(valor_numerico)[2:].zfill(8)  # Adiciona zeros à esquerda se necessário

    if len(binario) % 8 != 0:
        binario = binario.zfill(
            (len(binario) // 8 + 1) * 8)  # Completa com zeros à esquerda se a sequência não for múltipla de 8
    return binario

# Separa o string de binario em array de bytes de string
def dividir_string(string, tamanho):
    array = []
    for i in range(0, len(string), tamanho):
        parte = string[i:i + tamanho]
        array.append(parte)
    return array

# Conversão de binário para string
def bin_to_string(strng):
    binary = ""
    new_str = dividir_string(strng, 8)
    for i in new_str:
        decimal_number = int(i, 2)
        utf8_character = chr(decimal_number)
        binary += utf8_character
    return binary

# Calcula BER
def BER(before, after):
    length = len(after)
    count = 0
    for i in range(0, length):
        if before[i] != after[i]:
            count += 1
    new_ber = count / length
    return new_ber


# Compara dois Strings e retorna o número de Caractéres distintos entre os dois
def compareEqualStr(str1, str2):
    #VAI RECEBER CADA STRING, REALIZAR CONTAGEM DE FREQUENCIAS E PRONTO APRESENTAR SOBRE FORMA GRAFICA


# Função de Interleaving
def interleaving(str):
    length = len(str)
    mV = int(np.ceil(np.sqrt(length)))
    mtxDim = (mV ** 2)
    extra = mtxDim - length
    mtx = list(str)
    while extra > 0:
        mtx.append('ý')
        extra -= 1
    matrix = np.empty((mV, mV), dtype='U1')
    for i in range(len(mtx)):
        row = i // mV
        col = i % mV
        matrix[row, col] = mtx[i]
    matrix = matrix.T
    lst = []
    for i in range(mtxDim):
        rows = i // mV
        cols = i % mV
        lst.append(matrix[rows, cols])
    return "".join(lst)

# Função de Interleaving
def deinterleaving(str):
    length = len(str)
    mV = int(np.ceil(np.sqrt(length)))
    mtxDim = (mV ** 2)
    mtx = list(str)
    matrix = np.empty((mV, mV), dtype='U1')
    for i in range(len(mtx)):
        row = i // mV
        col = i % mV
        matrix[row, col] = mtx[i]
    matrix = matrix.T
    lst = []
    for i in range(mtxDim):
        rows = i // mV
        cols = i % mV
        if matrix[rows, cols] != 'ý':
            lst.append(matrix[rows, cols])
    return "".join(lst)


# Solução Exercicio
def b(ber):
    # Leitura
    readFile = read_file("alice29.txt")
    # Interleaving
    interleaved = interleaving(readFile)
    # Conversão
    binSeq = binConvert(interleaved)
    # BSC
    binSeqBSC = bsc(binSeq, ber)
    # Reconversão
    final = bin_to_string(binSeqBSC)
    # desinterleaving
    deinterleaved = deinterleaving(final)
    # Contagem de BER
    calc_ber = BER(binSeq, binSeqBSC)
    # Numero total de bits que passam no BSC (one way)
    print(f"Número total de bits que passam no BSC (one way) é {len(binSeqBSC)}")
    # Comparação de BER's
    print(f"Given input BER was {ber} but calculated was {calc_ber}")
    # Numero de Símbolos diferentes nos transmitido e recebido
    symbDifs = compareEqualStr(readFile, deinterleaved)
    print(f"Existem {symbDifs} símbolos diferentes entre ficheiro transmitido e recebido. \n")


def main():
    BER_TEST = [10 ** (-1), 10 ** (-2), 10 ** (-3), 10 ** (-4), 10 ** (-5)]
    #for ber in BER_TEST:
        #b(ber)
    b(0.01)

if __name__ == '__main__':
    main()
