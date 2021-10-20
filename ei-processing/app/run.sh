#!/bin/sh

echo "COLLECTION MODE" $EI_COLLECT_MODE_IMAGE

if [ $EI_COLLECT_MODE_IMAGE = "Y" ];
then
    edge-impulse-linux --api-key $EI_API_KEY_IMAGE --disable-microphone
else
    edge-impulse-linux-runner --api-key $EI_API_KEY_IMAGE --download modelfile.eim
    python3 classify.py 
fi