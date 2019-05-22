#!/usr/bin/python3
#-*-coding: utf-8-*-
import datetime
import json
import os
import re
import socket

import paho.mqtt.client as mqtt


def incoming_call(client, topic, _date, _time, _line, _nmbr, _mesg, _name):
    print("call", _date, _time, _line, _nmbr, _mesg, _name)
    data = {"date": _date,
            "time": _time,
            "line": _line,
            "nmbr": _nmbr,
            "mesg": _mesg,
            "name": _name,
            }
    d = datetime.datetime(int(_date[4:8]), int(_date[0:2]), int(_date[2:4]),
                        int(_time[0:2]), int(_time[2:4]))
    now = datetime.datetime.now()
    print(data)
    delta = abs(now - d)
    if delta.seconds < 120:
        client.publish(topic, json.dumps(data))
        print("published")
    else:
        print("delta too large, timestamp:", d, "now:", now)

def incoming_ring(client, topic, _line, _ring, _time):
    print("ring", _line, _ring, _time)
    data = {"line": _line,
            "ring": _ring,
            "time": _time,
            }
    client.publish(topic, json.dumps(data))

actions = [
    (re.compile(
     r'^[PC]ID: '
     r'\*DATE\*(\d{8})'
     r'\*TIME\*(\d{4})'
     r'\*LINE\*([^*]+)'
     r'\*NMBR\*([^*]+)'
     r'\*MESG\*([^*]+)'
     r'\*NAME\*([^*]+)'
     r'\*$')
     , incoming_call),
    (re.compile(
     r'^CIDINFO: '
     r'\*LINE\*([^*]+)'
     r'\*RING\*([^*]+)'
     r'\*TIME\*([^*]+)'
     r'\*$')
     , incoming_ring),
]

def main():
    ncid_host = os.getenv('NCID_HOST')
    ncid_port = int(os.getenv('NCID_PORT', 3333))
    mqtt_host = os.getenv('MQTT_HOST')
    mqtt_port = int(os.getenv('MQTT_PORT', 1883))
    mqtt_topic = os.getenv('MQTT_TOPIC')
    mqtt_username = os.getenv('MQTT_USER', None)
    mqtt_password = os.getenv('MQTT_PASSWORD', None)

    while True:
        client = mqtt.Client()
        if mqtt_username:
            client.username_pw_set(mqtt_username, mqtt_password)
        client.connect(mqtt_host,
                       mqtt_port,
                       60)
        client.loop_start()
        s = socket.socket()
        try:
            s.connect((ncid_host, ncid_port))
            print("connected")
            while True:
                data = s.recv(1024).decode().strip()
                print(data)
                for regex, func in actions:
                    match = regex.match(data)
                    if match:
                        func(client, mqtt_topic, *match.groups())
        except Exception as E:
            raise E
        finally:
            s.close()
            client.disconnect()

if __name__ == "__main__":
    main()
