from JSONtoPD import *
from Tracker import *
import time
import MySQLdb
from sqlalchemy import create_engine

def DbaseUpdate(Hourly):

    # Calculate initial elapsed time.
    elapsed = tracker()

    if elapsed < 86400:
        while elapsed < 86400:

            dbase_update = False
            print('It has not been 24 hours yet. Going to sleep for 15 minutes.')
            time.sleep(1)

    elif elapsed >= 86400:

        # Establish a connection.

        # Connecting to the SQL database.
        con = MySQLdb.connect(host='3.25.191.104',
                              user='mysql',
                              passwd='TP08',
                              db='tp08_website')

        # Engine used to upload data to the database.
        engine = create_engine('mysql://mysql:TP08@3.25.191.104:3306/tp08_website')

        # Establishing a cursor to allow SQL queries.
        cur = con.cursor()

        print('\nIt has been 24 hours. Updating the database.')

        # SQL Query.
        print('Checking if data exists.')
        query = "SELECT postcode from {}".format('Hourly')
        cur.execute(query)

        # If there are data entries in the database,
        if cur.fetchone():

            print('Pulling data from the database.')

            # Retrieve all data from the database.
            query = "SELECT * from {}".format('Hourly')
            cur.execute(query)

            # Converting the query results to a dataframe.
            df = pd.read_sql_query(query, engine)
            n = df.shape[0]

            # Converting it to a datetime format.
            df['date_recorded'] = df['date_recorded'].apply(lambda x: dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

            # Sorting by the recording date.
            df = df.sort_values(by = 'date_recorded').reset_index(drop=True)

            # Dropping first half of the dataset.
            # We're removing 24 hours out of a 48 hour period per postcode.
            df = df[n // 2: n].reset_index(drop=True)

            # Add the new 24 hours data onto the trimmed dataframe.
            Push = pd.concat([df, Hourly], axis=0, ignore_index=True)
            Push = Push.sort_values(by='date_recorded').reset_index(drop=True)

            print('Data pushed to database.')
            Push.to_sql(con = engine, name = 'Hourly', if_exists = 'append', index = False)

            time.sleep(5)

            # Update the last active date in the tracker text file.
            tracker()

            # Close the connection.
            con.close()
