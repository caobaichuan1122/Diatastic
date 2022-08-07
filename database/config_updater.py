from configparser import ConfigParser
from datetime import datetime as dt


TIME_FORMAT = "%d/%m/%Y %H:%M:%S"

class Config:
    def __init__(self, path):
        self.path = path
        self.config = ConfigParser()
        self.config.read(path)
    
    @property
    def last_pulled(self):
        if self.config["API"]["last_pulled"] == "":
            return None
        return dt.strptime(self.config["API"]["last_pulled"], TIME_FORMAT)
    
    @last_pulled.setter
    def last_pulled(self, datetime):
        self.config["API"]["last_pulled"] = dt.strftime(datetime, TIME_FORMAT)
        with open(self.path, "w") as config_file:
            self.config.write(config_file)
        
def main() -> None:
    config_file_path = "./database/.ini"
    config = Config(config_file_path)
    
    if config.last_pulled is None or (dt.now() - config.last_pulled).days > 0:
        config.last_pulled = dt.now()
    print(config.last_pulled)


if __name__ == "__main__":
    main()
