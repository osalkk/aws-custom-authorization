#!/usr/bin/python3

import paho.mqtt.client as mqtt
import ssl
import json,time
import paho.mqtt.publish as publish
import button
from datetime import datetime


def on_connect(mqttc, obj, flags, rc):
    if rc==0:
        print ("Subscriber Connection status code: "+str(rc)+" | Connection status: successful")
    else :
        print("Connection unsuccessful! (Result code " + str(rc) + ": " + RESULT_CODES[rc] + ")")
        client.disconnect()

def on_publish(client, userdata, mid):
    print(client, userdata, mid)

#Connect to AWS IoT
client = mqtt.Client(client_id="rasp1",protocol=mqtt.MQTTv311)
client.on_connect = on_connect
client.on_publish = on_publish
client.tls_set("/root/root-CA.pem",certfile="/root/c9aa9ef139-certificate.pem.crt",keyfile="/root/c9aa9ef139-private.pem.key",tls_version=ssl.PROTOCOL_SSLv23,ciphers=None)
client.tls_insecure_set(True)
client.connect("A1470V05UAX5KX.iot.eu-west-1.amazonaws.com", 8883, 60)
client.loop_start()

rc=0
while rc == 0:
    data={}
    if button.is_pressed():
        print('pressed')
        data['state']=button.is_pressed()
        data['time']=datetime.now().strftime('%Y/%m/%d %H:%M:%S')
        payload = json.dumps(data)
        print(payload)
        msg_info = client.publish("Rasp/data", payload, qos=1)
        time.sleep(0.3)

print('rc: ' +str(rc))
