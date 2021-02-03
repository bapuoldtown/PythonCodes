import psycopg2
from config import config
import json

import redis

def connect():
    """ Connect to the PostgreSQL database server """
    conn = None
    red=redis.Redis()
    try:
        # read connection parameters
        params = config()

        # connect to the PostgreSQL server
        print('Connecting to the PostgreSQL database...')
        print(type(params))
        print({**params})
        conn = psycopg2.connect(**params)
		
        # create a cursor object
        cur = conn.cursor()
        
	# execute a selecet statement and push to redis cache as write back methods
        print('PostgreSQL database version:')
        cur.execute('SELECT version()')
        orderslist=[]

        # display the PostgreSQL database server version
        db_version = cur.fetchone()
        print(db_version)

        #cur.execute("select column_name from information_schema.columns where table_name = 'company'")
        print('Fetching the rows of the rows')
        cur.execute('SELECT info from orders')
        for row in cur.fetchall():
            orderslist.append(row)
        order_list_str=json.dumps(orderslist)
        #code writes into the redis server using a key called allorders :)
        red.set('allorders',order_list_str)
        #Write to Redus queue
        red.mset({"orderslist":str(orderslist[0])})

       
	# close the communication with the PostgreSQL
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            print("Connection is successful Bhai")
            conn.close()
            print('Database connection closed.')


if __name__ == '__main__':
    connect()
