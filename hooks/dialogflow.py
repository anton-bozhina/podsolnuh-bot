# -*- coding: utf8 -*-
""" WebHook for DialogFlow """

import json


def dialogflow_webhook(request, log):
    """    Функция отвечает за обработку и отправку данных DialogFlow     """

    action = request.get('queryResult').get('action')

    # Check if the request is for the translate action
    if action == 'playsong':
        # Get the parameters for the translation
        fulfillment_messages = request['queryResult']['fulfillmentMessages'][0]['text'].get('text')

        log.error(fulfillment_messages)

        # Compose the response to Dialogflow
        response = {'fulfillmentText': fulfillment_messages[0].format('Test Song!')}
        log.error(response)
    else:
        # If the request is not to the translate.text action throw an error
        log.error('Unexpected action requested: %s', json.dumps(request))
        response = {'speech': 'error', 'displayText': 'error'}

    return response
