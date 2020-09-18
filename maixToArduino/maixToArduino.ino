#define IN1 0
#define IN2 5

void setup() {
  pinMode(IN1, OUTPUT);
  pinMode(IN2, OUTPUT);
  Serial.begin(9600);
}

void loop() {
  digitalWrite(IN1, HIGH);
  analogWrite(IN2, 800);
}

