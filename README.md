# Scale Your Fleet Of TinyML Solutions
Scale your parking lot monitoring system or any TinyML solution using AWS IoT , Edge Impulse and Balena

<p align="center">
<img width="978" alt="Screen Shot 2021-10-17 at 11 05 37 AM" src="https://user-images.githubusercontent.com/9275193/137633212-b9391d5b-065a-4f08-90bd-d1cdf5e839ca.png">

</p>

## Introduction
This project is a proof of concept to demonstrate how easily you can deploy a fleet of edge devices running tinyML model with object detection capability. I have chosen a simple use case of counting cars in a parking lot. You can use similar infrasturcture to build any kind of objection detection use cases such as identifying product defect in real manufactoring workflow, automate car inspection for exterior damages etc.
Parking facilities need to know how many cars are parked in a given facility at any given point of time, to evaluate how many empty parkings avialble and intake more customers. You also want to keep track of the number of cars that enter and exit your facility during any given time. You can use this information to improve operations, such as adding more parking payment centers, optimizing price, directing cars to different floors etc. Parking center owners typically operate on multiple floor or more than one facility and they want to manage a fleet of devices and aggregate real-time data to take effifient decision on business process.

![IMG_4948](https://user-images.githubusercontent.com/9275193/139112437-0644638b-c782-40a8-9632-0c5a41c66bbe.jpg)

## Re-requisite

### Software 
<table>
<tr><td>
<img height="24px" src="https://files.balena-cloud.com/images/fincm3/2.58.3%2Brev1.prod/logo.svg" alt="fincm3" style="max-width: 100%; margin: 0px 4px;"></td><td> balenaFin</td>
</tr>
<tr><td>
<img height="24px" src="https://files.balena-cloud.com/images/raspberrypi3/2.58.3%2Brev1.prod/logo.svg" alt="raspberrypi3" style="max-width: 100%; margin: 0px 4px;"></td><td>Raspberry Pi 3 Model B+</td>
</tr>
<tr><td>
<img height="24px" src="https://files.balena-cloud.com/images/raspberrypi4-64/2.65.0%2Brev1.prod/logo.svg" alt="raspberrypi4-64" style="max-width: 100%; margin: 0px 4px;"></td><td>Raspberry Pi 4 Model B</td>
</tr>
</table>

 [Raspberry Pi camera](https://www.raspberrypi.org/products/camera-module-v2/) or any USB camera.

### Software 

* Sign up for a free [Edge Impulse account](https://edgeimpulse.com/)
* Sign up for a free [BalenaCloud account](https://www.balena.io/)
* [balenaEtcher](https://www.balena.io/etcher/)
* Sign up for a free [AWS account](https://console.aws.amazon.com/)
* Python 3.7+ and pip

## Create AWS IoT Resources and Certificates
You must have an active AWS account to create resources on AWS cloud. First install and configure AWS CLI
```
pip3 install awscli --upgrade --user
```
Or follow [this](https://docs.aws.amazon.com/cli/latest/userguide/install-cliv1.html) link. After installation is done, you need to configure AWS CLI. Follow [this](https://docs.aws.amazon.com/cli/latest/userguide/cli-configure-quickstart.html) article to set it up.

You are now ready to create AWS resources. To communicate with AWS IoT Core from Edge devices, at minimum we need following AWS rerources to be created. 
- A Policy
- Key & Certificate
- Thing

Policy needs to be attached to the certificate and certificate needs to be attched to the "thing".
If you are doing this first time, this might sound complicated. Don't worry! I have a python `register.py` utility program under device_registration folder which will create all above resources. Before you execute the program, you may want to change below variables.

```
THING_NAME="EI_BALENA_THING"
THING_TYPE="EI-Thing"
POLICY_NAME="EI-Thing-Policy"
```
Then execute below commands
```
cd device_registration
python3 register.py
```
Above program will create all the resources and download the key and certificate and store them under `certs` folder.
To validate, you may run `pubsub.py`. This program will connect to your AWS IoT core using downloaded key & certificate and send data to `EI_TOPIC` topic every 5 seconds. Log into your AWS console and make sure your topic is receiving data. 

Once everything is verified and looking good, copy below files from `device_registration/certs` folder to `ei_processing/app/certs`
```
certificate.pem.crt
private.pem.key
```
## Create Edge Impulse Project
Head over to [Edge Impluse Studio](https://studio.edgeimpulse.com), click on your profile name, then click on `+ Create new project`. Enter a name for your project and choose object detection when prompted. After your project is created, you will be taken to project dashboard page. Click on "Keys" tab and create a new API key. 

<p align="center">
<img width="978" alt="Screen Shot 2021-10-17 at 11 05 37 AM" src="https://user-images.githubusercontent.com/9275193/138987190-06286698-ab28-4727-8f82-e21237a1262e.png">

</p>

Copy the API key and save somewhere. You need that in a moment.

## Create Balena Fleet 
Click on the *deploy-with-balena* button as given below, which will help you to deploy your application to balenaCloud and then to your Raspbery Pi in **one-click!**

[![](https://balena.io/deploy.png)](https://dashboard.balena-cloud.com/deploy?repoUrl=https://github.com/just4give/parking-lot-monitor-awsiot)

On the popup modal, select your device type (Raspberry Pi 3 or 4 ) and toggle "Advanced" switch.
<img width="1665" alt="Screen Shot 2021-10-26 at 9 58 47 PM" src="<img width="1010" alt="Screen Shot 2021-10-26 at 10 09 51 PM" src="https://user-images.githubusercontent.com/9275193/138987981-a8899856-aba1-4e92-9283-e912e4c2563b.png">">

That should expand the fleet variables section. Paste API key from Edge Impulse Studio under EI_API_KEY_IMAGE. Set collection mode to "Y" and make sure your EI_TOPIC is same as your used during device registration.
<img width="1011" alt="Screen Shot 2021-10-26 at 10 10 13 PM" src="https://user-images.githubusercontent.com/9275193/138988167-1838c41e-9fa0-4965-bd8e-5e8034e31437.png">

Then click on  "Create and deploy" button. In a moment, you should see your fleet on Balena Cloud account. You should see a button "+ Add device". Clicking on that should open a modal. Choose Ethernet+Wifi, enter your Wifi SSID & password. Then click on "Download balenaOs" button. This should download the image as a zip file. Flash this image on a SD card using Balena Etcher. Put the SD card on Raspberry Pi 3 and plug the device to power. Wait for 5-10 minutes and your device should come online on balena cloud.

## Build Model With Edge Impulse
To quickly get started you can fork my [project](https://studio.edgeimpulse.com/public/53686/latest) or continue reading.

Once your device is online, you should see below log on balena cloud which indicates your device is connected to Edge Impulse.
```
 ei-processing  COLLECTION MODE Y
 ei-processing  Edge Impulse Linux client v1.2.10
 ei-processing  
 ei-processing  [SER] Using camera MicrosoftÂ® LifeCam HD-3000 starting...
 ei-processing  [SER] Connected to camera
 ei-processing  [WS ] Connecting to wss://remote-mgmt.edgeimpulse.com
 ei-processing  [WS ] Connected to wss://remote-mgmt.edgeimpulse.com
 ```
 Now head over to EI Studio and navigate to Data aquisition page. On the right, you should see "Record new data" section and you will also notice feed from your camera.

 <img width="710" alt="Screen Shot 2021-10-27 at 9 16 46 AM" src="https://user-images.githubusercontent.com/9275193/139073472-d891ed50-8fd6-45bd-9c4b-7a38a4ad6c58.png">

Click on "Start sampling" to capture the image. Capture lot of images of cars and some random objects such as person, bike, motorcycle etc. In my project I have used some toy cars and some lego humans. Collect at least 20 cars and 20 other images. After you capture the images, you should see them under "Labeling queue" tab. Click on that and you should see the first image you captured.

<img width="1437" alt="Screen Shot 2021-10-27 at 9 25 44 AM" src="https://user-images.githubusercontent.com/9275193/139075750-422bea3a-1c9a-4899-8328-9881d8498ac7.png">

Drag your mouse over the object and label it. Repeat for all the images. We have two labels - car and unknown. 

Watch this youtube [video](https://youtu.be/dY3OSiJyne0) created by Jan Jongboom, CTO of Edge Impulse for detail step by step instructions to train and build your model. 

Once your model is trained, head over to balena cloud account. Navigate to fleet variables page (Not device variables) and change `EI_COLLECT_MODE_IMAGE` to `N`.

Your device will be restarted. See the logs on balena cloud. EI model will be automatically downloaded on your device and ready for object detection.

```
 ei-processing  COLLECTION MODE N
 ei-processing  Edge Impulse Linux runner v1.2.10
 ei-processing  
 ei-processing  [RUN] Downloading model...
 ei-processing  [RUN] Downloading model OK
 ei-processing  [RUN] Stored model in /usr/src/app/modelfile.eim
 ei-processing  AWS IOT PUB-SUB Example
 ei-processing  MODEL: /usr/src/app/modelfile.eim
 ei-processing  Loaded runner for "Mithun / parking-lot-car-awsiot"
 ei-processing  Looking for a camera in port 0:
 ei-processing  Camera V4L2 (480.0 x 640.0) found in port 0 
 ei-processing  Looking for a camera in port 1:
 ei-processing  [ WARN:0] global /tmp/pip-wheel-qd18ncao/opencv-python/opencv/modules/videoio/src/cap_v4l.cpp (893) open VIDEOIO(V4L2:/dev/video1): can't open camera by index
 ei-processing  Looking for a camera in port 2:
 ei-processing  [ WARN:0] global /tmp/pip-wheel-qd18ncao/opencv-python/opencv/modules/videoio/src/cap_v4l.cpp (893) open VIDEOIO(V4L2:/dev/video2): can't open camera by index
 ei-processing  Looking for a camera in port 3:
 ei-processing  [ WARN:0] global /tmp/pip-wheel-qd18ncao/opencv-python/opencv/modules/videoio/src/cap_v4l.cpp (893) open VIDEOIO(V4L2:/dev/video3): can't open camera by index
 ei-processing  Looking for a camera in port 4:
 ei-processing  [ WARN:0] global /tmp/pip-wheel-qd18ncao/opencv-python/opencv/modules/videoio/src/cap_v4l.cpp (893) open VIDEOIO(V4L2:/dev/video4): can't open camera by index
 ei-processing  Camera V4L2 (480.0 x 640.0) in port 0 selected.
 ```

 Now place one or two cars in front of the camera and see the logs. You will notice your device counts number of cars it sees. How cool is that? 

 ```
 ei-processing  Camera V4L2 (480.0 x 640.0) in port 0 selected.
 ei-processing  1 Cars found.
 ei-processing  Received a new message: 
 ei-processing  b'{"uuid": "49418b480e408ef9c632fc6cb25ebfdc", "cars": 1}'
 ei-processing  from topic: 
 ei-processing  EI_TOPIC
 ei-processing  --------------
 ei-processing  
 ei-processing  
 ```

<img width="415" alt="Screen Shot 2021-10-25 at 11 52 50 AM" src="https://user-images.githubusercontent.com/9275193/139079306-5311e834-fa68-42d7-b692-70f725f30177.png">

For the purpose of visual feedback, I have integrated `Telegram` bot with this project. This step is optional for you. But, if you want to add Telegram bot, you need to get Bot access token and chat id. Once you obtain them, add them in fleet variable. 

```
TG_CHAT_ID
TG_TOKEN

```
### Check Data on AWS
You have noticed from the log that, when a car is detected, data is sent to AWS IoT topic. Your device connects to AWS IoT using the certificates you created during device registration process. Head over to your AWS console.

<img width="1660" alt="Screen Shot 2021-10-27 at 10 12 29 AM" src="https://user-images.githubusercontent.com/9275193/139083352-1c020890-f90d-4d77-a317-5cb7e8ac4d39.png">

Go to IoT Core service and click on "Test" from left menu. Then click on "MQTT test client". Enter `#` in topic filter text field and click on "Subscribe" button.
<img width="1333" alt="Screen Shot 2021-10-27 at 10 28 05 AM" src="https://user-images.githubusercontent.com/9275193/139086057-2a8fdf45-a27b-403e-8a5d-a73e7bc7fb85.png">

Within 2 minutes, you should receive data in your topic as below.
```
{
  "uuid": "49418b480e408ef9c632fc6cb25ebfdc",
  "cars": 1
}
```
`uuid` is the device id which is unique to the device. 


## Scale By Adding New Devices
Now as we configured and deployed object detection model to our device, it's time to see how we can add more devices to the fleet. This step is super simple and you already did before. From your balena fleet dashboard, click on "Add device" button. Choose your device type, enter Wifi credential, download the image, flash on the SD card, insert SD card to Raspberry Pi and power on. 

<img width="1477" alt="Screen Shot 2021-10-27 at 12 19 06 PM" src="https://user-images.githubusercontent.com/9275193/139106197-fffb0c6f-e306-471a-bc86-09640afeb417.png">

In few minutes, new device should show up on your fleet dashboard and ready for object detection. It's that simple! If you head over to AWS console, you will notice data coming from both the devices. Each device has unique `uuid`.



## Extending The Solution
We can do so much more with this proof of concept project as explained earlier and extend it to other parking-related use cases, such as the following:

As data is sent to AWS IoT, opportunities are endless. You can forward the data to IoT Event and build a fleet workflow using Lambda. You can trigger SMS/Emails/Push Notifications using Amazon Pinpoint. You can ingest data to dynamodb through AWS AppSync. You can build a web/mobile app using AWS Amplify and get realtime update and many more. 
