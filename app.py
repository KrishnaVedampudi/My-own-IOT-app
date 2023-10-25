import time
from flask import Flask, render_template
from paho.mqtt import client as mqtt_client

app = Flask(__name__)
broker = "broker.emqx.io"
port = 1883
topic = "topicName/pir"

client_id = 'test'
username = 'emqx'
password = ''

detection = 1

def connect():
    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.on_subscribe = on_subscribe
    client.connect(broker, port)
    return client

def on_connect(client: mqtt_client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker! Result code: " + str(rc))
        client.subscribe(topic)
    else:
        print("Failed to connect, return code: " + str(rc))

def on_subscribe(client, userdata, mid, granted_qos):
    print("Subscribed to topic with QoS: " + str(granted_qos))

def on_message(client, userdata, msg):
    global detection
    detection = msg.payload.decode()
    print("Detection:", detection)

@app.route('/')
def check_detection():
    client_run = connect()
    client_run.loop_start()
    time.sleep(1)
    status = int(detection)
    return render_template('index.html', status=status)

if __name__ == "__main__":
    app.run()
