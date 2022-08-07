from datetime import datetime as dt
from time import sleep
import pandas as pd
import requests

# Load postcodes from csv
postcodes_csv_path = "./database/Postcodes.csv"
postcodes_coords_df = pd.read_csv(postcodes_csv_path)

API_KEY = "3b8bfa253dd09a9f809435251aded64b"

# Exclude all metrics other than `hourly`
exclusion_list = ["current", "minutely", "daily", "alerts"]
exclusions = ",".join(exclusion_list)


def api_call(delay=2) -> pd.DataFrame:

    # Empty list to be added with new rows of data
    final_data_list = []

    # Iterate through postcodes
    for postcode, lat, long in postcodes_coords_df.itertuples(index=False):

        # Call the API
        url = f"https://api.openweathermap.org/data/2.5/onecall?lat={lat}&lon={long}&exclude={exclusions}&appid={API_KEY}"
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


def main() -> None:
    print(api_call(delay=1))


if __name__ == "__main__":
    main()
