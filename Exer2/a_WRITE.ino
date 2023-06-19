// VARIAVEIS DE INPUT DA FUNÇÃO DE PROGRESSAO GEOMETRICA
int n = 6;         // número de termos
int u = 2;         // primeiro termo
int r = 3;         // razão

int* termos;       // Ponteiro para armazenar os termos calculados

void setup() {
  Serial.begin(9600);
  termos = new int[n];
}

uint32_t get_fletcher32(const String& data) {
    uint32_t sum1 = 0xFFFF;
    uint32_t sum2 = 0xFFFF;

    for (int index = 0; index < data.length(); index++) {
        sum1 = (sum1 + data[index]) % 65535;
        sum2 = (sum2 + sum1) % 65535;
    }

    uint32_t result = (sum2 << 16) | sum1;
    return result;
}

void loop() {
  String send = "";
  String temp = "";
  int temp_len = 0;
  // Calcular os termos
  for (int i = 0; i < n; i++) {
    int termo = u;
    for (int j = 1; j <= i; j++) {
      termo *= r;
    }
    termos[i] = termo;
    temp = temp + termo + ",";
  }
  //agora separar 2 char dentro do string de cada vez
  for(int l=0; l<temp.length(); l = l + 2){
    String checksumInput = String(temp[l]) + String(temp[l+1]);
    uint32_t checksum = get_fletcher32(checksumInput);
    send = checksumInput + "_" + String(checksum) + "_";
    Serial.print(send);
  }
  Serial.print("#");

  delay(1000);
}
