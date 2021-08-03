import configparser


# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS songplays"
user_table_drop = "DROP TABLE IF EXISTS users"
song_table_drop = "DROP TABLE IF EXISTS songs"
artist_table_drop = "DROP TABLE IF EXISTS artists"
time_table_drop = "DROP TABLE IF EXISTS time"

# CREATE TABLES

#Example data in events
#{"artist":"Tamba Trio","auth":"Logged #In","firstName":"Kaylee","gender":"F","itemInSession":4,"lastName":"Summers","length":177.18812,"level":"free","location":"Phoeni#x-Mesa-Scottsdale, AZ","method":"PUT","page":"NextSong","registration":1540344794796.0,"sessionId":139,"song":"Quem Quiser #Encontrar O Amor","status":200,"ts":1541106496796,"userAgent":"\"Mozilla\/5.0 (Windows NT 6.1; WOW64) AppleWebKit\/537.36 (KHTML, #like Gecko) Chrome\/35.0.1916.153 Safari\/537.36\"","userId":"8"}
staging_events_table_create= ("""
CREATE TABLE staging_events(
artist VARCHAR(256),
auth VARCHAR(32), 
firstName VARCHAR(256),
gender CHAR, 
itemInSession INTEGER, 
lastName VARCHAR(256), 
length FLOAT, 
level VARCHAR(16), 
location VARCHAR(128),
method VARCHAR(16), 
page VARCHAR(128),
registration FLOAT, 
sessionId INTEGER,
song VARCHAR(256), 
status INTEGER, 
ts BIGINT, 
userAgent VARCHAR(256),
userId INTEGER
);
""")

#Example data in songs: 
#{"num_songs": 1, "artist_id": "ARJIE2Y1187B994AB7", "artist_latitude": null, "artist_longitude": null, "artist_location": "", #"artist_name": "Line Renaud", "song_id": "SOUPIRU12A6D4FA1E1", "title": "Der Kleine Dompfaff", "duration": 152.92036, "year": 0}
staging_songs_table_create = ("""
CREATE TABLE staging_songs(
num_songs INTEGER,
artist_id VARCHAR(18), 
artist_latitude FLOAT, 
artist_longitude FLOAT, 
artist_location VARCHAR(256), 
artist_name VARCHAR(256),
song_id VARCHAR(18), 
title VARCHAR(256), 
duration FLOAT,
year INTEGER 
);
""")

#This is the fact table so I will distribute based on the joins needed for analysis 
#At this point User and Song seem to be the most probably used tables to join
#Focusing on user and using it as a dist key
songplay_table_create = ("""
CREATE TABLE songplays(
songplay_id INT IDENTITY(1, 1), 
start_time bigint not null, 
user_id integer not null sortkey distkey, 
level  varchar(16) not null,
song_id varchar(18) not null, 
artist_id varchar(18) not null,
session_id integer not null,
location varchar(128), 
user_agent varchar(256),
primary key(songplay_id)
)
;
""")

#Potentially there are many users, so distributing on user_id. A User_id exists in the logs already so there is no need to use 
#a serial. Also, making not null the values that I suppose are required
user_table_create = ("""
create table users(
user_id integer not null sortkey distkey, 
first_name varchar(256) not null, 
last_name varchar(256) not null, 
gender char, 
level varchar(16) not null,
primary key(user_id)
)
;
""")

#Similar considerations as the ones listed for the users table
song_table_create = ("""
create table songs(
song_id varchar(18) not null sortkey distkey, 
title varchar(256) not null, 
artist_id varchar(18) not null, 
year integer not null, 
duration float not null,
primary key(song_id)
)
;
""")

#There will be many artists, so I'm distributing on artist_id. This value is provided in the song json files
#so no need to use a serial. Applying not null in the required columns 
artist_table_create = ("""
create table artists(
artist_id char(18) not null sortkey distkey, 
name varchar(256) not null, 
location varchar(256), 
latitude float, 
longitude float,
primary key(artist_id)
)
;
""")

#This is a small tale, using distribution style
time_table_create = ("""
create table time( 
start_time bigint not null,
hour integer not null,
day integer not null,
week integer not null,
month integer not null,
year integer not null,
weekday integer not null,
primary key(start_time))
diststyle all;
""")

# STAGING TABLES

#Original line commented to parameterize
#staging_events_copy = ("""
#COPY staging_events FROM 's3://udacity-dend/log_data' credentials 'aws_iam_role={}' json 's3://udacity-dend/log_json_path.json'
#""").format(*config['IAM_ROLE'].values())

staging_events_copy = ("""
COPY staging_events FROM 's3://udacity-dend/log_data' credentials 'aws_iam_role={}' json {}
""").format(*config['IAM_ROLE'].values(), config.get('S3','LOG_JSONPATH'))


#Original line commented to parameterize
#staging_songs_copy = ("""
#COPY staging_songs FROM 's3://udacity-dend/song_data' credentials 'aws_iam_role={}' json 's3://mv-west-2-#bucket/song_json_path.json'
#""").format(*config['IAM_ROLE'].values())


staging_songs_copy = ("""
COPY staging_songs FROM 's3://udacity-dend/song_data' credentials 'aws_iam_role={}' json {}
""").format(*config['IAM_ROLE'].values(), config.get('S3','SONG_JSONPATH'))


# FINAL TABLES

songplay_table_insert = ("""
INSERT INTO songplays(start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
    SELECT 
    dse.ts, --starttime
    dse.userId, --userid
    dse.level, --level
    dss.song_id, --songid
    dss.artist_id, --artistid
    dse.sessionId, --sessionid
    dse.location, --location
    dse.userAgent --user_agent
    FROM staging_events dse
    INNER JOIN staging_songs dss
    ON dse.song = dss.title
    WHERE dse.page = 'NextSong'
""")

user_table_insert = ("""
INSERT INTO users(user_id, first_name, last_name, gender, level)
SELECT DISTINCT
dse.userId, --user_id
dse.firstName, --first_name
dse.lastName, --last_name
dse.gender, --gender
dse.level --level
FROM staging_events dse
where dse.userId is not null
ORDER BY dse.ts DESC
""")

song_table_insert = ("""
INSERT INTO songs(song_id, title, artist_id, year, duration)
SELECT DISTINCT
dss.song_id, 
dss.title, 
dss.artist_id, 
dss.year, 
dss.duration
FROM staging_songs dss
""")

artist_table_insert = ("""
INSERT INTO artists(artist_id, name, location, latitude, longitude)
SELECT DISTINCT
dss.artist_id, 
dss.artist_name, 
dss.artist_location, 
dss.artist_latitude, 
dss.artist_longitude
FROM staging_songs dss
""")

time_table_insert = ("""
INSERT INTO time(start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT
dse.ts, 
extract(hour from (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second')), 
extract(day from (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second')), 
extract(week from (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second')), 
extract(month from (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second')), 
extract(year from (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second')), 
extract(dayofweek from (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second'))
FROM staging_events dse
""")

# QUERY LISTS


create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_songs_copy, staging_events_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
