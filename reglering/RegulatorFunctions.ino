#include <Wire.h>

#define DIRA 0 //Motor direction
#define PWMA 5 //Motor pwm
#define HALL 12

int pulses = 0;
float wheel_d = 3.6;
int prev_time = 0;
int prev_pulses = 0;
int o = 0;
float x = 0;
float awmax = 180.0;
float yg = 25.5;
float aw = 0;
float av = 0;
float y = 0;
float v = 0;
float i = 0;
int dira = 0;

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
  *y = (float(pulses)/130)*(3.14*wheel_d);
  *prev_pulses = pulses; 
  *prev_time = current_time;
  *o += aw*time_diff
  interrupts(); 
}

auto GtG (float x, float y, float o, float awmax, float* av, float*aw){
  int og = 0;
  if (not x == 0) {
     int og = tan(y/x)*360/(2*3.14);
  }
  float kpv = 5;
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
    *av = 0;
    *aw = awmax;
  }
}

int * FL (float d, float awmax){
  float kpv = 1;
  float kpw = 1;
  float vg = 0;
  if (d = 0){
    float vg = 20;
  }
  else {
    float vg = 1/d;
  }
  float av = kpv*vg;
  float aw = kpw*d;
  if (aw > awmax){
    aw = awmax;
    av = 0;
  }
  int result[] = {av, aw};
  return result;
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
  Serial.begin(115200);
  digitalWrite(DIRA, 1);
  attachInterrupt(digitalPinToInterrupt(HALL), Increase_pulses, FALLING);
}

void loop() {
  Get_X(pulses, &prev_pulses, wheel_d, &y, &v, &prev_time);
  float delta_y = yg - y;
  if (abs(delta_y) > 1.0 or v > 5){
  GtG(x, delta_y, o, awmax, &av, &aw);
  Serial.println(delta_y);
  //Serial.println(delta_y);
  
  if (av > 0){
    dira = 0;
  } else {
    dira = 1;
    av = -1*av;
  }
  digitalWrite(DIRA, dira);
  analogWrite(PWMA, av+200.0);
  }
  else{
    analogWrite(PWMA, 0);
    Serial.println("Done");
  }
  
}

