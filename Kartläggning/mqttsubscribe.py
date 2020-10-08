import paho.mqtt.client as mqtt 
import time

def on_log(client, userdata, level, buf):
    print("log: " + buf)

def on_connect(client, userdata, flags, rc):
    print(rc)
    if rc==0:
        print("connected OK Returned code=", str(rc))
    else:
        print("Bad connection Returned code= ", str(rc))

def on_disconnect(client, userdata, flags, rc = 0 ):
    print("disconnected result code " + str(rc))

# Dekrypterar inkommande meddelanden
def on_message(client, userdata, msg): 
    topic = msg.topic
    m_decode = str(msg.payload.decode("utf-8", "ignore"))
    print("message received "+ m_decode)

    
# Broker information
broker = "maqiatto.com"
client = mqtt.Client(client_id="client194954276", clean_session=True, userdata=None, protocol=mqtt.MQTTv31, transport="websockets")

# Kör funktioner
client.on_connect = on_connect
client.on_log = on_log
client.on_disconnect = on_disconnect
client.on_message = on_message

# Connectar till maqiatto.com
print("Connecting to broker", broker)
client.username_pw_set(username="jesper.jansson@abbindustrigymnasium.se", password="1234")
client.connect(broker, 8883)

client.loop_start()
client.subscribe("jesper.jansson@abbindustrigymnasium.se/map")

time.sleep(10)
client.loop_stop()
client.disconnect()