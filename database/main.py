# Scripts.
# Sends a call to the API.
from API import *
# Updates the database.
from Update import *

# This loop will keep running and activate every 24 hours.
# This is caused by the internal restriction in the DBaseUpdate function
while True:
    # Full dataset with 48 entries per postcode, for 722 postcodes.
    Hourly = API_Call()
    print(Hourly.head())

    # Execute update.
    print('\nChecking timer since last update.\nPlease stand by..')
    DbaseUpdate(Hourly)

    # Update the last active date in the tracker text file.
    tracker()