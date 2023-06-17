import random


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

#Calcula BER
def BER(before, after):
    length = len(after)
    count = 0
    for i in range(0, length):
        if before[i] != after[i]:
            count += 1
    new_ber = count / length
    return new_ber

#Codificação de Hamming(7,4)
def codHamming74(binario):
    temp = 0
    cod = ""
    while temp != len(binario):
        temp += 4
        if temp % 4 == 0:
            m0 = int(binario[temp - 4])
            m1 = int(binario[temp - 3])
            m2 = int(binario[temp - 2])
            m3 = int(binario[temp - 1])
            b0 = m1 ^ m2 ^ m3
            b1 = m0 ^ m1 ^ m3
            b2 = m0 ^ m2 ^ m3
            cod += str(m0) + str(m1) + str(m2) + str(m3) + str(b0) + str(b1) + str(b2)
        else:
            # Lidar com os bits restantes que não formam um segmento completo de 4 bits
            # Caso não seja múltiplo de 4, você pode decidir como tratar esses bits extras.
            # Por exemplo, pode ignorá-los ou fazer algum tipo de preenchimento.
            print("CHEGUEI")
            pass
    return cod

#Descodificação de Hammington(7,4)
def decodHamming74(binario):
    temp = 0
    decod = ""
    while temp < len(binario):
        temp += 7
        m3 = int(binario[temp - 4])
        m2 = int(binario[temp - 5])
        m1 = int(binario[temp - 6])
        m0 = int(binario[temp - 7])
        b0 = int(binario[temp - 3])
        b1 = int(binario[temp - 2])
        b2 = int(binario[temp - 1])
        b0_recalc = m1 ^ m2 ^ m3
        b1_recalc = m0 ^ m1 ^ m3
        b2_recalc = m0 ^ m2 ^ m3
        sindroma = [None] * 3
        sindroma[2] = str(b2 ^ b2_recalc)
        sindroma[1] = str(b1 ^ b1_recalc)
        sindroma[0] = str(b0 ^ b0_recalc)
        sindroma = ''.join(sindroma)
        if sindroma == "011":
            if m0 == 0:
                m0 = 1
            else:
                m0 = 0
        if sindroma == "110":
            if m1 == 0:
                m1 = 1
            else:
                m1 = 0
        if sindroma == "101":
            if m2 == 0:
                m2 = 1
            else:
                m2 = "0"
        if sindroma == "111":
            if m3 == 0:
                m3 = 1
            else:
                m3 = 0
        decod += str(m0) + str(m1) + str(m2) + str(m3)
    return decod

# Compara dois Strings e retorna o número de Caractéres distintos entre os dois
def compareEqualStr(str1, str2):
    if len(str1) != len(str2):
        raise ValueError("Strings devem ter dimensões iguais")
    difs = 0
    for i in range(0, len(str2)-1):
        if str1[i] != str2[i]:
            difs += 1
    return difs

# Solução Exercicio
def a(ber):
    # Leitura
    readFile = read_file("alice29.txt")
    # Conversão
    binSeq = binConvert(readFile)
    # Codificação
    cod = codHamming74(binSeq)
    # BSC
    binSeqBSC = bsc(cod, ber)
    # Descodificação
    decod = decodHamming74(binSeqBSC)
    # Reconversão
    final = bin_to_string(decod)
    # Contagem de BER
    calc_ber = BER(binSeq, decod)
    # Numero total de bits que passam no BSC (one way)
    print(f"Número total de bits que passam no BSC (one way) é {len(binSeqBSC)}")
    # Apresentação de Resultados
    print(f"Given input BER was {ber} but calculated was {calc_ber}")
    # Numero de Símbolos diferentes nos transmitido e recebido
    symbDifs = compareEqualStr(readFile, final)
    print(f"Existem {symbDifs} símbolos diferentes entre ficheiro transmitido e recebido. \n")


def main():
    BER_TEST = [10**(-1), 10**(-2), 10**(-3), 10**(-4), 10**(-5)]
    for ber in BER_TEST:
        a(ber)


if __name__ == '__main__':
    main()
