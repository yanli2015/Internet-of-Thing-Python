

from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import sys
import logging
import time
import getopt
from temperature_iot import *
import wemo2
import my_email_module
import json

# Custom MQTT message callback
def customCallback(client, userdata, message):
    temperature = message.payload
    print("Received a new message: ")
    print(temperature)
    print("from topic: ")
    print(message.topic)
    print("--------------\n\n")

# Usage
usageInfo = """Usage:

Use certificate based mutual authentication:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -c <certFilePath> -k <privateKeyFilePath>

Use MQTT over WebSocket:
python basicPubSub.py -e <endpoint> -r <rootCAFilePath> -w

Type "python basicPubSub.py -h" for available options.
"""
# Help info
helpInfo = """-e, --endpoint
	Your AWS IoT custom endpoint
-r, --rootCA
	Root CA file path
-c, --cert
	Certificate file path
-k, --key
	Private key file path
-w, --websocket
	Use MQTT over WebSocket
-h, --help
	Help information
-p, --ip
    WEMO's IP
-t, --threshold_temperature
    The temperature that need to turn on the air conditioner
"""

# Read in command-line parameters
useWebsocket = False
host = ""
rootCAPath = ""
certificatePath = ""
privateKeyPath = ""
wemoIP = ""
threshold_temperature = ""
try:
    opts, args = getopt.getopt(sys.argv[1:], "hwe:k:c:r:p:t",
                               ["help", "endpoint=", "key=", "cert=", "rootCA=", "websocket", "ip","threshold_temperature"])
    if len(opts) == 0:
        raise getopt.GetoptError("No input parameters!")
    for opt, arg in opts:
        if opt in ("-h", "--help"):
            print(helpInfo)
            exit(0)
        if opt in ("-e", "--endpoint"):
            host = arg
        if opt in ("-r", "--rootCA"):
            rootCAPath = arg
        if opt in ("-c", "--cert"):
            certificatePath = arg
        if opt in ("-k", "--key"):
            privateKeyPath = arg
        if opt in ("-w", "--websocket"):
            useWebsocket = True
        if opt in ("-p", "--ip"):
            wemoIP = arg
        if opt in ("-t", "--threshold_temperature"):
            threshold_temperature = arg
            print threshold_temperature + "********"
except getopt.GetoptError:
    print(usageInfo)
    exit(1)

# Missing configuration notification
missingConfiguration = False
if not host:
    print("Missing '-e' or '--endpoint'")
    missingConfiguration = True
if not rootCAPath:
    print("Missing '-r' or '--rootCA'")
    missingConfiguration = True
if not useWebsocket:
    if not certificatePath:
        print("Missing '-c' or '--cert'")
        missingConfiguration = True
    if not privateKeyPath:
        print("Missing '-k' or '--key'")
        missingConfiguration = True
if missingConfiguration:
    exit(2)

# Configure logging
logger = None
if sys.version_info[0] == 3:
    logger = logging.getLogger("core")  # Python 3
else:
    logger = logging.getLogger("AWSIoTPythonSDK.core")  # Python 2
logger.setLevel(logging.DEBUG)
streamHandler = logging.StreamHandler()
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
streamHandler.setFormatter(formatter)
logger.addHandler(streamHandler)

# Init AWSIoTMQTTClient
myAWSIoTMQTTClient = None
if useWebsocket:
    myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub", useWebsocket=True)
    myAWSIoTMQTTClient.configureEndpoint(host, 443)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath)
else:
    myAWSIoTMQTTClient = AWSIoTMQTTClient("basicPubSub")
    myAWSIoTMQTTClient.configureEndpoint(host, 8883)
    myAWSIoTMQTTClient.configureCredentials(rootCAPath, privateKeyPath, certificatePath)

# AWSIoTMQTTClient connection configuration
myAWSIoTMQTTClient.configureAutoReconnectBackoffTime(1, 32, 20)
myAWSIoTMQTTClient.configureOfflinePublishQueueing(-1)  # Infinite offline Publish queueing
myAWSIoTMQTTClient.configureDrainingFrequency(2)  # Draining: 2 Hz
myAWSIoTMQTTClient.configureConnectDisconnectTimeout(10)  # 10 sec
myAWSIoTMQTTClient.configureMQTTOperationTimeout(5)  # 5 sec

# Connect and subscribe to AWS IoT
myAWSIoTMQTTClient.connect()
# myAWSIoTMQTTClient.subscribe("sdk/test/Python", 1, customCallback)
# time.sleep(2)

# Publish to the same topic in a loop forever
loopCount = 0
while True:
    print wemoIP
    threshold_temperature = 70.0
    switch = wemo2.wemo(wemoIP)
    payload_map = read_temp()
    current_temperature = float(payload_map["Temperature_F"])
    print current_temperature
    print threshold_temperature
    print switch.status()
    if current_temperature > threshold_temperature:
	if switch.status() is "0":
            switch.on()
            print "Turn on the air conditioner."
            my_email_module.send_email("Current temperature is bigger than threshold temperature, so air Conditioner was just turned on.")
        elif switch.status() is "1":
            print "It is already on"
    if current_temperature < threshold_temperature:
	if switch.status() == 1:
            switch.off()
            print "Turn off the air conidtioner."
            my_email_module.send_email("Current temperature is smaller than threshold temperature, so air Conditioner was just turned off.")
    myAWSIoTMQTTClient.publish("sdk/test/Python", json.dumps(payload_map), 1)
    print json.dumps(payload_map)
    loopCount += 1
    time.sleep(10)
