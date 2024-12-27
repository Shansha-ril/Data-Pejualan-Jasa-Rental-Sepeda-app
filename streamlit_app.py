import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
from babel.numbers import format_currency
sns.set(style='dark')

def create_season_count_df(df):
    seasonal_count = df.groupby(by="season").cnt.sum().reset_index()
    return seasonal_count

def create_hourly_count_df(df):
    hourly_count = df.groupby(by="hr").cnt.sum().reset_index()
    return hourly_count

day_df = pd.read_csv("Submit/dashboard/day_data.csv")
hour_df = pd.read_csv("Submit/dashboard/hour_data.csv")

min_date = day_df["dteday"].min()
max_date = day_df["dteday"].max()

with st.sidebar:

    start_date, end_date = st.date_input(
        label='Rentang Waktu',min_value=min_date,
        max_value=max_date,
        value=[min_date, max_date]
    )

day_df = day_df[(day_df["dteday"] >= str(start_date)) & 
                (day_df["dteday"] <= str(end_date))]

hour_df = hour_df[(hour_df["dteday"] >= str(start_date)) & 
                (hour_df["dteday"] <= str(end_date))]

seasonal_order_df = create_season_count_df(day_df)
hourly_order_df = create_hourly_count_df(hour_df)

st.header('Data Pejualan Jasa Rental Sepeda :sparkles:')

st.subheader('Jasa terjual tiap musim')
 
 
fig, ax = plt.subplots(figsize=(16, 8))
colors = ('#8B4513', '#FFF8DC', '#93C572', '#E67F0D')
labels = ()
for x in day_df.season.unique():
    if x == 1:
        labels = ("springer", *labels)
    elif x == 2:
        labels = ("summer", *labels)
    elif x == 3:
        labels = ("fall", *labels)
    else :
        labels = ("winter", *labels)

ax.pie(
    x=seasonal_order_df.cnt,
    labels= labels,
    autopct='%1.1f%%',
    colors=colors,
)
 
st.pyplot(fig)


st.subheader('Jasa terjual tiap jam')

hours = hour_df.hr.unique()

count = hour_df.groupby(by="hr").cnt.sum()

fig, ax = plt.subplots()
ax.bar(x=hours, height=count, width=0.5)
ax.set_xlabel('Jam')
ax.set_ylabel('Jumlah Total')
ax.set_title('Jumlah Total per Jam')

ax.set_xticks(hours)
ax.set_xticklabels(hours)

st.pyplot(fig)
