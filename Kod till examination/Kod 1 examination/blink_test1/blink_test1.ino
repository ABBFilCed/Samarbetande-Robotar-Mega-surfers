#include "EspMQTTClient.h"

void onConnectionEstablished();

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

//int passeratEnRutaLed = 12; // lampa för antal rutor
int hittatHinderLed = 14; // lampa för hittat hinder
String payload;
int ledOn;

void onRecieve(){
  ledOn = payload.toInt();
  Serial.println("Mqtt");
}


void onConnectionEstablished()
{
  client.subscribe("jesper.jansson@abbindustrigymnasium.se/ruta", [] (const String &payload)
  {
    onRecieve();
  });
}

void setup() {
  pinMode(LED_BUILTIN, OUTPUT);
  //pinMode(hittatHinderLed, OUTPUT);
  digitalWrite(LED_BUILTIN, LOW);
  Serial.begin(115200);
}

void loop() { 
  client.loop();
  if (ledOn){
    Serial.println("Lyser");
    digitalWrite(LED_BUILTIN, HIGH);
    delay(1000);
    digitalWrite(LED_BUILTIN, LOW);
    ledOn = 0;
  }
  //digitalWrite(hittatHinderLed, HIGH);
}
