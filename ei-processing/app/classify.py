from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import json
import random
import time
import os
import uuid
import cv2
from edge_impulse_linux.image import ImageImpulseRunner
import subprocess

print("AWS IOT PUB-SUB Example")
SETTINGS = json.load(open("./settings.json"))

UUID = os.environ['BALENA_DEVICE_UUID']
AWS_TOPIC = os.environ['AWS_TOPIC']
EI_API_KEY_IMAGE = os.environ['EI_API_KEY_IMAGE']

TG_CHAT_ID=None
TG_TOKEN=None
INTERVAL_IN_SECONDS=120

if 'TG_CHAT_ID' in os.environ:
    TG_CHAT_ID = os.environ['TG_CHAT_ID']

if 'TG_TOKEN' in os.environ:
    TG_TOKEN = os.environ['TG_TOKEN']

if 'INTERVAL_IN_SECONDS' in os.environ:
    INTERVAL_IN_SECONDS = os.environ['INTERVAL_IN_SECONDS']

async_mode = None
runner = None
show_camera = False
video_frame = None
videoCaptureDeviceId = 0

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

# counter = 0
# while True:
#     sensorData = {
#         "uuid": UUID,
#         "temperature": random.randint(50, 70)
#     }
#     myMQTTClient.publish(AWS_TOPIC, json.dumps(sensorData), 0)
#     counter += 1
#     time.sleep(60)


#myMQTTClient.disconnect()
def send_image(imageFile):
        command = 'curl -s -X POST https://api.telegram.org/bot' + TG_TOKEN + '/sendPhoto -F chat_id=' + TG_CHAT_ID + " -F photo=@" + imageFile
        subprocess.call(command.split(' '))
        return

def now():
    return round(time.time() * 1000)

def get_webcams():
    port_ids = []
    for port in range(5):
        print("Looking for a camera in port %s:" %port)
        camera = cv2.VideoCapture(port)
        if camera.isOpened():
            ret = camera.read()[0]
            if ret:
                backendName =camera.getBackendName()
                w = camera.get(3)
                h = camera.get(4)
                print("Camera %s (%s x %s) found in port %s " %(backendName,h,w, port))
                port_ids.append(port)
            camera.release()
    return port_ids

def main():
    global videoCaptureDeviceId
    model = '/usr/src/app/modelfile.eim'
    last_sent = 0

    dir_path = os.path.dirname(os.path.realpath(__file__))
    modelfile = os.path.join(dir_path, model)

    print('MODEL: ' + modelfile)

    with ImageImpulseRunner(modelfile) as runner:
        try:
            model_info = runner.init()
            print('Loaded runner for "' + model_info['project']['owner'] + ' / ' + model_info['project']['name'] + '"')
            labels = model_info['model_parameters']['labels']
            
            port_ids = get_webcams()
            if len(port_ids) == 0:
                raise Exception('Cannot find any webcams')

            videoCaptureDeviceId = int(port_ids[0])


            camera = cv2.VideoCapture(videoCaptureDeviceId)
            ret = camera.read()[0]
            if ret:
                backendName = camera.getBackendName()
                w = camera.get(3)
                h = camera.get(4)
                print("Camera %s (%s x %s) in port %s selected." %(backendName,h,w, videoCaptureDeviceId))
                camera.release()
            else:
                raise Exception("Couldn't initialize selected camera.")

            next_frame = 0 # limit to ~10 fps here

            for res, img in runner.classifier(videoCaptureDeviceId):
                img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)
                
                if (next_frame > now()):
                    time.sleep((next_frame - now()) / 1000)

                # print('classification runner response', res)
                

                if "classification" in res["result"].keys():
                    print('Result (%d ms.) ' % (res['timing']['dsp'] + res['timing']['classification']), end='')
                    for label in labels:
                        score = res['result']['classification'][label]
                        print('%s: %.2f\t' % (label, score), end='')
                    print('', flush=True)

                elif "bounding_boxes" in res["result"].keys():
                    no_of_cars = 0
                    #print('Found %d bounding boxes (%d ms.)' % (len(res["result"]["bounding_boxes"]), res['timing']['dsp'] + res['timing']['classification']))
                    for bb in res["result"]["bounding_boxes"]:
                        if bb['label'] == 'car':
                            no_of_cars = no_of_cars + 1
                            img = cv2.rectangle(img, (bb['x'], bb['y']), (bb['x'] + bb['width'], bb['y'] + bb['height']), (0, 255, 0), 1)
                            img = cv2.putText(img, "%s" %( bb['label']),(bb['x'],bb['y']-10), cv2.FONT_HERSHEY_SIMPLEX,0.50, (0,255, 0), 1)
                        else:
                            img = cv2.rectangle(img, (bb['x'], bb['y']), (bb['x'] + bb['width'], bb['y'] + bb['height']), (0, 0, 0), 1)
                            img = cv2.putText(img, "%s" %( bb['label']),(bb['x'],bb['y']-10), cv2.FONT_HERSHEY_SIMPLEX,0.50, (0,0, 0), 1)
                    
                    #no_of_cars = len(res["result"]["bounding_boxes"])
                    img = cv2.putText(img, "CAM ID %s" %( UUID),(10,20), cv2.FONT_HERSHEY_SIMPLEX,0.50, (255,0, 0), 2)
                    img = cv2.putText(img, "CARS %s" %( str(no_of_cars)),(10,40), cv2.FONT_HERSHEY_SIMPLEX,0.50, (255,0, 0), 2)
                    if no_of_cars > 0 and (time.time()-last_sent) > INTERVAL_IN_SECONDS:
                        last_sent = time.time()
                        print("{cars} Cars found.".format(cars = no_of_cars))
                        cv2.imwrite('/var/media/frame.jpg', img)
                        sensorData = {
                            "uuid": UUID,
                            "cars": no_of_cars
                        }
                        myMQTTClient.publish(AWS_TOPIC, json.dumps(sensorData), 0)
                        send_image('/var/media/frame.jpg')
                        
     

            next_frame = now() + 100
        finally:
            if (runner):
                runner.stop()

if __name__ == "__main__":
    main()