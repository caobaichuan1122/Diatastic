from datetime import datetime as dt
from time import sleep

from api import api_call
from config_manager import Config
from update import update_mysql


def main() -> None:
    host = "3.25.191.104"
    user = "mysql"
    password = "TP08"
    database = "tp08_website"
    port = 3306

    config_file_path = "./database/.ini"

    while True:
        config = Config(config_file_path)

        if config.last_pulled is None or (dt.now() - config.last_pulled).days > 0:
            data = api_call(delay=1)
            update_mysql(host, user, password, database, port, data)
            config.last_pulled = dt.now()
        else:
            sleep(60 * 60)


if __name__ == "__main__":
    main()
