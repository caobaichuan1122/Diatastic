from datetime import datetime as dt
from datetime import timedelta

import matplotlib.pyplot as plt
import pandas as pd
from sqlalchemy import create_engine


def construct_viz(user, password, host, port, database, postcode):
    # Set up connection to MySql database
    engine = create_engine(
        f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
    )

    # Pull data as df from db
    df = pd.read_sql("weather", engine)

    # Filter out postcode and from future datetimes
    df = df.loc[
        (df["postcode"] == postcode)
        & (df["timestamp"] > dt.now() - timedelta(hours=1))
        & (df["timestamp"] < dt.now() + timedelta(hours=24))
    ]

    def save_fig(col, file_name):
        plt.plot(
            df["timestamp"].apply(lambda x: x.strftime("%H")),
            df[col],
            linestyle="--",
            marker="o",
            color="b",
        )
        plt.xlabel("timestamp")
        plt.ylabel(col)
        plt.savefig(file_name)
        plt.close()

    save_fig("temp", "./weather/temp_viz.png")
    save_fig("uv", "./weather/uv_viz.png")

    # TODO:Push "./weather/temp_viz.png" to html in website
    # TODO:Push "./weather/uv_viz.png" to html in website


# class Visualization:
#     def __init__(self, user, password, host, port, database):
#         # Set up connection to MySql database
#         self.engine = create_engine(
#             f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
#         )

#     def show_viz(self, postcode):
#         # Pull data as df from db
#         df = pd.read_sql("weather", self.engine)

#         # Filter out postcode and from future datetimes
#         df = df.loc[
#             (df["postcode"] == postcode)
#             & (df["timestamp"] > dt.now() - timedelta(hours=1))
#             & (df["timestamp"] < dt.now() + timedelta(hours=24))
#         ]

#         def save_viz(col):
#             plt.plot(df["timestamp"].apply(lambda x: x.strftime("%H")), df[col], linestyle="--", marker="o", color="b")
#             plt.xlabel("timestamp")
#             plt.ylabel(col)
#             plt.savefig(f"./weather/demo-{col}.png")
#             plt.close()


#         save_viz("temp")
#         save_viz("uv")

#         # TODO:Push these png files to the website


def main() -> None:
    host = "3.25.191.104"
    user = "mysql"
    password = "TP08"
    database = "tp08_website"
    port = 3306

    postcode = 3996  # Change this

    construct_viz(host=host, user=user, password=password, database=database, port=port, postcode=postcode)


if __name__ == "__main__":
    main()
