from datetime import datetime
import paho.mqtt.client as mqtt

broker_address=""


def on_message(client, userdata, message):
    print("Message Function Triggered")
    time = datetime.now()
    print(time)
    print("message received  ", str(message.payload.decode("utf-8")),\
          "topic", message.topic, "retained ", message.retain)
    if message.retain == 1:
        print("This is a retained message")



def on_connect(client, userdata, flags, rc):
    if rc==0:
        print("connected OK Returned code",rc)
        print("Subscribing to topic")
        client.subscribe("", qos=2)
    else:
        print("Bad connection Returned code",rc)

def on_disconnect(client, userdata, rc):
   print("Client Got Disconnected")
   print('rc value '+str(rc))
   time = datetime.now()
   print(time)
   if rc != 0:
       print('Unexpected MQTT disconnection. Will auto-reconnect')
   else:
       print('rc value:' + str(rc))


def mqttConnection():
    client = mqtt.Client("")
    client.on_connect = on_connect
    # client.on_disconnect =  on_disconnect
    client.on_message = on_message
    print("connecting to broker")
    client.connect(broker_address, 1883, 60)
    client.loop_forever()

if __name__ == "__main__":
    mqttConnection()
