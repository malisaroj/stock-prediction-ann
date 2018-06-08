import pandas as pd
import numpy as np
import os
import glob
import csv
import sqlite3
from sqlalchemy import create_engine
#import time
#import sys

#from timeit import default_timer as timer

# conn = sqlite3.connect("data.db")
# cur = conn.cursor()


def setup(engine, tablename):
    engine.execute("""DROP TABLE IF EXISTS "%s" """ % (tablename))

    engine.execute("""CREATE TABLE "%s" ('Date' NUMERIC PRIMARY KEY, 'Total Transactions' INT, 'Traded Shares' REAL, 'TotalTraded Amount' REAL, 'Maximum Price' REAL, 'Minimum Price' REAL, 'Closing Price' REAL, 'Opening Price' REAL)""" % (tablename))


#engine = create_engine('sqlite://', echo=False)


def checkDir(source):

    os.chdir(source)

    for file in glob.glob("*.csv"):
        TABLENAME = file
        ENGINE = create_engine('sqlite:///data.db', echo=False)
        filename = os.path.basename(file)
        print('setting up db')
        setup(ENGINE, TABLENAME)
        print('Creating table for ' + filename + '...\n')

        try:

            df = pd.read_csv(file, index_col=0, parse_dates=True)
            print(df)
            df.to_sql(TABLENAME, ENGINE, if_exists='replace', index=False)

        except(FileNotFoundError, IOError):
            print('Wrong file or file path.')
            return
            if data.empty:
                print('data empty')
                return
    print('complete')


if __name__ == '__main__':
    checkDir('/media/saroj/589AD0E99AD0C4A2/Documents/stock-prediction-ann/preprocessing working module/data/')
    #DB_TYPE = 'sqlite'
    #DB_DRIVER = 'psycopg2'
    #DB_USER = 'admin'
    #DB_PASS = 'password'
    #DB_HOST = 'localhost'
    #DB_PORT = '5432'
    #DB_NAME = 'data'
    #POOL_SIZE = 50
    #TABLENAME = 'test_upsert'
    #SQLALCHEMY_DATABASE_URI = '%s+%s://%s:%s@%s:%s/%s' % (DB_TYPE, DB_DRIVER, DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME)
    #ENGINE = create_engine(SQLALCHEMY_DATABASE_URI, pool_size=POOL_SIZE, max_overflow=0)


#engine.execute("SELECT * FROM ADB").fetchall()

# cur.close()
# conn.close()
