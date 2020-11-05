String payload, readString;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(100);
}

void loop(){
  while(Serial.available()){
    delay(1);
    String err = Serial.readString();
    Serial.println(err);
    /*
    char c = Serial.read();
    payload += c;
    if(payload.length() > 4){
      Serial.println(payload);
      payload = "";*/
  }
}


