String payload, readString;

void setup() {
  Serial.begin(115200);
}

void loop(){
  while(Serial.available()){
    delay(1);
    char c = Serial.read();
    payload += c;
    if(payload.length() > 4){
      Serial.println(payload);
      payload = "";
    }
  }
}

