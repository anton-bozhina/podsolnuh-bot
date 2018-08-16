# -*- coding: utf8 -*-

import os
import json
from datetime import datetime
from pytz import timezone

TRACK_FILE = 'trackfile.json'


def get_track_json():
    if not os.path.exists(TRACK_FILE):
        with open(TRACK_FILE, 'w'): pass

    with open(TRACK_FILE, 'r+') as json_file:
        try:
            # если можно, то загружаем данные
            trackfile = json.load(json_file)
        except ValueError:
            # если что то пошло не так, то создаем новые данные
            trackfile = {}

    return str(json.dumps(trackfile, sort_keys=True, indent=4, separators=(',</br>', ': ')))