import paho.mqtt.client as mqtt
import random

clientID = "MyClient" + random.randint(1000,9998)
client = mqtt.Client(client_id=clientID, clean_session=True, userdata=None, protocol="MQTTv311", transport="tcp")


host = "maqiatto.com"
port = 8883

client.connect(host, port=port, keepalive=999999, bind_address="")

client.connected_flag=False

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        print("connected OK Returned code=",rc)
        #client.subscribe(topic)
    else:
        print("Bad connection Returned code= ",rc)

topic1 = "filip.cederblad@abbindustrigymnasium.se/bil"
topic2 = "filip.cederblad@abbindustrigymnasium.se/bil1"

client.subscribe(topic1)
client.subscribe(topic2)

def on_message(client, userdata, message):
    mess = str(message.payload.decode("utf-8"))
    #Kod för att lägga till rutor i kartan och på vilken plats de ska vara. Typ if payload == 1 lägg till 1 på rutan framför roboten

client.on_message=on_message   



#while True:
    