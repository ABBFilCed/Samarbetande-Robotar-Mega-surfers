String payload,incomingValue, readString;
float d, o; //error distance, omega
String part;
String ediString, omeString, prtString; // labels

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(50);
  ediString = "edi";
  omeString = "ome";
  prtString = "prt";
}

void loop(){
  while(Serial.available()){
    delay(0.05);
    incomingValue = Serial.readString();
    //Serial.println(incomingValue);
    
    if(ediString.compareTo(incomingValue.substring(0,3)) == 0){
      d = incomingValue.substring(4).toFloat();
      Serial.println(d);
    }
    
    else if(omeString.compareTo(incomingValue.substring(0,3)) == 0){
      o = incomingValue.substring(4).toFloat();
      Serial.println(o);
    }

    else if(prtString.compareTo(incomingValue.substring(0,3)) == 0){
      part = incomingValue.substring(4);
      Serial.println(part);
    }
  }
}

