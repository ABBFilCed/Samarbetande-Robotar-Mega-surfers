String payload, readString;
float d, o; //error distance, omega
String ediString, omeString; // labels

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(50);
  ediString = "edi";
  omeString = "ome";
}

void loop(){
  while(Serial.available()){
    delay(0.05);
    String incomingValue = Serial.readString();
    Serial.println(incomingValue);
    
    if(ediString.compareTo(incomingValue.substring(0,3)) == 0){
      d = incomingValue.substring(4).toFloat();
    }
    
    else if(omeString.compareTo(incomingValue.substring(0,3)) == 0){
      o = incomingValue.substring(4).toFloat();
    }
    Serial.println(d);
    Serial.println(o);
  }
}

