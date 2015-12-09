#!/usr/bin/python3

import paho.mqtt.client as mqtt
import ssl
import json,time
import RPi.GPIO as GPIO

GPIO.setwarnings(False)

def on_connect(client, userdata, flags, rc):
    print("Connected with result code "+str(rc))
    client.subscribe("$aws/things/Raspberry-pi/shadow/update/accepted")

def on_message(client, userdata, msg):
    message_json = json.loads(msg.payload.decode())
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(11, GPIO.OUT)
    if message_json['state']['desired']['led'] == "on":
         print("LED ON")
         GPIO.output(11,GPIO.HIGH)
    elif message_json['state']['desired']['led'] == "off":
         print("LED OFF")
         GPIO.output(11,GPIO.LOW)
    elif message_json['state']['desired']['led'] == "blink":
         print("blinking")
         count=message_json['state']['desired']['count']
         print(count)
         for i in range (0,int(count)):
             GPIO.output(11,GPIO.HIGH)
             time.sleep(0.1)
             GPIO.output(11,GPIO.LOW)
             time.sleep(0.1)


#Connect to AWS IoT
client = mqtt.Client(client_id="myrasp")
client.on_connect = on_connect
client.on_message = on_message
client.tls_set(ca_certs='/root/root-CA.pem', certfile='/root/c9aa9ef139-certificate.pem.crt', keyfile='/root/c9aa9ef139-private.pem.key', tls_version=ssl.PROTOCOL_SSLv23)
client.tls_insecure_set(True)
client.connect("A1470V05UAX5KX.iot.eu-west-1.amazonaws.com", 8883, 30)
client.loop_forever()


