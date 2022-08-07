from sqlalchemy import create_engine

def update_mysql(host, user, password, database, port, data, table="weather"):
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )

    data.to_sql(name=table, con=engine, if_exists="replace", index=False)

    engine.dispose()


def main() -> None:
    from datetime import datetime as dt
    from time import sleep
    from api import api_call
    from config_manager import Config

    host = "3.25.191.104"
    user = "mysql"
    password = "TP08"
    database = "tp08_website"
    port = 3306


    config_file_path = "./database/.ini"
    config = Config(config_file_path)

    if config.last_pulled is None or (dt.now() - config.last_pulled).days > 0 or 1:
        data = api_call(delay=1)
        update_mysql(host, user, password, database, port, data)
        config.last_pulled = dt.now()
    else:
        sleep(60 * 60)  # Sleep an hour


if __name__ == "__main__":
    main()