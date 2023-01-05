import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import time
import json
from datetime import datetime
import os

influxClient = InfluxDBClient('influxdb', 8086)

def logging(msg):
    debug = os.getenv('DEBUG_DATA_FLOW')
    if debug:
        print(msg, flush=True)


def on_connect(client, userdata, flags, rc):
    logging(f'Connected with the result code {rc}')
    client.subscribe('#')

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload)
    logging(f'Received a message by topic [{topic}]')

    log_msg = ''
    data_timestamp = ''
    location, station = topic.split('/')

    if 'timestamp' in payload:
        data_timestamp = payload['timestamp']
        logging(f'Data timestamp is: {data_timestamp}')
    else:
        data_timestamp = datetime.now().strftime('%Y-%M-%d %H:%M:%S')
        logging('Data timestamp is NOW')

    for key in payload:
        log_msg = data_timestamp + ' '
        log_msg += f'{location}.{station}.'

        data = []

        if isinstance(payload[key], int) or isinstance(payload[key], float):
            log_msg += key + ' ' + str(payload[key])
            data.append(
                {
                    "measurement": f'{station}.{key}',
                    "tags" : {
                        "location" : location,
                        "station" : station
                    },
                    "fields": {
                        "value" : float(payload[key])
                    },
                    "timestamp" : data_timestamp
                }
            )

            influxClient.write_points(data)
            logging(log_msg)


def main():
    time.sleep(10)
    global client

    if len(list(filter(lambda x: x['name'] == "iot_data", influxClient.get_list_database()))) == 0:
        influxClient.create_database("iot_data")
    influxClient.switch_database('iot_data')

    logging('Connected to InfluxDB')

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect('mqtt', 1883)
    client.loop_forever()

if __name__ == '__main__':
    main()
