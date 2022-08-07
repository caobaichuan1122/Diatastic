# Essentials.
import pandas as pd
import time

# API request function.
import requests
from JSONtoPD import JSONtoPandas
Postcode = pd.read_csv('C:/Users/HP-user/OneDrive/Desktop/Postcodes.csv')
selection = 'hourly'

# Empty Lists.
postcode_list = []
lat_list = []
lng_list = []
timestamp_list = []
temp_list = []
humidity_list = []
uvi_list = []
description_list = []


# For each postcode in the dataset, call the API.
def API_Call():
    for i in range(1):
        print('Retrieving data from the API.')

        # Iterating through each row in the dataset.
        postcode = Postcode['postcode'].loc[i]
        lat = Postcode['lat'].loc[i]
        lng = Postcode['long'].loc[i]

        # List of metrics to exclude.
        # Based on what the user clocks on, remove the corresponding item from the list and that will be
        # what's returned. I.e. If user clicks on daily, we will exclude everything but daily.
        exclusion_list = ['current', 'minutely', 'daily', 'alerts']

        # Join the remaining options into a string.
        exclusion = ','.join(exclusion_list)

        # API address.
        url = 'https://api.openweathermap.org/data/2.5/onecall?lat={}&lon={}&exclude={}\
               &appid=3b8bfa253dd09a9f809435251aded64b'.format(lat, lng, exclusion)

        # API call.
        resp = requests.get(url=url)

        # Reading the response.
        if resp.status_code == 200:
            print('Successful!\n')
            data = resp.json()
            API_df = JSONtoPandas(data)

            # Storing the data in separate lists before storing them into a dataframe.
            humidity_list.append(API_df['humidity'].tolist())
            uvi_list.append(API_df['uvi'].tolist())
            timestamp_list.append(API_df['timestamp'].tolist())
            temp_list.append(API_df['temp'].tolist())
            description_list.append(API_df['description'].tolist())

            for i in range(len(humidity_list[0])):
                postcode_list.append(postcode)
                lat_list.append(lat)
                lng_list.append(lng)

        # The sleep timer creates a delay to reduce the load on the API.
        time.sleep(4)

    return API_df
