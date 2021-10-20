
import json
import subprocess
import sys

subprocess.check_call([sys.executable, '-m', 'pip', 'install', '-r',
'requirements.txt'])

import boto3

#CHANGE THIS VARIABLES
THING_NAME="EI_BALENA_THING"
THING_TYPE="EI-Thing"
POLICY_NAME="EI-Thing-Policy"
#END OF VARIABLES

SETTINGS ={}


iot_client = boto3.client('iot')

response = iot_client.describe_endpoint(
    endpointType='iot:Data-ATS'
)

host = response['endpointAddress']
SETTINGS['host'] = host
SETTINGS['caPath'] = './certs/AmazonRootCA1.pem'


print("ENDPOINT = {host}".format(host =host))


response = iot_client.update_indexing_configuration(
    thingIndexingConfiguration={
        'thingIndexingMode': 'REGISTRY_AND_SHADOW'
    }
)



response = iot_client.create_policy(
    policyName=POLICY_NAME,
    policyDocument=json.dumps(json.load(open("./policy.json"))),
    tags=[
        {
            'Key': 'Name',
            'Value': POLICY_NAME
        },
    ]
)


response = iot_client.create_keys_and_certificate(
    setAsActive=True
)


SETTINGS['certificateArn'] = response['certificateArn']
certificateArn = response['certificateArn']
certificatePem = response['certificatePem']
privateKey = response['keyPair']['PrivateKey']

#save the certificate
with open('./certs/certificate.pem.crt', 'w') as outfile:
    outfile.write(certificatePem)
    SETTINGS['certPath'] = './certs/certificate.pem.crt'


#save the private key
with open('./certs/private.pem.key', 'w') as outfile:
    outfile.write(privateKey)
    SETTINGS['keyPath'] = './certs/private.pem.key'

      

response = iot_client.create_thing_type(
    thingTypeName=THING_TYPE,
    thingTypeProperties={
        'thingTypeDescription': 'Balena EI Thing',
        'searchableAttributes': [
            "Balena","EI"
        ]
    },
    tags=[
        {
            'Key': 'Name',
            'Value': THING_TYPE
        },
    ]
)

print("THING TYPE ARN= {arn}".format(arn =response['thingTypeArn']))

response = iot_client.create_thing(
    thingName=THING_NAME,
    thingTypeName=THING_TYPE
)

print("THING ARN= {arn}".format(arn =response['thingArn']))

response = iot_client.attach_policy(
    policyName=POLICY_NAME,
    target=certificateArn
)

response = iot_client.attach_thing_principal(
    thingName=THING_NAME,
    principal=certificateArn
)


with open('settings.json', 'w') as outfile:
    json.dump(SETTINGS, outfile)

print("Thing registered with AWS IoT")