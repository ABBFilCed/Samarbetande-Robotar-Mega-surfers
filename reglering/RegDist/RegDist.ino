#include <Wire.h>
#include <Servo.h>

#define DIRA 0 //Motor direction
#define PWMA 5 //Motor pwm
#define HALL 12
#define IN1 0
#define IN2 5

Servo myservo;

String payload, readString;
int pulses = 0;
float wheel_d = 3.6;
int prev_time = 0;
int prev_pulses = 0;
int o = 0;
float d = 0;
float x = 0;
float awmax = 180.0;
float yg = 0;
float aw = 0;
float av = 0;
float y = 0;
float v = 0;
float i = 0;
int dira = 0;
int last_millis;
int c_num;

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
  *y = (float(pulses)/160)*(3.14*wheel_d);
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
  float kpv = 10;
  float kiv = 0.005;
  float kpw = 1;
  float vg = sqrt(sq(x)+sq(y));
  if (y < 0){
    vg = -1*vg;
  }
  i = i + vg;
  *av = (kpv*vg) + (kiv*i);
  int wg = (og-o);  
  *aw = kpw*wg;
  if ((*aw) > awmax){
    *av = 200;
    *aw = awmax;
  }
}

int FL (float d, float awmax, float o, float* av, float* aw){
  float kpw = 1;
  float og = 10.0*d;
  float delta_o = og-o;
  *aw = kpw*(delta_o) + 90.0;
  if (*aw > awmax){
    *aw = awmax;
    *av = 200;
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

int RegDist (float yg){
  Get_X(pulses, &prev_pulses, wheel_d, &y, &v, &prev_time);
  float delta_y = yg - y;
  if (abs(delta_y) >= 0.5 or v > 1){
    GtG(x, delta_y, o, awmax, &av, &aw);
    //Serial.println(delta_y);
    //Serial.println(delta_y);
    
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
    //Serial.println(aw); 
    digitalWrite(DIRA, dira);
    analogWrite(PWMA, av+200.0);
  }
  else{
    analogWrite(PWMA, 0);
    Serial.println("Done");
  }
}

int 

void setup() {
  pinMode(DIRA, OUTPUT);
  pinMode(PWMA, OUTPUT);
  pinMode(HALL, INPUT);
  myservo.attach(2);
  Serial.begin(115200);
  digitalWrite(DIRA, 1);
  Serial.setTimeout(100);
  attachInterrupt(digitalPinToInterrupt(HALL), Increase_pulses, FALLING);
  last_millis = millis();
  delay(5000);
}

void loop() {
  RegDist(25.5);
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

