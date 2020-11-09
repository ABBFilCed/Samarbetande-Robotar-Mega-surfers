String payload, readString;
String err;
String num;
String val;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(100);
}

void loop(){
  while(Serial.available()){
    delay(1);
    String incomingValue = Serial.readString();
    Serial.println(incomingValue);
    if(val.compareTo(incomingValue.substring(0,3)) = 0){
      val = incomingValue.substring(4);
    }
    
    if(err.compareTo(incomingValue.substring(0,3)) = 0){
      err = incomingValue.substring(4);
    }
    
    if(num.compareTo(incomingValue.substring(0,3)) = 0){
      num = incomingValue.substring(4);
    }
  }
}

