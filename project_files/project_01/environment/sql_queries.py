# DROP TABLES

songplay_table_drop = "DROP TABLE IF EXISTS songplays;"
user_table_drop = "DROP TABLE IF EXISTS users;"
song_table_drop = "DROP TABLE IF EXISTS songs;"
artist_table_drop = "DROP TABLE IF EXISTS artists;"
time_table_drop = "DROP TABLE IF EXISTS time;"

# CREATE TABLES

songplay_table_create = ("""
    CREATE TABLE IF NOT EXISTS songplays (
    songplay_id SERIAL PRIMARY KEY,
    start_time timestamp without time zone NOT NULL,
    user_id integer NOT NULL,
    level varchar(40) NOT NULL,
    song varchar(18),
    artist varchar(18), 
    CONSTRAINT non_dupe
    UNIQUE (start_time, user_id, song)
    );    
""")

user_table_create = ("""
    CREATE TABLE IF NOT EXISTS users(
    user_id integer primary key,
    first_name varchar(40),
    last_name varchar(40),
    gender char(1),
    level varchar(40)
    );
""")

song_table_create = ("""
    CREATE TABLE IF NOT EXISTS songs(
    song_id varchar(18) primary key,
    title varchar(100),
    artist_id varchar(18),
    year int,
    duration float
    );
""")

artist_table_create = ("""
    CREATE TABLE IF NOT EXISTS artists(
    artist_id varchar(18) primary key,
    artist_name varchar(100),
    artist_location varchar(100),
    artist_latitude float,
    artist_longitude float
    );
""")

time_table_create = ("""
    CREATE TABLE IF NOT EXISTS time(
    start_time timestamp without time zone primary key,
    hour integer,
    minute integer,
    day integer,
    week integer,
    month integer,
    year integer,
    weekday integer
    );
""")

# INSERT RECORDS

songplay_table_insert = ("""
    INSERT INTO songplays(start_time, user_id, level, song, artist)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT ON CONSTRAINT non_dupe
    DO NOTHING;    
""")

user_table_insert = ("""
    INSERT INTO users(user_id, first_name, last_name, gender, level)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (user_id)
    DO UPDATE
    SET level = EXCLUDED.level;
    ;
""")

song_table_insert = ("""
    INSERT INTO songs(song_id, title, artist_id, year, duration)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (song_id)
    DO NOTHING;
""")

artist_table_insert = ("""
    INSERT INTO artists(artist_id, artist_name, artist_location, artist_latitude, artist_longitude)
    VALUES (%s, %s, %s, %s, %s)
    ON CONFLICT (artist_id)
    DO NOTHING;
""")


time_table_insert = ("""
    INSERT INTO time(start_time, hour, day, month, week, year, weekday)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    ON CONFLICT (start_time)
    DO NOTHING;
""")

# FIND SONGS

song_select = ("""
    SELECT songs.song_id, songs.artist_id
    FROM songs
    INNER JOIN artists
    ON songs.artist_id = artists.artist_id
    WHERE songs.title = %s 
    AND artists.artist_name = %s 
    AND songs.duration = %s;
""")

# QUERY LISTS

create_table_queries = [songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
insert_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]