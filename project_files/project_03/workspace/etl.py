import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries


'''
Load data into the staging tables created in create_tables.py
'''
def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()

'''
Transform data read from the staging tables and insert into the production tables
'''
def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()

'''
Entry point used to execute stand-alone: Read config + Create connection and cursor object + 
call staging and insert functions
'''
def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()