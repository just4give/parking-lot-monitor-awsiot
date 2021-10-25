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
## Create Balena Fleet 
Before we collect images to train our model, we need to create balena fleet and connect Raspberry Pi directly to Edge Impulse data collection module.

## Build Model With Edge Impulse




## Scale By Adding New Devices

## Extending The Solution




This project is in progress and I will uplaod code and document shortly. 
