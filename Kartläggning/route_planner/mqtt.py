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

client = mqtt.Client(transport="websockets")

client.on_connect=on_connect

print("Connecting to broker", host)

#client.tls_set()

#client.on_connect = on_connect
#client.on_message = on_message  
client.username_pw_set(username="jesper.jansson@abbindustrigymnasium.se", password="1234")
client.connect(host, 8883)
client.loop_start()
client.publish(topic, "hello world")
#client.subscribe(topic)

#client.loop_forever()  
time.sleep(4)
client.loop_stop()
client.disconnect()

#while True:
    