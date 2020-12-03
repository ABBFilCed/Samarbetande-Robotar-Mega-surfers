#include <Wire.h>
#include <Servo.h>
#include "EspMQTTClient.h"

EspMQTTClient client(
 "ABB_Indgym_Guest",           // Wifi ssid
  "Welcome2abb",           // Wifi password
  "maqiatto.com",  // MQTT broker ip
  1883,             // MQTT broker port
  "jesper.jansson@abbindustrigymnasium.se",            // MQTT username
  "1234",       // MQTT password
  "jesper",          // Client name
  onConnectionEstablished, // Connection established callback
  true,             // Enable web updater
  true              // Enable debug messages
);

#define DIRA 0 //Motor direction
#define PWMA 5 //Motor pwm
#define HALL 12
#define IN1 0
#define IN2 5

Servo myservo;

String payload, incomingValue, readString;
String part;
String ediString, omeString, prtString; // labels
int pulses = 0;
float wheel_d = 3.6;
int prev_time = 0;
int prev_pulses = 0;
float o = 0;
float d = 0;
float x = 0;
float awmax = 180.0;
float yg = 51;
float aw = 0;
float av = 90;
float y = 0;
float v = 0;
float vg = 5.0;
float i = 0;
int dira = 0;
int last_millis;
int c_num;

void onRecieve(){
  r_direction = payload.toInt();
  Serial.write(1);
  wait_msg = true;
  message = "[" + String(r_direction) + ", " + part + "]";
  client.publish("jesper.jansson@abbindustrigymnasium.se/map", message);
}

auto sendPwm(av, aw){
  message = "[" + String(av) + ", " + String(aw) + "]";
  client.publish("jesper.jansson@abbindustrigymnasium.se/pwm", message);
}

void onConnectionEstablished()
{
  client.subscribe("jesper.jansson@abbindustrigymnasium.se/robot1", [] (const String &payload)
  {
    onRecieve();
  });
}


void Increase_pulses(){
  if (dira) {
   pulses -= 1;
  }
  else {
  pulses += 1; //Increases pulses everytime the digital input 12 goes from HIGH to LOW
  //Serial.println(pulses);
  }
}

auto Get_X (int pulses, int* prev_pulses, float wheel_d, float* y, float* v, int* prev_time){
  noInterrupts();//No interupts during the calculations
  int current_time = millis();
  int time_diff = (current_time - *prev_time); //Time since last calculation
  int varv_diff = (pulses - *prev_pulses); //Pulses sice last calculation 
  float rpm = (float(varv_diff)/float(time_diff))*60000/96; // pulse per millisecond multiplied with milliseconds per minute and 1:48 gear ratio
  *v = (rpm/60)*(3.14*wheel_d);
  *y = (float(pulses)/140)*(3.14*wheel_d);
  *prev_pulses = pulses; 
  *prev_time = current_time;
  //*o += aw*time_diff
  interrupts(); 
}

auto GtG (float x, float y, float o, float awmax, float* av, float*aw){
  int og = 0;
  if (not x == 0) {
     int og = tan(y/x)*360/(2*3.14);
  }
  float kpv = 6;
  float kiv = 0.0005;
  float kpw = 1;
  float vg = sqrt(sq(x)+sq(y));
  if (y < 0){
    vg = -1*vg;
  }
  i = i + vg;
  *av = (kpv*vg) + (kiv*i);
  int wg = (og-o);  
  *aw = kpw*wg + 90;
  if ((*aw) > awmax){
    *av = 0;
    *aw = awmax;
  }
}

int CC (float vg, float v, float* av){
  float e = vg - v;
  float kpv = 100.0;
  *av = kpv*e;
}

int FL (float d, float awmax, float o, float* av, float* aw){
  float kpw = 10;
  float og = -30.0*d;
  float delta_o = og-o;
  *aw = kpw*(delta_o) + 90.0;
  if (*aw > awmax){
    *aw = awmax;
    *av = 0;
  }
  else if (*aw < 0){
    *aw = 0;
    *av = 0;
  }
}

int AO (float s){
  float kpv = 1;
  float av = kpv*(-s);
  return av;
}

int RC (int og){
  return og;
}

void setup() {
  pinMode(DIRA, OUTPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(HALL, INPUT);
  myservo.attach(14);
  Serial.begin(115200);
  digitalWrite(DIRA, 1);
  Serial.setTimeout(50);
  attachInterrupt(digitalPinToInterrupt(HALL), Increase_pulses, FALLING);
  last_millis = millis();
  ediString = "edi";
  omeString = "ome";
  prtString = "prt";
  myservo.write(90);
  delay(5000);
  client.publish("jesper.jansson@abbindustrigymnasium.se/pwm", "Robot connected!");
}

void loop() {
  client.loop();
  Get_X(pulses, &prev_pulses, wheel_d, &y, &v, &prev_time);
  float delta_y = yg - y;
  if (abs(delta_y) >= 0.5 or v > 1){
    GtG(x, delta_y, o, awmax, &av, &aw);
    aw = 90;
    //Serial.println(delta_y);
    //Serial.println(delta_y);
    FL(d, awmax, o, &av, &aw);
    if (av > 0){
      dira = 0;
    } else {
      dira = 1;
      av = -1*av;
    }
    /*if (o > 5 or d > 0.5){
      FL(d, awmax, o, &av, &aw);
    }
    myservo.write(aw);*/
    Serial.println(aw); 
    digitalWrite(DIRA, dira);
    analogWrite(PWMA, av+200.0);
    myservo.write(aw);
    sendPwm(av, aw);
  }
  else{
    analogWrite(PWMA, 0);
    Serial.println("Done");
    myservo.write(90);
    client.publish("jesper.jansson@abbindustrigymnasium.se/pwm", "Done");
  }

  
  /*
  else{
    analogWrite(PWMA, 0);
    Serial.println("Done");
  }*/
  if(Serial.available()){
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
  /*Serial.println(Serial.available());
  if ((millis() - last_millis) > 100 and Serial.available()){
      String mess = Serial.readString();
      Serial.println("Reading from UART");
      Serial.println(mess);
      for (int i; i < mess.length(); i++) {
        char c = mess[i];
        if (String(c) == ",") {
          c_num = i;
        }
      }
      d = mess.substring(0, c_num).toFloat();
      o = mess.substring(c_num+1).toFloat();
      Serial.println(d, o);
      last_millis = millis();
    }*/
 }

