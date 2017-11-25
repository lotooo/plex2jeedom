#
# Author: Matthieu Serrepuy <https://github.com/lotooo>
#
# App to stop/start jeedom scenarii via the Plex webhooks
# https://support.plex.tv/hc/en-us/articles/115002267687-Webhooks  
#
import os
import sys
import json
import yaml
import requests
from flask import Flask, abort, request

##################################
# ENV variables
##################################

try:
    flask_port = os.environ['FLASK_PORT']
except:
    flask_port = 5001

try:
    flask_debug = os.environ['FLASK_DEBUG']
except:
    flask_debug = False

####################################
# MANDATORY : The Jeedom Host 
####################################
try:
    jeedom_host = os.environ['JEEDOM_HOST']
except:
    print('Unknown Jeedom. Please set it via env variable JEEDOM_HOST')
    sys.exit(1)

####################################
# MANDATORY : The Jeedom API key
####################################
try:
    jeedom_api = os.environ['JEEDOM_API']
except:
    print('Unknown Jeedom API. Please set it via env variable JEEDOM_API')
    sys.exit(1)

def open_scenarii_mapping_config():
    """
    Read the yaml configuration file
    Containing the player uuid with 
    scenario mapping per events
    """
    app.logger.info("Loading scenarii mapping from %s" % os.environ['SCENARIO_MAPPING_YAML'])
    with open(os.environ['SCENARIO_MAPPING_YAML'], 'r') as f:
        jeedom_scenarii = yaml.load(f)
    app.logger.info("%d plex clients managed to trigger jeedom" % len(jeedom_scenarii.keys()))

    return jeedom_scenarii


def start_jeedom_scenario(scenario_id):
    """ Start a specific scenario """
    # Source: https://github.com/jeedom/core/blob/stable/doc/fr_FR/api_http.asciidoc
    # http://#IP_JEEDOM#/core/api/jeeApi.php?apikey=#APIKEY#&type=scenario&id=#ID#&action=#ACTION#
    url = "https://%s/core/api/jeeApi.php" % jeedom_host
    parameters = {
        "apikey"   : jeedom_api,
        "type"      : "scenario",
        "action"    : "start",
        "id"        : scenario_id
    }
    r = requests.get(url, params=parameters)
    if r.status_code == 200:
        return "Scenario %d started" % scenario_id
    else:
        return "Error starting scenario %d" % scenario_id

app = Flask(__name__)

@app.route("/", methods=['POST'])
def scene_root():
    # read the json webhook
    data = request.form

    try:
        webhook = json.loads(data['payload'])
    except:
        app.logger.error("No payload found")
        abort(400)

    app.logger.debug(webhook)

    # Extract the event
    try:
        event = webhook['event']
    except KeyError:
        app.logger.info("No event found in the json")
        return "No event found in the json"

    # Extract the player uuid
    try:
        player_uuid = webhook['Player']['uuid']
    except:
        app.logger.info("No player uuid found")
        return 'No player found. No action taken'

    scenarii_mapping = open_scenarii_mapping_config()
    client = scenarii_mapping.get(player_uuid)

    if not client:
        app.log.info("Client %s is not managed. Ignoring the webhook" % player_uuid)
        return "Nothing to do"
    
    scenario_id = client.get(event)
    if not scenario_id:
        app.log.info("No jeedom scenario for event %s on client %s" % (event, client))
        return "Nothing to do"

    app.logger.info("Client %s requested to start scenario %d in jeedom (%s)" % (player_uuid, scenario_id, event))
    return start_jeedom_scenario(scenario_id)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=flask_port, debug=flask_debug)
