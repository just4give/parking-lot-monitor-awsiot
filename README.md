# Scale Your Fleet Of TinyML Solutions
Scale your parking lot monitoring system or any TinyML solution using AWS IoT , Edge Impulse and Balena

<p align="center">
<img width="978" alt="Screen Shot 2021-10-17 at 11 05 37 AM" src="https://user-images.githubusercontent.com/9275193/137633212-b9391d5b-065a-4f08-90bd-d1cdf5e839ca.png">

</p>

## Introduction

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




## Scale By Adding New Devices

## Extending The Solution




This project is in progress and I will uplaod code and document shortly. 
