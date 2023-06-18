// VARIAVEIS DE INPUT DA FUNÇÃO DE PROGRESSAO GEOMETRICA
int n = 6;         // número de termos
int u = 2;         // primeiro termo
int r = 3;         // razão

int* termos;       // Ponteiro para armazenar os termos calculados

void setup() {
  Serial.begin(9600);
  termos = new int[n];
  checksums = new int[n];
}

void loop() {
  // Calcular os termos (32 bits)
  for (int i = 0; i < n; i++) {
    int termo = u;
    for (int j = 1; j <= i; j++) {
      termo *= r;
    }
    termos[i] = termo;
    Serial.print(termos[i]);
    Serial.print(",");
  }
  Serial.print("#");

  delay(1000);
}