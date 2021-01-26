import psycopg2
import sys
import boto3
from config import config

def connect():

    # gets the credentials from .aws/credentials
    session = boto3.Session(profile_name='LucasUrbisaia') # user from .aws/config file
    client = boto3.client('rds')

    # token = client.generate_db_auth_token(DBHostname=ENDPOINT, Port=PORT, DBUsername=USR, Region=REGION)
    conn = None

    try:
        # read connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()

        # display the PostgreSQL database server version
        print('Successfully connected to database. PostgreSQL database version:')
        cur.execute('SELECT version()')
        db_version = cur.fetchone()
        print(db_version)

        # close the communication with the PostgreSQL
        cur.close()

    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Database connection closed.')
