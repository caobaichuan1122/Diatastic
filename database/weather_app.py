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
        config_path,
        postcodes_csv_path,
        api_key,
        host,
        user,
        password,
        database,
        port,
    ):
        self.config_path = config_path
        self.config = ConfigParser()
        self.config.read(config_path)

        self.postcodes_df = pd.read_csv(postcodes_csv_path)
        self.api_key = api_key
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.port = port

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

            if response.status_code == 200:  # Success
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

        return pd.DataFrame(final_data_list)

    def push_df_to_db(self, df, table="weather"):
        engine = create_engine(
            f"mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}"
        )

        df.to_sql(name=table, con=engine, if_exists="replace", index=False)
        self.last_pulled = dt.now()

        engine.dispose()

    def perpetual_run_daily(self):
        print("WARNING: APP RUNNING PERPETUALLY!")
        while True:
            if self.last_pulled is None or (dt.now() - self.last_pulled).days > 0:
                df = self.api_call(delay=1)
                self.push_df_to_db(df, table="weather")
            else:
                print(
                    f"Not a day yet, sleeping for an hour..\nLast pulled: {self.last_pulled}\n......"
                )
                sleep(60 * 60)  # Sleep an hour


def main() -> None:
    pass


if __name__ == "__main__":
    main()
