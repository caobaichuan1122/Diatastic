from weather_app import WeatherApp

config_path = "./database/.ini"
postcodes_csv_path = "./database/Postcodes.csv"
API_KEY = (
    "3a178218d81590de8682b7e41b33743e" or "3b8bfa253dd09a9f809435251aded64b"
)  # Luck's or Rash's, short-circuits to first api key 

host = "3.25.191.104"
user = "mysql"
password = "TP08"
database = "tp08_website"
port = 3306


def main() -> None:
    app = WeatherApp(
        config_path=config_path,
        postcodes_csv_path=postcodes_csv_path,
        api_key=API_KEY,
        host=host,
        user=user,
        password=password,
        database=database,
        port=port,
    )
    app.perpetual_run_daily(table="weather", forced=False)


if __name__ == "__main__":
    main()
