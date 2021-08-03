# ETL Pipeline for project Sparkify

## Analytical Database

Sparkify needs to analyze the users interaction with the platform in terms of songs played, time spent in the platform, logon/ logoff and others related. In order to do so, we need to create an analytical database that allows the Data team to perform analytical queries without interfering with the company activities. 
For this purpose, we are creating an ETL pipeline that extracts data from the application and web logs and ingest the data into a Redshift cluster (from now on, the Data Warehouse  or DWH).
The approach chose is to run an Extraction from the logs (stored in S3) into staging tables created in Redshift. 
Then a second step is executed where the data is transformed and inserted into a Star data model that can be used to perform queries in an efficient way.


## Database Schema Design 
To build the schema we have chose a star model approach including the following tables:

- songplays 
- users 
- songs 
- artists 
- time

Songplays is the main fact table, since Sparkify is primarily interested in understanding user preferences regarding songs, which translates into plays. 
The remainder tables are all dimension tables needed to understand those song plays. 


## Copy command to insert S3 files into Redshift. Important: Follow these instructions to run the project
 
 There are two main ways to provide credentials in the copy command. The first one (recommended) is by means of an IAM role:

     copy [table_name] from 's3://[bucket_name]/[folder_name]' credentials 'aws_iam_role=[IAM role]' json 's3://[bucket_name]/[folder_name]/[json_path_file.json]';


You could also provide access_key_id and secret_access_key in the following way: 

    copy [table_name]
    FROM
    's3://<bucketname>/<bucketfolder>'
    access_key_id '<access-key>' secret_access_key '<secret-key>' json 's3://[bucket_name]/[folder_name]/[json_path_file.json]'

 
The JSON path file is very important, otherwise the COPY command fails. 
Now, there is a JSON path file provided for the log file ('s3://udacity-dend/log_json_path.json') but I couldn't find one for the song files, so I created one (provided in the environment folder of the submission as 'log_json_path.json' and uploaded it to my S3 bucket. 
To be able to test all this, you need to add an additional setting in dwh.cfg under the S3 section, called SONG_JSONPATH and I have set it to the final location of the file in my S3 bucket. Make sure the cluster region and the S3 bucket region are one and the same or you will get an error. 
For reference, here is the complete contents of the dwh.cfg file: 

[AWS]
KEY=*****
SECRET=*****


[CLUSTER] 
HOST=[Cluster location as read in the AWS Console]
DB_NAME=DB Name provided when creating the cluster
DB_USER=User Name to access the cluster
DB_PASSWORD=*******
DB_PORT=Port used to access the cluster

[IAM_ROLE]
ARN=Role created to allow Redshift access to S3, in the form: arn:aws:iam::XXXXXX:role/[RoleName]


[S3]
LOG_DATA='s3://udacity-dend/log_data'
LOG_JSONPATH='s3://udacity-dend/log_json_path.json'
SONG_DATA='s3://udacity-dend/song_data'
SONG_JSONPATH=Path to the JSON Path for the songs data files


DWH_CLUSTER_TYPE=multi-node
DWH_NUM_NODES=4
DWH_NODE_TYPE=dc2.large
DWH_IAM_ROLE_NAME=[Role Name]



## Insert commands 

Redshift does not provide the UPSERT functionality included in PostgreSQL with the ON CONFLICT clause, so the insert/ update commands need to be done manually, generating a transaction that deletes records that exist in the staging table, and then re-inserting them. I have not included this functionality since this is a one-time insertion and the tables of the star model always start empty. 



