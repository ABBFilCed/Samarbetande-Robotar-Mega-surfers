import paho.mqtt.client as mqtt


class Mqtt():

    def __init__(self, broker, client_id, username, password, topic):
        """Initialize mqtt client and subscribe to topic."""
        self.broker = broker
        self.client = mqtt.Client(client_id=client_id, clean_session=True,
                                  userdata=None, protocol=mqtt.MQTTv31, transport="websockets")
        self.client.on_connect = self.on_connect
        self.client.on_disconnect = self.on_disconnect
        self.client.on_message = self.on_message

        print("Connecting to broker", broker)
        self.client.username_pw_set(
            username=username, password=password)
        self.client.connect(broker, 8883)

        self.client.loop_start()
        self.client.subscribe(username + "/" + topic)
        self.msgs = []

    def on_connect(self, client, userdata, flags, rc):
        """Prints status code when connected."""
        print(rc)
        if rc == 0:
            print("connected OK Returned code=", str(rc))
        else:
            print("Bad connection Returned code= ", str(rc))

    def on_disconnect(self, client, userdata, flags, rc=0):
        """Prints status code when disconnected."""
        print("disconnected result code " + str(rc))

    def on_message(self, client, userdata, msg):
        """Decodes and appends new message to msgs."""
        m_decode = str(msg.payload.decode("utf-8", "ignore"))
        self.msgs.append(m_decode)
