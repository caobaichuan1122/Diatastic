# Essentials.
import time

import pandas as pd

# API request function.
import requests

from JSONtoPD import JSONtoPandas

postcodes_coords_df = pd.read_csv("./database/Postcodes.csv").head(5)
API_KEY = "3b8bfa253dd09a9f809435251aded64b"

# For each postcode in the dataset, call the API.
def api_call(delay):

    # Empty DF to be concatenated with new rows
    final_df = pd.DataFrame()

    # Iterate through all postcodes
    for row in postcodes_coords_df.itertuples(index=False):
        postcode = row.postcode
        lat = row.lat
        long = row.long

        print(f"Retrieving data from the API\t{postcode=}\t{lat=}\t{long=}")

        # Exclude all metrics other than `hourly`
        exclusion_list = ["current", "minutely", "daily", "alerts"]
        exclusions = ",".join(exclusion_list)

        # Call the API
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&exclude={exclusions}&appid={API_KEY}"
        response = requests.get(url=url)

        # If successful, read the response
        if response.status_code == 200:
            print("Successful!")

            API_df = JSONtoPandas(response.json())

            # Include postcode data
            API_df["postcode"] = postcode
            API_df["lat"] = lat
            API_df["lng"] = long

            # print(API_df)

            # Concatenate new rows to final df
            final_df = pd.concat([final_df, API_df], ignore_index=True)

        # Delay to reduce the load on the API
        time.sleep(delay)

    return final_df


def main() -> None:
    print(api_call(delay=1))


if __name__ == "__main__":
    main()