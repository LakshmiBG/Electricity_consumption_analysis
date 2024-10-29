import pandas as pd
import streamlit as st


#Reading csv files
dfEl = pd.read_csv('Electricity_20-09-2024.csv',delimiter=';', decimal=',')
dfSh = pd.read_csv('sahkon-hinta-010121-240924.csv')

#Change time format of both files to Pandas datetime

#dfEl
dfEl['time'] = pd.to_datetime(dfEl['Time'],format= ' %d.%m.%Y %H:%M')  #1.1.2020 0:00
#dfSh
dfSh['time'] = pd.to_datetime(dfSh['Time'],format= '%d-%m-%Y %H:%M:%S')  #01-01-2021 00:00:00

#Join the two data frames according to time
df = pd.merge(dfEl, dfSh, on = 'time', how = 'inner')

df = df.rename(columns={"Energy (kWh)": "energy_kwh", "Price (cent/kWh)": "price_kwh_cent"})
#df.columns
#print(df.columns)


#Calculate the hourly bill paid (using information about the price and the consumption)
df['bill_euro'] = df['energy_kwh']*df['price_kwh_cent']/100
# print(df.head())

# Calculated grouped values of daily, weekly or monthly consumption, bill, average price
# and average temperature


#freq = 'd', grouping over one day
#freq = 'w', grouping over week
#freq = 'm', grouping over month

df_daily_avg = (df.groupby(pd.Grouper(key = 'time', freq = 'd'))[['energy_kwh','bill_euro','price_kwh_cent','Temperature']]).mean().reset_index()
df_weekly_avg = (df.groupby(pd.Grouper(key = 'time', freq = 'w'))[['energy_kwh','bill_euro','price_kwh_cent','Temperature']].mean()).reset_index()
df_monthly_avg = (df.groupby(pd.Grouper(key = 'time', freq = 'm'))[['energy_kwh','bill_euro','price_kwh_cent','Temperature']].mean()).reset_index()

#df_monthly_avg.columns


df_daily_avg['frequency'] = 'daily'
df_weekly_avg['frequency'] = 'weekly'
df_monthly_avg['frequency'] = 'monthly'

df_daily_avg['datetime'] = df['time'].dt.date
df_weekly_avg['datetime'] = df['time'].dt.date
df_monthly_avg['datetime'] = df['time'].dt.date

# get min date from data
min_date = df_daily_avg['datetime'].min()
max_date = df_daily_avg['datetime'].max()

print(min_date, max_date)

#Start and end date input
start_date = st.date_input(label='Start Date',format="YYYY/MM/DD", value=min_date)
end_date = st.date_input(label='End Date',format="YYYY/MM/DD", value=max_date)

#Grouping interval
option = st.selectbox("Select an option:", ["Daily", "Weekly", "Monthly"])

if option == 'Daily':
    # filter dates
    df_daily_avg.set_index('datetime')
    df_filtered = df_daily_avg[(df_daily_avg['datetime']> start_date) & (df_daily_avg['datetime']<end_date)]
    st.line_chart(data=df_filtered, x='time', y='energy_kwh')
elif option == 'Weekly':
    df_weekly_avg.set_index('datetime')
    df_filtered = df_weekly_avg[(df_weekly_avg['datetime']> start_date) & (df_weekly_avg['datetime']<end_date)]
    st.line_chart(data=df_weekly_avg, x='time', y='energy_kwh')
else:
    df_monthly_avg.set_index('datetime')
    df_filtered = df_monthly_avg[(df_monthly_avg['datetime']> start_date) & (df_monthly_avg['datetime']<end_date)]
    st.line_chart(data=df_monthly_avg, x='time', y='energy_kwh')