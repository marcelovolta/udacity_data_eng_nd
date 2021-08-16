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

To copy the JSON data there are two options: either we provide a JSON path file, or use the 'auto' option that requires names of columns match the name of JSON fields. In the Project Review feedback, it was suggested to use the 'auto' option in the Songs copy, while for the Events we are using the JSON path.  


## Insert commands 

Redshift does not provide the UPSERT functionality included in PostgreSQL with the ON CONFLICT clause, so the insert/ update commands need to be done manually, generating a transaction that deletes records that exist in the staging table, and then re-inserting them. I have not included this functionality since this is a one-time insertion and the tables of the star model always start empty. 



