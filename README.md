# rpi-touchscreen-mqtt
This Python script is intended to be run as a service and allows you to control a screen/touchscreen via MQTT. It can directly be added as an MQTT Light in Home Assistant, allowing it to be used in automations and scripts.
![MQTT Light Example](https://github.com/LucaKaufmann/rpi-touchscreen-mqtt/raw/master/images/mqtt_light.png)

# Setup

## Requirements
* Raspberry Pi connected to a screen or touchscreen (official 7" touchscreen for example).
* [python-multitouch](https://github.com/pimoroni/python-multitouch)
* xscreensaver installed
* [rpi-backlight](https://github.com/linusg/rpi-backlight)

## Steps
1. Install python-multitouch, [installation instructions](https://github.com/pimoroni/python-multitouch)
2. Install xscreensaver, ```sudo apt-get install xscreensaver ```
3. Install rpi-backlight , ```pip install rpi_backlight```
4. Clone this repository on your raspberry pi
5. Edit rpi-touchscreen.py, replace BROKER_URL, MQTT_USER, MQTT_PASSWORD
6. Run sh start-touchscreen.sh

## Run as a service
rpi-touchscreen can be run as a service on boot:

Create a new file in /etc/systemd/system, for example (adjust path to start-touchscreen.sh):
```sudo nano /etc/systemd/system/touchscreen.service```

```
[Unit]
Description=Touchscreen service
Requires=network-online.target
Wants=network-online.target
After=network-online.target

[Service]
ExecStart=/path/to/start-touchscreen.sh
StandardOutput=null
StandardOutput=syslog
StandardError=syslog
SyslogIdentifier=IMS
User=pi

[Install]
WantedBy=multi-user.target
Alias=touchscreen.service
```

* ```sudo systemctl daemon-reload```
* ```sudo systemctl enable touchscreen.service```
* ```sudo systemctl start touchscreen.service```

# Example usage

