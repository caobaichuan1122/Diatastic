import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Data
hourly = pd.read_csv('C:/Users/HP-user/OneDrive/Desktop/Test2.csv')

# Temperature.
fig2 = px.line(hourly, x = 'timestamp', y = 'temp')
fig2.add_trace(go.Scatter(x = hourly['timestamp'], y = hourly['temp'],
                          mode = 'lines+markers')
               )
fig2.show()

# Ultraviolet.
fig2 = px.line(hourly, x = 'timestamp', y = 'uvi')
fig2.add_trace(go.Scatter(x = hourly['timestamp'], y = hourly['uvi'],
                          line = dict(color = 'royalblue'),
                          mode = 'lines+markers')
              )
fig2.show()