import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(rc)
    if rc==0:
        print("connected OK Returned code=", str(rc))
    else:
        print("Bad connection Returned code= ", str(rc))

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload))

client_id = "Backend"
host = "maqiatto.com"
port = 8883
topic = "jesper.jansson@abbindustrigymnasium.se/map"

client = mqtt.Client(client_id="client_id", clean_session=True, userdata=None, transport="tcp")

client.on_connect=on_connect

print("Connecting to broker", host)

#client.on_connect = on_connect
#client.on_message = on_message  

client.connect(host, 1883)
client.loop_start()
client.publish(topic, "hello world")
#client.subscribe(topic)

#client.loop_forever()  
time.sleep(4)
client.loop_stop()
client.disconnect()

#while True:
    