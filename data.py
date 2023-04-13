import streamlit as st 
import pandas as pd
import numpy as np
import matplotlib as plt
import seaborn as sns
import plotly.express as px
import missingno as msno
import altair as alt
import folium
import pydeck as pdk
from folium.plugins import HeatMap


name = "Talal Eshki"
github_link = "https://github.com/mud00"
linkedin_link = "https://linkedin.com/in/talal-eshki"

def page1():
    path = "https://github.com/fivethirtyeight/uber-tlc-foil-response/blob/master/uber-trip-data/uber-raw-data-apr14.csv?raw=true"
    df = pd.read_csv(path, delimiter=",")

    def get_dom(dt):
        return dt.day 

    df['dom'] = pd.to_datetime(df['Date/Time']).map(get_dom)

    def get_hour(dt):
        return dt.hour

    df['hour'] = pd.to_datetime(df['Date/Time']).map(get_hour)

    def count_rows(rows):
        return len(rows)

    df['Date/Time'] = pd.to_datetime(df['Date/Time'], format='%m/%d/%Y %H:%M:%S')
    df['dom'] = df['Date/Time'].dt.day

    by_date = df.groupby('dom').apply(count_rows)

    by_hour = df.groupby('hour').apply(count_rows)

    by_date = df.groupby('dom').size()

    st.title('Uber Pickups Data Study')
    st.write('This data is from Uber pickups in April 2014, we will be analysing the dataset and extracting relative information from it.')

    st.write('Pickups per day of month')
    chart_data = pd.DataFrame({'count': by_date})
    chart_data.index.name = 'day'

    st.line_chart(chart_data, use_container_width=True)

    chart_data = pd.DataFrame({'count': by_date})
    chart_data.index.name = 'day'

    st.write('Plotting the same data in a bar chart')
    st.bar_chart(chart_data)

    def get_weekday(dt):
        return dt.weekday()

    df['weekday'] = df['Date/Time'].map(get_weekday)

    by_weekday = df.groupby('weekday').size()

    chart_data = pd.DataFrame({'count': by_weekday})
    chart_data.index.name = 'weekday'

    weekdays = ['Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun', 'Mon']

    chart_data.index = weekdays

    st.write('Frequency by Weekday - Uber - April 2014')
    st.bar_chart(chart_data)

    df2 = df.groupby(['weekday', 'hour']).apply(count_rows).unstack()

    fig = px.imshow(df2, x=np.arange(0, 24, 1), y=weekdays, color_continuous_scale='inferno')
    fig.update_layout(title='Heatmap by Hour and weekdays - Uber - April 2014')
    st.plotly_chart(fig)


def page2():
    def count_rows(rows):
        return len(rows)

    def get_hour(dt):
        return dt.hour


    DATA = "https://raw.githubusercontent.com/uber-web/kepler.gl-data/master/nyctrips/data.csv "
    df = pd.read_csv(DATA, delimiter = ",")
    msno.bar(df)
    df.head()

    df['tpep_pickup_datetime'] = pd.to_datetime(df['tpep_pickup_datetime'])
    df['tpep_dropoff_datetime'] = pd.to_datetime(df['tpep_dropoff_datetime'])
    df['trip_duration'] = (df['tpep_dropoff_datetime'] - df['tpep_pickup_datetime']).dt.total_seconds() / 60
    df['Hour (Time)'] = df['tpep_pickup_datetime'].dt.hour

    by_hour = df.groupby('Hour (Time)').apply(count_rows)
    st.title('Taxi Pickups in NYC on the 15th of April 2015 - Data Study')
    st.write('This data is from Taxi pickups in NYC on the 15th of April 2015, we will be analysing the dataset and extracting relative information from it.')
    st.write()
    st.write('Pickups per hour of the day')
    st.bar_chart(by_hour)

    by_hour = pd.DataFrame({'Frequency': by_hour.values})

    fig = px.imshow(by_hour.transpose(), color_continuous_scale='inferno', title='Heatmap of Taxi Trips by Hour')
    fig.update_layout(xaxis_title='Hour of the Day', yaxis_title='Frequency', xaxis_showgrid=False)
    st.plotly_chart(fig)

    st.write('We can see a peak in taxi orders at 10pm')
    st.write('')
    st.write("**Total number of taxi rides per passenger count**")
    counts_by_passenger = df.groupby("passenger_count").size()
    st.bar_chart(counts_by_passenger)


    df1 = df[df['VendorID'] == 1]

    df1_by_hour = df1["Hour (Time)"].value_counts().sort_index().reindex(range(24), fill_value=0)
    df1_by_hour = pd.DataFrame(df1_by_hour.fillna(0).values.reshape(-1, 1), index=range(24), columns=["Frequency"])

    st.write("**Frequency of Trips by Hour for Vendor 1**")
    st.area_chart(df1_by_hour)


    df2 = df[df['VendorID'] == 2]

    df2_by_hour = df2["Hour (Time)"].value_counts().sort_index()
    df2_by_hour = pd.DataFrame(df2_by_hour.values, index=range(24), columns=["Frequency"])
    st.write("**Frequency of Trips by Hour for Vendor 2**")
    st.area_chart(df2_by_hour)

    data = pd.concat([df1_by_hour, df2_by_hour], axis=1).reset_index()
    data.columns = ['Hour', 'Vendor 1', 'Vendor 2']
    st.write("**Vendor trips compared between eachother**")

    st.area_chart(data)

    df['fare_rounded'] = df['fare_amount'].round()

    df_freq = pd.DataFrame(df['fare_rounded'].value_counts()).reset_index()
    df_freq.columns = ['fare_rounded', 'count']

    chart = alt.Chart(df_freq).mark_bar().encode(
        x='fare_rounded:Q',
        y='count:Q'
    ).properties(
        title='Frequency of Fare Prices'
    )

    chart = chart.properties(width=700, height=400)

    st.altair_chart(chart)


st.sidebar.title("Ubers and Taxis in NYC")

st.sidebar.markdown(f"{name}  \n  \nGitHub  \nhttps://www.github.com/mud00  \n  \nLinkedin  \nhttps://www.linkedin.com/in/talal-eshki")

menu = ["Uber Data", "Taxi Data"]
choice = st.sidebar.selectbox("Select a page", menu)

if choice == "Uber Data":
    page1()
else:
    page2()
