String payload, readString;
int err, num, val;
String errString, numString, valString;

void setup() {
  Serial.begin(115200);
  Serial.setTimeout(100);
}

void loop(){
  
  while(Serial.available()){
    valString = "val";
    numString = "num";
    errString = "err";
    delay(1);
    String incomingValue = Serial.readString();
    Serial.println(incomingValue);
    
    if(valString.compareTo(incomingValue.substring(0,3)) = 0){
      val = incomingValue.substring(4);
    }
    
    if(errString.compareTo(incomingValue.substring(0,3)) = 0){
      err = incomingValue.substring(4);
    }
    
    if(numString.compareTo(incomingValue.substring(0,3)) = 0){
      num = incomingValue.substring(4);
    }
  }
}

