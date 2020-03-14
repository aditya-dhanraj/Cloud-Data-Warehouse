import configparser

# CONFIG
config = configparser.ConfigParser()
config.read('dwh.cfg')

'''Get Required Params from config(dwh.cfg) file
'''

ARN             = config.get('IAM_ROLE', 'ARN')
LOG_DATA        = config.get('S3', 'LOG_DATA')
LOG_JSONPATH    = config.get('S3', 'LOG_JSONPATH')
SONG_DATA       = config.get('S3', 'SONG_DATA')

# DROP TABLES

staging_events_table_drop = "DROP TABLE IF EXISTS staging_events cascade"
staging_songs_table_drop = "DROP TABLE IF EXISTS staging_songs"
songplay_table_drop = "DROP TABLE IF EXISTS fact_songplays"
user_table_drop = "DROP TABLE IF EXISTS dim_users"
song_table_drop = "DROP TABLE IF EXISTS dim_songs"
artist_table_drop = "DROP TABLE IF EXISTS dim_artists"
time_table_drop = "DROP TABLE IF EXISTS dim_time"

# CREATE TABLES

staging_events_table_create= ("""
CREATE TABLE IF NOT EXISTS staging_events (
    event_id               BIGINT IDENTITY(0,1) NOT NULL,
    artist                 VARCHAR,
    auth                   VARCHAR,
    firstName              VARCHAR,
    gender                 CHAR(1),
    itemInSession          INTEGER NOT NULL,
    lastName               VARCHAR,
    length                 FLOAT,
    level                  VARCHAR,
    location               VARCHAR,
    method                 VARCHAR,
    page                   VARCHAR,
    registration           FLOAT,
    sessionId              INTEGER SORTKEY DISTKEY,
    song                   VARCHAR,
    status                 INTEGER NOT NULL,
    ts                     TIMESTAMP,
    userAgent              VARCHAR,
    userId                 INTEGER
    );
""")

staging_songs_table_create = ("""
CREATE TABLE IF NOT EXISTS staging_songs(
    num_songs              INTEGER,
    artist_id              VARCHAR NOT NULL SORTKEY DISTKEY,
    artist_latitude        FLOAT,
    artist_location        VARCHAR,
    artist_longitude       FLOAT,
    artist_name            VARCHAR,
    duration               FLOAT,
    song_id                VARCHAR NOT NULL,
    title                  VARCHAR,
    year                   INTEGER 
);
""")

songplay_table_create = ("""
CREATE TABLE IF NOT EXISTS fact_songplays(
    songplay_id           INTEGER IDENTITY(0,1),
    start_time            TIMESTAMP SORTKEY,
    user_id               INTEGER   DISTKEY,
    level                 VARCHAR,
    song_id               VARCHAR,
    artist_id             VARCHAR,
    session_id            INTEGER,
    location              VARCHAR,
    user_agent            VARCHAR
);

""")

user_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_users(
    user_id                INTEGER DISTKEY SORTKEY,
    first_name             VARCHAR,
    last_name              VARCHAR,
    gender                 CHAR(1),
    level                  VARCHAR
);
""")

song_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_songs(
    song_id                VARCHAR SORTKEY,
    title                  VARCHAR,
    artist_id              VARCHAR,
    year                   INTEGER,
    duration               FLOAT

);
""")

artist_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_artists(
    artist_id              VARCHAR SORTKEY,
    name                   VARCHAR,
    location               VARCHAR,
    latitude               FLOAT,
    longitude              FLOAT
);
""")

time_table_create = ("""
CREATE TABLE IF NOT EXISTS dim_time(
    start_time             TIMESTAMP SORTKEY,
    hour                   INTEGER,
    day                    INTEGER,
    week                   INTEGER,
    month                  INTEGER,
    year                   INTEGER,
    weekday                INTEGER
);
""")

# STAGING TABLES

''' Query for Loading Data from s3 to staging Tables
'''
staging_events_copy = ("""
    copy staging_events from {}
    credentials 'aws_iam_role={}' 
    format as json {}
    STATUPDATE ON
    timeformat as 'epochmillisecs'
    region 'us-west-2';
""").format(LOG_DATA, ARN, LOG_JSONPATH)

staging_songs_copy = ("""
    copy staging_songs from {}
    credentials 'aws_iam_role={}'
    format as json 'auto'
    STATUPDATE ON
    region 'us-west-2';
""").format(SONG_DATA, ARN)

# FINAL TABLES

'''Query for Insering Data into Analytical Tables
'''
songplay_table_insert = ("""
    INSERT INTO fact_songplays
    (start_time, user_id, level, song_id, artist_id, session_id, location, user_agent)
        SELECT DISTINCT (se.ts) AS start_time,
            se.userId    AS user_id,
            se.level     AS level,
            ss.song_id   AS song_id,
            ss.artist_id AS artist_id,
            se.sessionId AS session_id,
            se.location  AS location,
            se.userAgent AS user_agent
        FROM staging_events se 
        JOIN staging_songs ss
        ON
            (se.artist = ss.artist_name)
        WHERE 
            page = 'NextSong';
""")

user_table_insert = ("""
    INSERT INTO dim_users
    (user_id, first_name, last_name, gender, level)
        SELECT DISTINCT 
            se.userId    AS user_id,
            se.firstName AS first_name,
            se.lastName  AS last_name,
            se.gender    AS gender,
            se.level     AS level
        FROM staging_events AS se
        WHERE user_id IS NOT NULL
        AND se.page = 'NextSong' ;
""")

song_table_insert = ("""
    INSERT INTO dim_songs
    SELECT 
        song_id,
        title,
        artist_id,
        year,
        duration
    FROM staging_songs 
    WHERE song_id IS NOT NULL;
""")

artist_table_insert = ("""
    INSERT INTO dim_artists
    SELECT distinct
        artist_id,
        artist_name      AS name, 
        artist_location  AS location,
        artist_latitude  AS latitude,
        artist_longitude AS longitude
    FROM staging_songs
    WHERE artist_id IS NOT NULL;
""")

time_table_insert = ("""
    INSERT INTO dim_time
    SELECT DISTINCT (start_time)         AS start_time,
        extract(hour from start_time)    AS  hour,
        extract(day from start_time)     AS  day,
        extract(week from start_time)    AS  week,
        extract(month from start_time)   AS  month,
        extract(year from start_time)    AS  year,
        extract(weekday from start_time) AS  weekday
    FROM fact_songplays
""")

# Analytical Query Result...

'''Query for getting Total no. of rows in each table
'''
count_query1 = ("""
    select count(*) from staging_events;
""")

count_query2 = ("""
    select count(*) from staging_songs;
""")

count_query3 = ("""
    select count(*) from fact_songplays;
""")

count_query4 = ("""
    select count(*) from dim_songs;
""")

count_query5 = ("""
    select count(*) from dim_users;
""")

count_query6 = ("""
    select count(*) from dim_artists;
""")

count_query7 = ("""
    select count(*) from dim_time;
""")

# QUERY LISTS

create_table_queries = [staging_events_table_create, staging_songs_table_create, songplay_table_create, user_table_create, song_table_create, artist_table_create, time_table_create]
drop_table_queries = [staging_events_table_drop, staging_songs_table_drop, songplay_table_drop, user_table_drop, song_table_drop, artist_table_drop, time_table_drop]
copy_table_queries = [staging_events_copy, staging_songs_copy]
insert_table_queries = [songplay_table_insert, user_table_insert, song_table_insert, artist_table_insert, time_table_insert]
count_table_queries = [count_query1, count_query2, count_query3, count_query4, count_query5, count_query6, count_query7]