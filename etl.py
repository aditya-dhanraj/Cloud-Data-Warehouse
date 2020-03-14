import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries

#Executes Query for loading data from json file of s3 to staging table.

print('Inserting Data from json file stored in s3 to staging tables')
def load_staging_tables(cur, conn):
    for query in copy_table_queries:
        print('Executing' + query + ' ')
        cur.execute(query)
        conn.commit()
        
# Executes Query for loading data from Staging tables to Analytical Table(Star Schema).

def insert_tables(cur, conn):
    print('Inserting data from staging tables to analytical table')
    for query in insert_table_queries:
        print('Executing' + query + ' ')
        cur.execute(query)
        conn.commit()


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