from configparser import ConfigParser
from datetime import datetime as dt
from time import sleep

import pandas as pd
import requests
from sqlalchemy import create_engine

from main import (
    API_KEY,
    config_path,
    database,
    host,
    password,
    port,
    postcodes_csv_path,
    user,
)

TIME_FORMAT = "%d/%m/%Y %H:%M:%S"

# Exclude all metrics other than `hourly`
exclusion_list = ["current", "minutely", "daily", "alerts"]
exclusions = ",".join(exclusion_list)


class WeatherApp:
    def __init__(
        self,
        config_path=config_path,
        postcodes_csv_path=postcodes_csv_path,
        api_key=API_KEY,
    ):
        self.config_path = config_path
        self.config = ConfigParser()
        self.config.read(config_path)
        self.postcodes_df = pd.read_csv(postcodes_csv_path)
        self.api_key = api_key

    @property
    def last_pulled(self):
        if self.config["API"]["last_pulled"] == "":
            return None
        return dt.strptime(self.config["API"]["last_pulled"], TIME_FORMAT)

    @last_pulled.setter
    def last_pulled(self, datetime):
        self.config["API"]["last_pulled"] = dt.strftime(datetime, TIME_FORMAT)
        with open(self.config_path, "w") as config_file:
            self.config.write(config_file)

    def api_call(self, delay=1):
        # Empty list to be added with new rows of data
        final_data_list = []

        # Iterate through postcodes
        for postcode, lat, long in self.postcodes_df.itertuples(index=False):

            # Call the API
            url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&exclude={exclusions}&appid={self.api_key}"
            response = requests.get(url)

            # If successful, read the response
            if response.status_code == 200:
                print(f"SUCCESS! \t{postcode=}\t{lat=:>9.4f}\t{long=:>9.4f}")

                weather_df = pd.json_normalize(response.json(), record_path=["hourly"])

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

        final_df = pd.DataFrame(final_data_list)
        return final_df

    def push_df_to_db(
        self,
        df,
        table="weather",
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
    ):
        engine = create_engine(
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        )

        df.to_sql(name=table, con=engine, if_exists="replace", index=False)

        engine.dispose()

    def perpetual_run_daily(self):
        print("WARNING: APP RUNNING PERPETUALLY!")
        while True:
            if self.last_pulled is None or (dt.now() - self.last_pulled).days > 0:
                data = self.api_call(delay=1)
                self.push_df_to_db(data)
                self.last_pulled = dt.now()
            else:
                print(
                    f"Not a day yet since last pulled\nSleeping for another hour\nLast pulled: {self.last_pulled}\n..."
                )
                sleep(60 * 60)  # Sleep an hour


def main() -> None:
    weather_app = WeatherApp()
    weather_app.perpetual_run_daily()


if __name__ == "__main__":
    main()
