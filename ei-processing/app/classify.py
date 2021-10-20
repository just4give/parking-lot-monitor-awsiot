from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import random
import time
import os
import uuid

print("AWS IOT PUB-SUB Example")
SETTINGS = json.load(open("./settings.json"))

UUID = os.environ['BALENA_DEVICE_UUID']
AWS_TOPIC = os.environ['AWS_TOPIC']



host = SETTINGS['host']

def customCallback(client, userdata, message):
    print("Received a new message: ")
    print(message.payload)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

myMQTTClient = AWSIoTMQTTClient("myClientID")
myMQTTClient.configureEndpoint(host, 8883)
myMQTTClient.configureCredentials(SETTINGS['caPath'], SETTINGS['keyPath'], SETTINGS['certPath'])
myMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

myMQTTClient.connect()


myMQTTClient.subscribe(AWS_TOPIC, 1, customCallback)

counter = 0
while True:
    sensorData = {
        "uuid": UUID,
        "temperature": random.randint(50, 70)
    }
    myMQTTClient.publish(AWS_TOPIC, json.dumps(sensorData), 0)
    counter += 1
    time.sleep(60)


#myMQTTClient.disconnect()