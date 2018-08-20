# -*- coding: utf8 -*-

import sqlite3

DATABASE = 'podsolnuh.db'

# SELECT * FROM tracks where played <= datetime('now', '-1 day')

# SELECT * FROM tracks WHERE played BETWEEN '20.08.2018 17:00' AND '20.08.2018 18:00'


def add_track(track):
    if (track != ''):
        with sqlite3.connect(DATABASE) as tracks_db:
            tracks_db.set_trace_callback(print)
            cursor = tracks_db.cursor()

            # получаем новый трек
            new_title = track

            # получаем самый последний трек
            cursor.execute('SELECT * FROM tracks ORDER BY ROWID DESC LIMIT 1')
            # print(cursor.fetchone())

            try:
                last_title = cursor.fetchone()['title']
            except TypeError:
                last_title = ''

            # Добавляем новый трек, только если последний не он же
            if new_title != last_title:
                cursor.execute("""
                INSERT INTO tracks (title) VALUES (?)
                """, [new_title, ])
                tracks_db.commit()

            # Проверка на старые записи
            cursor.execute("""
            DELETE FROM tracks where played <= datetime('now', '-1 hour')
            """)

            return 'track add'
    else:
        return 'empty'


def get_all_tracks():
    with sqlite3.connect(DATABASE) as tracks_db:
        tracks_db.set_trace_callback(print)
        cursor = tracks_db.cursor()
        cursor.execute('SELECT * FROM tracks')

        try:
            list = cursor.fetchall()
            return('</br>'.join('<strong>[{}]</strong>: {}'.format(x[0], x[1]) for x in list))
        except:
            return ''

