--https://panoply.io/data-warehouse-guide/redshift-etl/
INSERT INTO songplays(userid, level, songid, artistid, sessionid, location, user_agent)
    SELECT 
    (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second'), --starttime
    dse.userId, --userid
    dse.level, --level
    dss.song_id, --songid
    dss.artist_id, --artistid
    dse.sessionId, --sessionid
    dse.location, --location
    dse.userAgent --user_agent
    FROM dwh.staging_events dse
    INNER JOIN dwh.staging_songs dss
    ON dse.song = dss.title
    WHERE dse.page = "NextSong"

INSERT INTO users(user_id, first_name, last_name, gender, level)
SELECT DISTINCT
dse.userId, --user_id
dse.firstName, --first_name
dse.lastName, --last_name
dse.gender, --gender
dse.level --level
FROM dwh.staging_events dse
ORDER BY (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second') ASC
ON CONFLICT (user_id)
    DO UPDATE
    SET level = EXCLUDED.level;
    
    
INSERT INTO songs(song_id, title, artist_id, year, duration)
SELECT DISTINCT
dss.song_id, 
dss.title, 
dss.artist_id, 
dss.year, 
dss.duration
FROM dwh.staging_songs dss

INSERT INTO artists(artist_id, name, location, latitude, longitude)
SELECT DISTINCT
dss.artist_id, 
dss.artist_name, 
dss.artist_location, 
dss.artist_latitude, 
dss.artist_longitude
FROM dwh.staging_songs dss
ON CONFLICT (artist_id)
    DO UPDATE
    SET (location = EXCLUDED.artist_location, 
    latitude = EXCLUDED.artist_latitude, 
    longitude = EXCLUDED.artist_longitude) 



INSERT INTO time(start_time, hour, day, week, month, year, weekday)
SELECT DISTINCT
dse.ts, 
extract(hour from (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second')), 
extract(day from (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second')), 
extract(week from (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second')), 
extract(month from (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second')), 
extract(year from (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second')), 
extract(dayofweek from (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second'))
FROM dwh.staging_events dse


    
    
    select cast(to_char((timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second'), 'HH24:MI:SS') as time) from staging_events dse
    
    select (timestamp 'epoch' + CAST(dse.ts AS BIGINT)/1000 * interval '1 second') from staging_events dse
