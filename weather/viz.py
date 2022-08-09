from datetime import datetime as dt
from datetime import timedelta

import matplotlib.pyplot as plt
import pandas as pd
# import plotly.express as px
# import plotly.graph_objects as go
from sqlalchemy import create_engine


class Visualization:
    def __init__(self, user, password, host, port, database):
        # Set up connection to MySql database
        self.engine = create_engine(
            f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}"
        )

    def show_viz(self, postcode):
        # Pull data as df from db
        df = pd.read_sql("weather", self.engine)

        # Filter out postcode and from future datetimes
        df = df.loc[
            (df["postcode"] == postcode)
            & (df["timestamp"] > dt.now() - timedelta(hours=1))
            & (df["timestamp"] < dt.now() + timedelta(hours=24))
        ]
        
        def save_viz(col):
            plt.plot(df["timestamp"].apply(lambda x: x.strftime("%H")), df[col], linestyle="--", marker="o", color="b")
            plt.xlabel("timestamp")
            plt.ylabel(col)
            plt.savefig(f"./weather/demo-{col}.png")
            plt.close()
            
        
        save_viz("temp")
        save_viz("uv")

        # TODO:Push these png files to the website


# # Data
# hourly = pd.read_csv('C:/Users/HP-user/OneDrive/Desktop/Test2.csv')

# # Temperature.
# fig2 = px.line(hourly, x = 'timestamp', y = 'temp')
# fig2.add_trace(go.Scatter(x = hourly['timestamp'], y = hourly['temp'],
#                           mode = 'lines+markers')
#                )
# fig2.show()

# # Ultraviolet.
# fig2 = px.line(hourly, x = 'timestamp', y = 'uvi')
# fig2.add_trace(go.Scatter(x = hourly['timestamp'], y = hourly['uvi'],
#                           line = dict(color = 'royalblue'),
#                           mode = 'lines+markers')
#               )
# fig2.show()


def main() -> None:
    host = "3.25.191.104"
    user = "mysql"
    password = "TP08"
    database = "tp08_website"
    port = 3306
    
    postcode = 3996  # Change this
    
    viz = Visualization(
        user=user, host=host, password=password, database=database, port=port
    )
    
    viz.show_viz(postcode)


if __name__ == "__main__":
    main()
