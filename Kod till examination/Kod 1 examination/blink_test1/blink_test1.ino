int passeratEnRutaLed = 12; // lampa för antal rutor
int hittatHinderLed = 14; // lampa för hittat hinder

void setup() {
  pinMode(passeratEnRutaLed, OUTPUT);
  pinMode(hittatHinderLed, OUTPUT);
}

void loop() {
  digitalWrite(passeratEnRutaLed, HIGH);
  digitalWrite(hittatHinderLed, HIGH);
}
