import configparser
import psycopg2
from sql_queries import drop_table_queries, create_table_queries, copy_table_queries, insert_table_queries

#Added a function to drop the staging tables
def drop_tables(cur, conn):
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()

#Added a function to create the tables
def create_tables(cur, conn):
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()

        

def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        cur.execute(query)
        conn.commit()


def insert_tables(cur, conn):
    for query in insert_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    drop_tables(cur, conn)
    create_tables(cur, conn)
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()