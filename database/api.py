import time

import pandas as pd
import requests

from JSONtoPD import JSONtoPandas

# Load postcodes from csv
postcodes_csv_path = "./database/Postcodes.csv"
postcodes_coords_df = pd.read_csv(postcodes_csv_path).head(5)

API_KEY = "3b8bfa253dd09a9f809435251aded64b"

# Exclude all metrics other than `hourly`
exclusion_list = ["current", "minutely", "daily", "alerts"]
exclusions = ",".join(exclusion_list)


def api_call(delay=2):

    # Empty DF to be concatenated with new rows
    final_df = pd.DataFrame()

    # Iterate through postcodes
    for postcode, lat, long in postcodes_coords_df.itertuples(index=False):

        # Call the API
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&exclude={exclusions}&appid={API_KEY}"
        response = requests.get(url)

        # If successful, read the response
        if response.status_code == 200:
            print(f"Success!\t{postcode=}\t{lat=}\t{long=}")

            # Convert response into postcode
            API_df = JSONtoPandas(response.json())

            # Include postcode data
            API_df[["postcode", "lat", "lng"]] = postcode, lat, long

            # Concatenate new rows to final df
            final_df = pd.concat([final_df, API_df], ignore_index=True)

        # Delay to reduce the load on the API
        time.sleep(delay)

    return final_df


def main() -> None:
    print(api_call(delay=1))


if __name__ == "__main__":
    main()
