import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print('Connected with the result code ' + str(rc), flush=True)
    client.subscribe('#')

def on_message(client, userdata, msg):
    print(msg.topic+" "+str(msg.payload), flush=True)


def main():
    time.sleep(10)
    global client

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect("mqtt", 1883)
    client.loop_forever()

if __name__ == '__main__':
    main()
