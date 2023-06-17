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


# Converte string binario para string
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
    if len(str1) != len(str2):
        raise ValueError("Strings devem ter dimensões iguais")
    difs = 0
    for i in range(0, len(str1)):
        if str1[i] != str2[i]:
            difs += 1
    return difs


# Função de Interleaving
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
# Codificador de Código de repetição(3,1)
def codRep31(input):
    # tecnica de repetição
    cod = ""
    for i in input:
        cod += i
        cod += i
        cod += i
    return cod

# Descodificador de Código de repetição(3,1)
def decodRep31(input):
    decod = ""
    i = 0
    while i < len(input) - 2:
        ones = 0
        zeros = 0
        for v in range(i, i + 2):
            if input[v] == "1":
                ones += 1
            else:
                zeros += 1
        if zeros > ones:
            decod += "0"
        else:
            decod += "1"
        i += 3
    return decod

# Solução Exercicio
def b(ber):
    # Leitura
    readFile = read_file("alice29.txt")
    # Interleaving
    interleaved = interleaving(readFile)
    # Conversão
    binSeq = binConvert(interleaved)
    # Codificação
    cod = codRep31(binSeq)
    # BSC
    binSeqBSC = bsc(cod, ber)
    # Descodificação
    decod = decodRep31(binSeqBSC)
    # Reconversão
    final = bin_to_string(decod)
    # desinterleaving
    deinterleaved = deinterleaving(final)
    # Contagem de BER
    calc_ber = BER(binSeq, binSeq)
    # Numero total de bits que passam no BSC (one way)
    print(f"Número total de bits que passam no BSC (one way) é {len(binSeqBSC)}")
    # Comparação de BER's
    print(f"Given input BER was {ber} but calculated was {calc_ber}")
    # Numero de Símbolos diferentes nos transmitido e recebido
    symbDifs = compareEqualStr(readFile, deinterleaved)
    print(f"Existem {symbDifs} símbolos diferentes entre ficheiro transmitido e recebido. \n")


def main():
    BER_TEST = [10 ** (-1), 10 ** (-2), 10 ** (-3), 10 ** (-4), 10 ** (-5)]
    for ber in BER_TEST:
        b(ber)


if __name__ == '__main__':
    main()
