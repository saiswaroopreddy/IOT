import pandas as pd
import numpy as np
import os
from dateutil import tz
from dateutil import parser
from _plotly_future_ import v4_subplots
import plotly.offline as pyo
import plotly.graph_objs as go
from plotly.subplots import make_subplots
import readDb

os.chdir("/Users/chanakya/Desktop/EPRI/2019/BoxFiles/AWS/data")

df = pd.read_csv("durational-export-2019-07-25-2019-08-07.csv")


def to_local(timestamp):
    utc = parser.parse(timestamp)

    return utc.astimezone(tz.tzlocal())


power_data = pd.DataFrame()
power_data['Timestamp'] = df['Interval Start Time'].apply(to_local)
power_data['Power'] = df['Average Power (W)']

table = readDb.get_table()
# Get triggers using device ID of button
triggers = readDb.get_triggers(table, 'G030PM045103HXCC')
triggers['Timestamp'] = triggers.iloc[:, 1].apply(
    readDb.to_local).apply(readDb.to_minute_res)

df2 = pd.DataFrame(index=triggers['Timestamp'])
df2 = df2.loc['2019-07-24':'2019-07-25']
df2['Count'] = 1
df2 = df2.resample('1T').sum()

# Create figure with secondary y-axis
fig = make_subplots(specs=[[{"secondary_y": True}]])

# Add traces
fig.add_trace(
    go.Scatter(x=power_data['Timestamp'], y=power_data['Power']),
    secondary_y=False,
)

fig.add_trace(
    go.Scatter(x=df2.index, y=df2['Count']),
    secondary_y=True,
)

# Add figure title
fig.layout.update(
    title_text=df['Description'][0] + " & " + "Number of uses"
)

fig.update_xaxes(title_text="Timestamps (UTC)")
# Set y-axes titles
fig.update_yaxes(title_text="<b>Power (Watts)</b>", secondary_y=False)
fig.update_yaxes(title_text="<b>Number of Uses</b>", secondary_y=True)


pyo.plot(fig)
