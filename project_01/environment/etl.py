import os
import glob
import importlib
import datetime
import psycopg2
import numpy as np
from psycopg2.extensions import register_adapter, AsIs
psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)
import codecs
import pandas as pd
pd.options.mode.chained_assignment = None # default='warn'

from sql_queries import *

def process_song_file(cur, filepath):
    
    #df = pd.read_json(filepath, lines=True) 
    #Added to prevent UTF-8 errors
    df = pd.read_json(codecs.open(filepath, 'r', 'utf-8'), lines=True)

    # insert song record
    for index, row in df.iterrows():
        song_data = [row['song_id'], row['title'], row['artist_id'], row['year'], row['duration']]
        cur.execute(song_table_insert, song_data)

        # insert artist record
        artist_data = [row['artist_id'], row['artist_name'], row['artist_location'], row['artist_latitude'], row['artist_longitude']]
        cur.execute(artist_table_insert, artist_data)


def process_log_file(cur, filepath):
    #open log file
    #df = pd.read_json(filepath, lines=True) 
    df = pd.read_json(codecs.open(filepath, 'r', 'utf-8'), lines=True)

    # filter by NextSong action
    df = df[df['page'] == 'NextSong']

    for index, row in df.iterrows():
        # convert timestamp column to datetime
        t = pd.to_datetime(row['ts'], unit='ms')
    
        # insert time data records
        time_data = [t, t.hour, t.day, t.month, t.week, t.year, t.weekday()]
        column_labels = ['start_time', 'hour', 'day', 'month', 'week', 'year', 'weekday']
        time_df = pd.DataFrame([time_data], columns = column_labels) 
        cur.execute(time_table_insert, time_df.iloc[0].values.tolist())

        # load user table
        user_data = [row["userId"],row["firstName"], row["lastName"], row["gender"], row["level"]] #selected_columns.copy()
        # insert user records
        cur.execute(user_table_insert, user_data)

        # insert songplay records
        # get songid and artistid from song and artist tables
        cur.execute(song_select, (row.song, row.artist, row.length))
        results = cur.fetchone()
        if results:
            songid, artistid = results
        else:
            songid, artistid = '', ''
        
        # insert songplay record
        songplay_data = [pd.to_datetime(row.ts, unit='ms'), row.userId, row.level, songid, artistid]
        cur.execute(songplay_table_insert, songplay_data)

            


def process_data(cur, conn, filepath, func):
    # get all files matching extension from directory
    all_files = []
    for root, dirs, files in os.walk(filepath):
        files = glob.glob(os.path.join(root,'*.json'))
        for f in files :
            all_files.append(os.path.abspath(f))

    # get total number of files found
    num_files = len(all_files)
    print('{} files found in {}'.format(num_files, filepath))

    # iterate over files and process
    for i, datafile in enumerate(all_files, 1):
        func(cur, datafile)
        conn.commit()
        print('{}/{} files processed.'.format(i, num_files))


def main():
    conn = psycopg2.connect("host=127.0.0.1 dbname=sparkifydb user=student password=student")
    cur = conn.cursor()

    process_data(cur, conn, filepath='data/song_data', func=process_song_file)
    process_data(cur, conn, filepath='data/log_data', func=process_log_file)

    conn.close()


if __name__ == "__main__":
    main()