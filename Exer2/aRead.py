import serial

###############################################################
# COM TÉCNICA FLETCHER SUM
###############################################################

porta_serial = "COM3"
ser = serial.Serial(porta_serial, 9600, timeout=1)

def main():
    bits = ""
    segmentos = []
    checksum = None
    termo = None

    while True:
        dado = ser.read().decode()  # Lê um byte enviado pelo Arduino
        if dado:
            if dado.isdigit():
                bits += dado
                if len(bits) == 32:
                    segmento = int(bits, 2)
                    verificarSegmento(segmento, segmentos)
                    segmentos.append(segmento)
                    bits = ""
            elif dado == "#":  # Caractere especial para indicar o fim da sequência
                if len(segmentos) < 2:
                    print("Erro: segmentos insuficientes para o checksum.")
                    break
                checksum = segmentos.pop()  # Remove o último segmento da lista para obter o checksum
                termo = segmentos.pop()  # Remove o segmento anterior para obter o termo
                if verificarChecksum(segmentos, termo, checksum):
                    print("Verificação de erros bem-sucedida. Fletcher checksum é válido.")
                else:
                    print("Erro detectado. Fletcher checksum inválido.")
                break

    if termo is not None:
        print(f"Termo recebido: {termo}")
    if checksum is not None:
        print(f"Checksum recebido: {checksum}")
    print("Segmentos recebidos:")
    for segmento in segmentos:
        print(segmento)


def verificarSegmento(segmento, segmentos):
    termo = segmento >> 16
    checksum = segmento & 0xFFFF
    checksum_calculado = calcularChecksum(segmentos, termo)
    if checksum_calculado == checksum:
        print(f"Verificação de erros bem-sucedida. Segmento: {segmento}")
    else:
        print(f"Erro detectado. Segmento: {segmento}")


def verificarChecksum(segmentos, termo, checksum):
    checksum_calculado = calcularChecksum(segmentos, termo)
    return checksum_calculado == checksum


def calcularChecksum(segmentos, termo):
    sum1 = 0xFFFF
    sum2 = 0xFFFF

    for segmento in segmentos:
        sum1 = (sum1 + segmento) % 65535
        sum2 = (sum2 + sum1) % 65535

    sum1 = (sum1 + termo) % 65535
    sum2 = (sum2 + sum1) % 65535

    return (sum2 << 16) | sum1


if __name__ == '__main__':
    main()
