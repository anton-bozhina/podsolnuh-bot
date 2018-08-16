# -*- coding: utf8 -*-
""" Podsolnuh Bot v. 0.0 """

import json
import os
from datetime import datetime
import vk
from flask import Flask, jsonify, make_response, request

APP = Flask(__name__)
LOG = APP.logger


@APP.route('/')
def homepage():
    """Generate default page"""
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    """.format(time=the_time)


@APP.route(os.environ.get('HOOK_URL_DIALOGFLOW', '/webhook'), methods=['POST'])
def webhook():
    """This method handles the http requests for the  Dialogflow webhook
    This is meant to be used in conjunction with the translate Dialogflow agent
    """

    # Get request parameters
    req = request.get_json(force=True)
    action = req.get('queryResult').get('action')

    # Check if the request is for the translate action
    if action == 'playsong':
        # Get the parameters for the translation
        fulfillment_messages = req['queryResult']['fulfillmentMessages'][0]['text'].get('text')

        LOG.error(fulfillment_messages)

        # Compose the response to Dialogflow
        res = {'fulfillmentText': fulfillment_messages[0].format('Test Song!')}
        LOG.error(res)
    else:
        # If the request is not to the translate.text action throw an error
        LOG.error('Unexpected action requested: %s', json.dumps(req))
        res = {'speech': 'error', 'displayText': 'error'}

    return make_response(jsonify(res))


if __name__ == '__main__':
    APP.run(debug=True, use_reloader=True)
