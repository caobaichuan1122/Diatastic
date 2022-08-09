from configparser import ConfigParser
from datetime import datetime as dt
from time import sleep

import pandas as pd
import requests
from sqlalchemy import create_engine

TIME_FORMAT = "%d/%m/%Y %H:%M:%S"

# Exclude all metrics other than `hourly`
exclusion_list = ["current", "minutely", "daily", "alerts"]
exclusions = ",".join(exclusion_list)


class WeatherApp:
    def __init__(
        self,
        engine,
        config_path,
        postcodes_csv_path,
        api_key
    ):
        self.config_path = config_path
        self.config = ConfigParser()
        self.config.read(config_path)

        self.postcodes_df = pd.read_csv(postcodes_csv_path)
        self.api_key = api_key

        # Connector to MySql database
        self.engine = engine

    @property
    def last_pulled(self):
        if (conf_last_pulled := self.config["API"]["last_pulled"]) == "":
            return None
        return dt.strptime(conf_last_pulled, TIME_FORMAT)

    @last_pulled.setter
    def last_pulled(self, datetime):
        # Update and write last pulled to config file
        self.config["API"]["last_pulled"] = dt.strftime(datetime, TIME_FORMAT)
        with open(self.config_path, "w") as config_file:
            self.config.write(config_file)

    def api_call(self, delay=1):
        # Empty list to be added with new rows of data
        final_data_list = []

        n_postcodes = len(self.postcodes_df)

        # Iterate through postcodes
        for index, postcode, lat, long in self.postcodes_df.itertuples():

            # Call the API
            url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&exclude={exclusions}&appid={self.api_key}"
            response = requests.get(url)

            if response.status_code == 200:  # Success
                print(
                    f"SUCCESS! \t{postcode=}\t{lat=:>9.4f}\t{long=:>9.4f}\t{index+1: 2d}/{n_postcodes}"
                )

                weather_df = pd.json_normalize(response.json(), record_path=["hourly"])

                # Store relevant data from row into dictionary
                postcode_weather_data = [
                    {
                        "postcode": postcode,
                        "timestamp": dt.fromtimestamp(row.dt),
                        "temp": round(row.temp - 273.15, 2),
                        "uv": row.uvi,
                    }
                    for row in weather_df.itertuples(index=False)
                ]

                # Append to list
                final_data_list += postcode_weather_data

                sleep(delay)

        # Construct dataframe of weather data for all postcodes
        return pd.DataFrame(final_data_list)

    def push_df_to_db(self, df, table="weather"):
        # Replace table with new updated data
        df.to_sql(name=table, con=self.engine, if_exists="replace", index=False)

        # Update `last pulled` in config file
        self.last_pulled = dt.now()
        print(f"COMPLETE! `{table}` updated with {len(df)} rows")

    def perpetual_run_daily(self, table="weather", forced=False):
        print("WARNING: APP RUNNING PERPETUALLY!")
        while True:
            # Pull if never pulled before, if a day has elapsed or if forced
            if (
                self.last_pulled is None
                or (dt.now() - self.last_pulled).days > 0
                or forced
            ):
                if forced:
                    print("[FORCING PULL]")
                    forced = False

                # Call API and push data to database
                df = self.api_call(delay=1)
                self.push_df_to_db(df, table)

            else:
                print(f"Not a day yet\tLast pulled: {self.last_pulled}")

            print("[sleeping for an hour.. zzz...]")
            sleep(60 * 60)  # Sleep an hour


def main() -> None:
    pass


if __name__ == "__main__":
    main()
