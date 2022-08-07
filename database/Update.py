from Database import *
from JSONtoPD import *
from Tracker import *
import time


def DbaseUpdate(Hourly):
    hours = 0
    # Establish the initial tracker timer.
    elapsed = tracker()
    print(elapsed)

    while elapsed > 86400:

        if elapsed >= 86400:

            print('\nIt has been 24 hours. Updating the database.')

            # SQL Query.
            query = "SELECT postcode from {}".format('Hourly')
            cur.execute(query)

            # If there are data entries in the database,
            if cur.fetchone():

                # Retrieve all data from the database.
                query = "SELECT * from {}".format('Hourly')
                cur.execute(query)

                # Converting the query results to a dataframe.
                df = pd.read_sql_query(query, engine)
                n = df.shape[0]

                # Converting it to a datetime format.
                df['date_recorded'] = df['date_recorded'].apply(lambda x: dt.datetime.strptime(x, "%Y-%m-%d %H:%M:%S"))

                # Sorting by the recording date.
                df = df.sort_values(by='date_recorded').reset_index(drop=True)

                # Dropping first half of the dataset.
                # We're removing 24 hours out of a 48 hour period per postcode.
                df = df[n // 2: n].reset_index(drop=True)

                # Add the new 24 hours data onto the trimmed dataframe.
                Push = pd.concat([df, Hourly], axis=0, ignore_index=True)
                Push = Push.sort_values(by='date_recorded').reset_index(drop=True)

            print('Data pushed to database.')
            Push.to_sql(con = engine, name = 'Hourly', if_exists = 'replace', index = False)

            time.sleep(5)
            # Update the last active date in the tracker text file.
            hours = elapsed/3600

        else:
            print('\nElapsed time since last update: %2f.\nGoing to sleep for 30s.\n' % hours)
            time.sleep(30)

    elapsed = tracker()
    return elapsed
