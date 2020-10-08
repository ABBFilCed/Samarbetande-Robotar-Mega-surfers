#define IN1 0
#define IN2 5

void setup() {

  Serial.begin(9600);
}

void loop() {
  while (Serial.available()) {​​​​
    delay(1);
    char c = Serial.read();
    payload += c;
    Serial.println(String(payload))
  }​​​​
}

