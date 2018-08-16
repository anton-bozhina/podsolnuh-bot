import vk
import json
import os
from flask import Flask, jsonify, make_response, request
from datetime import datetime

app = Flask(__name__)
log = app.logger


@app.route('/')
def homepage():
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>Test It is currently {time}.</p>

    <img src="http://loremflickr.com/600/400" />
    """.format(time=the_time)


@app.route(os.environ.get('HOOK_URL_DIALOGFLOW', '/webhook'), methods=['POST'])
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

        log.error(fulfillment_messages)

        # Compose the response to Dialogflow
        res = {'fulfillmentText': fulfillment_messages[0].format('Test Song!')}
        log.error(res)
    else:
        # If the request is not to the translate.text action throw an error
        log.error('Unexpected action requested: %s', json.dumps(req))
        res = {'speech': 'error', 'displayText': 'error'}

    return make_response(jsonify(res))


if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)

