import paho.mqtt.client as mqtt
from influxdb import InfluxDBClient
import time
import json
from datetime import datetime

influxClient = InfluxDBClient('influxdb', 8086)

def on_connect(client, userdata, flags, rc):
    print('Connected with the result code ' + str(rc), flush=True)
    client.subscribe('#')

def on_message(client, userdata, msg):
    topic = msg.topic
    payload = json.loads(msg.payload)
    print(f'Received a message by topic [{topic}]', flush=True)

    log_msg = ''
    data_timestamp = ''
    location, station = topic.split('/')

    if 'timestamp' in payload:
        data_timestamp = payload['timestamp']
        print(f'Data timestamp is: {data_timestamp}', flush=True)
    else:
        data_timestamp = datetime.now().strftime('%Y-%M-%d %H:%M:%S')
        print('Data timestamp is NOW', flush=True)

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
            print(log_msg, flush=True)

            influxClient.write_points(data)


def main():
    time.sleep(10)
    global client
        # check if db exists
    if len(list(filter(lambda x: x['name'] == "iot_data", influxClient.get_list_database()))) == 0:
        influxClient.create_database("iot_data")
    influxClient.switch_database('iot_data')

    print('Connected to InfluxDB', flush=True)

    # create mqtt client
    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message

    client.connect('mqtt', 1883)
    client.loop_forever()

if __name__ == '__main__':
    main()
