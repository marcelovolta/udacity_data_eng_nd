# Project 01: Data Modeling with Postgre SQL 


## Contents

- data (folder): All the JSON files for songs and events (user activity)
- etl.ipynb: Jupyter notebook that includes all the ETL code used to develop the ETL methods 
- test.ipynb: Jupyter notebook containing all the tests to run on the data after executing the creation of tables and ETL process
- create_tables.py: Python implementation of the code needed to drop existing DB and recreate all the tables of the model
- etl.py: Python implementation of the ETL code demonstrated in etl.ipynb
- README.md: This file. Documentation of the project.
- sql_queries.py: Python module containign all the SQL strings used in the ETL process (imported in etl.ipynb and etl.py)

## Running the project

To run the project from scratch, make sure you have a postgre SQL instance running in the local host (a Docker image is recommended). The code tries a connection to postgre SQL with the following connection string: 

    "host=127.0.0.1 dbname=studentdb user=student password=student"

On the console or command prompt CD into the directory where the files are located and execute the following two commands: 

    $ python create_tables.py
    $ python etl.py
    
If the project runs successfully, you will see a message displaying the files inside data being processed


# Code Notes 

## Code in `etl.ipynb`


### Data Translation errors 
Added the following lines in etl.ipynb (first cell):
 
    import numpy as np
    from psycopg2.extensions import register_adapter, AsIs
    psycopg2.extensions.register_adapter(np.int64, psycopg2._psycopg.AsIs)

These are meant to prevent any problems in data translation from pandas (I was having the "can't adapt type 'numpy.int64'" error. 
 

 
### Pandas Warnings
To disable copy warnings in Pandas, I have added the following line, in etl.ipynb (first cell) since I'm overwriting references in the current project: 
 
    pd.options.mode.chained_assignment = None # default='warn'

### Process Song Data 
By selecting only one file as indicated in the instructions, we are limiting the possibility to add song plays later on, since we will only get song plays for the song selected (see below)

### `songs` Table 
There is no need to force the selection of only the first record since there is only record in the dataframe (we have forced this selection in the previous step already). The same note is valid for the `artists`table. 

### Process log data: `time` table
The process to create a list from a dataframe, then a dictionary and then a dataframe again seemed counter-intuitive. I achieved the same goal using a simple selection of columns from the original dataframe and then copying:

    selected_columns = filtered_df[["start_time","hour", "day", "month", "week", "year", 'weekday']]
    time_df = selected_columns.copy()
    
### `users` table
In this case I started form the filtered dataframe that includes only 'NextSong' actions, so that the users inserted are only the ones that played songs. This is because the current Star schema is meant to query songs played. 

### `songplays` table
In this case I only inserted a row if both songid, and artistid are non-null. 
The reason for this is that we are only inserting songs played. It follows these two ids can't be null for valid songplays.
As mentioned above, there are no records inserted because we took only the firt record from the song data. 
The code, however, runs without problems.


## Notes for `etl.py`

### File processing error
I have added the following line in the imports section to prevent errors when loading a JSON file UTF-8 encoded: 
    
    import codecs

Then, the JSON load line:
    
    df = pd.read_json(filepath, lines=True) 

Was changed to:

    df = pd.read_json(codecs.open(filepath, 'r', 'utf-8'), lines=True)

But even with this change, sometimes the file in question (which contains a song name in Spanish) was loaded successfully, and sometimes id didn't, so in the end, I deleted it in my local environment to allow for debugging and processing. 






 
