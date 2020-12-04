#include <Wire.h>
#include <Servo.h>
#include "EspMQTTClient.h"

void onConnectionEstablished();

EspMQTTClient client(
 "ABB_Indgym_Guest",           // Wifi ssid
  "Welcome2abb",           // Wifi password
  "maqiatto.com",  // MQTT broker ip
  1883,             // MQTT broker port
  "jesper.jansson@abbindustrigymnasium.se",            // MQTT username
  "1234",       // MQTT password
  "jesper1",          // Client name
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
String ediString, omeString, prtString, legString; // labels
int pulses = 0;
float wheel_d = 3.6;
int prev_time = 0;
int prev_pulses = 0;
float o = 0;
float d = 0;
float x = 0;
float awmax = 180.0;
float yg = 0;
float aw = 0;
float av = 90;
float y = 0;
float v = 0;
float vg = 5.0;
float i = 0;
float oi = 0;
int dira = 0;
int last_millis;
int c_num;
float n = 0;
int lego = 0;

void onRecieve(){
  Serial.println("Message recieved");
}

void sendN(){
  String message = "1";
  Serial.println("Send to mqtt broker");
  client.publish("jesper.jansson@abbindustrigymnasium.se/ruta", message);
}

void onConnectionEstablished()
{
  client.subscribe("jesper.jansson@abbindustrigymnasium.se/ruta", [] (const String &payload)
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

auto Get_Xpos (int pulses, int* prev_pulses, float wheel_d, float* y, float* v, int* prev_time){
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

auto GoToGoal (float x, float y, float o, float awmax, float* av, float*aw){
  int og = 0;
  if (not x == 0) {
     int og = tan(y/x)*360/(2*3.14);
  }
  float kpv = 8;
  float kiv = 0.003;
  float kpw = 1;
  float vg = sqrt(sq(x)+sq(y));
  if (y < 0){
    vg = -1*vg;
  }
  i = i + vg;
  *av = (kpv*vg) + (kiv*i);
  int wg = (og-o);  
  /**aw = kpw*wg + 90;
  if ((*aw) > awmax){
    *av = 0;
    *aw = awmax;
  }*/
}

int FollowLine (float d, float awmax, float o, float* av, float* aw){
  float kpw = 0.6;
  float kpi = 0.00008;
  float og = -20.0*d;
  float delta_o = og-o;
  oi += delta_o;
  *aw = kpi*oi + kpw*(delta_o) + 90.0;
  if (*aw > awmax){
    *aw = awmax;
    *av = 0;
  }
  else if (*aw < 0){
    *aw = 0;
    *av = 0;
  }
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
  delay(10000);
}

void loop() {
  client.loop();
  Get_Xpos(pulses, &prev_pulses, wheel_d, &y, &v, &prev_time);
  float delta_y = yg - y;
  if (abs(delta_y) >= 0.2 or v > 0.5){
    GoToGoal(x, delta_y, o, awmax, &av, &aw);
    FollowLine(d, awmax, o, &av, &aw);
    //Serial.println(delta_y);
    //Serial.println(delta_y);
    if (av > 0){
      dira = 0;
    } else {
      dira = 1;
      av = -1*av;
    }
    Serial.println(aw); 
    myservo.write(aw);
    digitalWrite(DIRA, dira);
    analogWrite(PWMA, av+200.0);
  }
  else{
    analogWrite(PWMA, 0);
    /*if (int(n) % 2 == 0){
      if (lego) {
        delay(5000);
      }
    }*/
    FollowLine(d, awmax, o, &av, &aw);
    Serial.println("Halv ruta");
    myservo.write(aw);
    if (abs(o) < 3){
      if (n < 6){
        yg = 12.5;
        pulses = 0;
        n += 1;
        i = 0;
        oi = 0;
        sendN();
      }
      else {
        Serial.println("Done");
      }
    }
  }
  
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
    else if(legString.compareTo(incomingValue.substring(0,3)) == 0){
      lego = incomingValue.substring(4).toInt();
      Serial.println(lego);
    }
  }
  
 }

