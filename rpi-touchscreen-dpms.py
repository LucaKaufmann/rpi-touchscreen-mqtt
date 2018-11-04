#!/usr/bin/env python
import time
import paho.mqtt.client as mqtt
import rpi_backlight as bl
from urllib.request import urlopen
from urllib.error import URLError
import subprocess
from ft5406 import Touchscreen, TS_PRESS

currentState = 'on'

ts = Touchscreen()

def touch_handler(event, touch):
    global currentState
    if event == TS_PRESS:
        currentState = 'on'

for touch in ts.touches:
    touch.on_press = touch_handler

ts.run()
subprocess.call("DISPLAY=:0 xset s 1200 1200", shell=True)


# Workaround
def wait_for_internet_connection():
    while True:
        try:
            response = urlopen('https://google.com',timeout=1)
            return
        except URLError:
            pass

def on_connect(client, userdata, flags, rc):
    if rc==0:
        client.connected_flag=True #set flag
        client.subscribe("dashboard/rpi1/set")
    else:
        print("Bad connection Returned code=",rc)
    

def on_message(client, userdata, msg):
    payload = str(msg.payload.decode("utf-8"))
    topic = msg.topic
    global currentState
    print("Received message '" + payload + "' on topic '"
        + topic + "' with QoS " + str(msg.qos))

    if topic == 'dashboard/rpi1/set':
        print("Set message received")
        values = payload.split(',')
        state = values[0]
        if state == 'on':
            subprocess.call("DISPLAY=:0 xset s reset", shell=True)
            subprocess.call("export DISPLAY=':0' | WID=$(xdotool search --onlyvisible --class chromium|head -1) | xdotool windowactivate ${WID} | xdotool key ctrl+F5", shell=True)
            currentState = state
        else:
            subprocess.call("DISPLAY=:0 xset s activate | DISPLAY=:0 xset dpms force off", shell=True)
            currentState = state
        if len(values) > 1:
            if values[1] != "":
                brightness = int(values[1])
                bl.set_brightness(brightness)
        getStatus()
 
def getStatus():
    topic = "dashboard/rpi1/status"
    global currentState
    brightness = bl.get_actual_brightness()
    payload = currentState+","+str(brightness)
    print("Publishing " + payload + " to topic: " + topic + " ...")
    client.publish(topic, payload, 0, True)

wait_for_internet_connection()
mqtt.Client.connected_flag=False#create flag in class
broker="BROKER_URL"
client = mqtt.Client("dashboard") 
client.username_pw_set('USER', 'PW')            #create new instance 
client.on_connect=on_connect  #bind call back function
client.on_message=on_message
client.loop_start()
print("Connecting to broker ",broker)
client.connect(broker)      #connect to broker
while not client.connected_flag: #wait in loop
    print("In wait loop")
    time.sleep(1)
while 1:
    try:
        getStatus()

    except Exception as e:
        print("exception")
        log_file=open("log.txt","w")
        log_file.write(str(time.time())+" "+e.__str__())
        log_file.close()

    print("")
    time.sleep(10)
