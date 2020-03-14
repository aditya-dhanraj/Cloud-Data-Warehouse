import configparser
import psycopg2
from sql_queries import count_table_queries

def execute_results(cur, conn):
    
    '''executes analytical queries to count no. of rows in each table 
    '''  
    print('Getting Results....')
    for query in count_table_queries:
        cur.execute(query)
        results = cur.fetchone()

        for row in results:
            print("  ", row)
            

def main():
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    execute_results(cur, conn)
 
    conn.close()


if __name__ == "__main__":
    main()