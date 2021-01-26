import os
import numpy as np
import psycopg2
import psycopg2.extras as extras
from config import config

def execute_values(df, table):
    """
    Using psycopg2.extras.execute_values() to insert the dataframe
    """
    # read database configuration
    params = config()
    # connect to the PostgreSQL database
    conn = psycopg2.connect(**params)
    # Create a list of tupples from the dataframe values
    tuples = [tuple(x) for x in df.to_numpy()]
    # Comma-separated dataframe columns
    cols = ','.join(list(df.columns))
    # SQL query to execute
    query = "INSERT INTO %s(%s) VALUES %%s" % (table, cols)
    cur = conn.cursor()
    try:
        extras.execute_values(cur, query, tuples)
        conn.commit()
    except (Exception, psycopg2.DatabaseError) as error:
        print("Error: %s" % error)
        conn.rollback()
        cur.close()
        return 1
    print("execute_values() done")
    cur.close()

def filter_auctions(id_list, df):
    df_clean = df[df.item.isin(id_list)]
    return df_clean