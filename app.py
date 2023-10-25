import time
from flask import Flask, render_template, jsonify
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
    client.on_message = on_message
    client.connect(broker, port)
    client.subscribe(topic)
    return client

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker!")
        client.subscribe(topic)
    else:
        print("Failed to connect, return code: " + str(rc))

def on_message(client, userdata, msg):
    global detection
    detection = int(msg.payload.decode())
    print("Detection:", detection)

@app.route('/')
def index():
    return render_template('index.html')  # Replace 'your_html_file.html' with the actual name of your HTML file

@app.route('/get_status', methods=['GET'])
def get_status():  # Renamed the function to 'get_status'
    global detection
    status = detection
    return jsonify({'status': status})

if __name__ == "__main__":
    client = connect()
    client.loop_start()
    app.run(debug=True) 
