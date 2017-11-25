plex2jeedom
==============

plex2jeedom is a small python app based on Flask acting as proxy between Plex Media Server webhooks and Jeedom.
It starts a specific scenario based on the player uuid + the event received

Based on:
* Flask : http://flask.pocoo.org/

# Installation

## CLI

```
git clone https://github.com/lotooo/plex2jeedom.git
cd plex2jeedom
pip install -r requirements.txt
```

## Docker
```
git clone https://github.com/lotooo/plex2jeedom.git
cd plex2jeedom
docker build . -t lotooo/plex2jeedom
```

## Dockerhub&
```
docker pull lotooo/plex2jeedom
```

# Environment variables
Name|Usage|Mandatory
----|-----|---------
JEEDOM_HOST|Host of your jeedom|Mandatory
JEEDOM_API|API key for jeedom|Optional
SCENARIO_MAPPING_YAML|Path to the yaml configuration file|Optional (default to /config/plex2jeedom.yml)
FLASK_PORT|Port flask should listen on|Optional
FLASK_DEBUG|Start flask in debug mode|Optional

# Usage

## CLI

```
export JEEDOM_HOST=jeedom.toto.com
export JEEDOM_API=xxxxxxxxxxxxxxxxxxxxxx
python plex2jeedom.py
```

## Docker
```
sudo docker run -d --name plex2hue-relay \
    -p 5001:5001 \
	-e JEEDOM_HOST=jeedom.toto.com \
	-e JEEDOM_API=xxxxxxxxxxxxxxxxxxxxxx \
    lotooo/plex2jeedom
```

# Configuration

The mapping between client uuid+event and scenario is done in the `plex2jeedom.yml`

Example:
```
yyyyyyyxxxxxxxxx: # player uuid
  media.play: 6 # scenario id
  media.resume: 6
  media.pause: 7
  media.stop: 7
```
