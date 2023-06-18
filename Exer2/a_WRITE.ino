// VARIAVEIS DE INPUT DA FUNÇÃO DE PROGRESSAO GEOMETRICA
int n = 6; // número de termos
int u = 2;  // primeiro termo
int r = 3;  // razão

void setup() {
  Serial.begin(9600);
}

void loop() {
  // Função de progressão geométrica
  for (int i = 0; i < n; i++) {
    int termo = u;
    for (int j = 1; j <= i; j++) {
      termo *= r;
    }
    enviarBits(termo);
    delay(500);
  }

  // Envia o Fletcher checksum
  uint32_t checksum = calcularChecksum();
  enviarBits(checksum); // Envia o checksum em bits para o PC
  delay(500);          // Aguarda 500 milissegundos antes de enviar o fim da sequência
  enviarFimSequencia();  // Envia o fim da sequência
  delay(500);
}

void enviarBits(uint32_t numero) {
  for (int i = 31; i >= 0; i--) {
    int bit = (numero >> i) & 1;
    Serial.print(bit);
  }
  Serial.println(); // Imprime uma nova linha após enviar todos os bits
}

uint32_t calcularChecksum() {
  uint32_t sum1 = 0xFFFF;
  uint32_t sum2 = 0xFFFF;

  for (int i = 0; i < n; i++) {
    int termo = u;
    for (int j = 1; j <= i; j++) {
      termo *= r;
    }
    sum1 = (sum1 + termo) % 65535;
    sum2 = (sum2 + sum1) % 65535;
  }

  return (sum2 << 16) | sum1;
}

void enviarFimSequencia() {
  Serial.println("#"); // Caractere especial para indicar o fim da sequência
}