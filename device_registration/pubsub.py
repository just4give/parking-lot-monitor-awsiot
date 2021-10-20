from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import random
import time

AWS_TOPIC="EI_TOPIC"
SETTINGS = json.load(open("./settings.json"))



print("AWS IOT PUB-SUB Example")
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
        "id": counter,
        "temperature": random.randint(50, 70)
    }
    myMQTTClient.publish(AWS_TOPIC, json.dumps(sensorData), 0)
    counter += 1
    time.sleep(5)


#myMQTTClient.disconnect()