import psycopg2
from config import config


def create_tables():
    """ create tables in the PostgreSQL database"""
    commands = (
        """
        CREATE TABLE blizz_ah_data (
            id INTEGER NOT NULL,
            item INTEGER NOT NULL,
            unit_price DECIMAL NOT NULL,
            quantity SMALLINT NOT NULL,
            TimeStamp TIMESTAMP NOT NULL,
            time_left VARCHAR(12) NOT NULL,
            PRIMARY KEY (id, TimeStamp)
        )
        """)
    conn = None
    try:
        # read the connection parameters
        params = config()
        # connect to the PostgreSQL server
        conn = psycopg2.connect(**params)
        cur = conn.cursor()
        # create table
        cur.execute(commands)
        # close communication with the PostgreSQL database server
        cur.close()
        # commit the changes
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
