ncid-mqtt-relay
===============

Requirements
------------

* NCIDD server running and connected to a modem or SIP.
* MQTT server
* Home Assistant (optional)

Installation
------------

Using Docker:

```
docker run -e NCID_HOST=192.168.0.4 -e NCID_PORT=3333 -e MQTT_HOST=mqtt.example.com -e MQTT_PORT=1883 -e MQTT_TOPIC=/ncid/0800999999/ -e MQTT_USER=mqtt -e MQTT_PASSWORD=YOURPASSWORD hairychris2/ncid-mqtt-relay
```

Using Docker-Compose:

```
ncid-mqtt-relay:
    image: hairychris2/ncid-mqtt-relay
    environment:
        - NCID_HOST=192.168.0.4
        - NCID_PORT=3333
        - MQTT_HOST=mqtt.example.com
        - MQTT_PORT=1883
        - MQTT_TOPIC=/ncid/0800999999/
        - MQTT_USER=mqtt
        - MQTT_PASSWORD=YOURPASSWORD
        - TZ=Europe/London
    logging:
      driver: "json-file"
      options:
        max-file: "5"
        max-size: "10m"
    volumes:
        - /etc/timezone:/etc/timezone:ro
        - /etc/localtime:/etc/localtime:ro

```

Or you can go old school and run it on your machine:

```
    export NCID_HOST=192.168.0.4
    export NCID_PORT=3333
    export MQTT_HOST=mqtt.example.com
    export MQTT_PORT=1883
    export MQTT_TOPIC=/ncid/0800999999/
    export MQTT_USER=mqtt
    export MQTT_PASSWORD=YOURPASSWORD
    pipenv install -r requirements.txt
    pipenv run python3 src/ncid-relay.py
```

Usage
-----

You can configure a sensor under Home Assistant, add this to configuration.yaml:

```
sensor:
  - platform: mqtt
    state_topic: "ncid/0800999999"
    value_template: "{{ value_json.name }} on {{ value_json.nmbr }}"
```
