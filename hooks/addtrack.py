# -*- coding: utf8 -*-

import os
import json
from datetime import datetime
from pytz import timezone

TRACK_FILE = 'trackfile.json'


def add_track(track):
    # устанавливаем временную зону
    server_timezone = timezone('Europe/Moscow')

    # будем работать только если есть трек
    if ( track != '' ) :
        if not os.path.exists(TRACK_FILE):
            with open(TRACK_FILE, 'w'): pass

        with open(TRACK_FILE, 'r+') as json_file:
            try:
                # если можно, то загружаем данные
                trackfile = json.load(json_file)
            except ValueError:
                # если что то пошло не так, то создаем новые данные
                trackfile = {}

        # получаем текущее время
        time_now = server_timezone.localize(datetime.now()).timestamp()
        # получаем новый трек
        new_track = track
        # получаем самый последний трек
        try:
            last_track = trackfile[list(trackfile)[-1]]['track']
        except IndexError:
            last_track = ''

        # получаем время первой запись в файле
        try:
            first_time = float(list(trackfile)[0])
        except IndexError:
            first_time = time_now


        # Добавляем новый трек, только если последний не он же
        if last_track != new_track:
            trackfile[str(time_now)] = {}
            trackfile[str(time_now)]['track'] = new_track

        # 24 часа = 86400
        # 1 час = 3600

        # Проверка на старые записи
        while time_now - first_time >= 3600:
            # если есть старая запись, удаляем и смотрим дальше
            trackfile.pop(list(trackfile)[0])
            first_time = float(list(trackfile)[0])

        # сохраняем треклиск в файл
        with open(TRACK_FILE, 'w') as json_file:
            json_file.write(json.dumps(trackfile, sort_keys=True, indent=4))

        return 'track add'
    else:
        return 'empty'
