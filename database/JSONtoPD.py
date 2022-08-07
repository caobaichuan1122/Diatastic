import pandas as pd
import datetime as dt


def JSONtoPandas(df):
    # Reading the file.
    Hourly = pd.json_normalize(df, record_path=['hourly'])

    # Converting numerical ts to datetime, and then to string.
    Hourly['timestamp'] = Hourly['dt'].apply(lambda x: dt.datetime.fromtimestamp(x))

    # Kelvin to Celsius.
    Hourly['temp_C'] = Hourly['temp'].apply(lambda x: x - 273.15)

    # Getting the weather info.
    weather = pd.json_normalize(df, ['hourly', 'weather'])
    Hourly = pd.concat([Hourly, weather], axis=1)

    # Dropping unnecessary columns.
    Hourly.drop(columns=['weather', 'icon', 'dt',
                         'pressure', 'dew_point', 'wind_speed',
                         'wind_deg', 'wind_gust', 'clouds',
                         'pop', 'id', 'feels_like', 'visibility', 'temp',
                         'main'],
                inplace=True)

    Hourly.rename(columns={'temp_C': 'temp'}, inplace=True)
    return Hourly
