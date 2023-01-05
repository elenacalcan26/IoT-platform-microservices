import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import time
import json

influxClient = InfluxDBClient('influxdb', 8086)

def on_connect(client, userdata, flags, rc):
    print('Connected with the result code ' + str(rc), flush=True)
    client.subscribe('#')

def on_message(client, userdata, msg):
    # print(msg.topic+" "+str(msg.payload), flush=True)
    topic = msg.topic
    payload = json.loads(msg.payload)
    print(f'Received a message by topic [{topic}]', flush=True)

    pass


def main():
    time.sleep(10)
    global client

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect('mqtt', 1883)
    client.loop_forever()

if __name__ == '__main__':
    main()
