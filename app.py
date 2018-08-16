# -*- coding: utf8 -*-
""" Podsolnuh Bot v. 0.0 """

import os
from datetime import datetime
import vk
from flask import Flask, jsonify, make_response, request
from hooks.dialogflow import dialog_flow
from hooks.addtrack import add_track

APP = Flask(__name__)
LOG = APP.logger


@APP.route('/')
def homepage():
    """ Домашняя страница """
    the_time = datetime.now().strftime("%A, %d %b %Y %l:%M %p")

    return """
    <h1>Hello heroku</h1>
    <p>It is currently {time}.</p>
    """.format(time=the_time)


@APP.route('/webhook/{}/dialogflow'.format(os.environ.get('HOOK_URL', 'not-secure')), methods=['POST'])
def dialogflow():
    """ Обработка и ответ хука от DialogFlow """

    return make_response(jsonify(dialog_flow(request.get_json(force=True), LOG)))


@APP.route('/webhook/{}/addtrack'.format(os.environ.get('HOOK_URL', 'not-secure')))
def addtrack():
    """ Обработка запроса на добавление трека """

    if 'track' in request.args:
        return add_track(request.args.get('track', type=str))
    else:
        return 'Args is Empty'


if __name__ == '__main__':
    APP.run(debug=True, use_reloader=True)
