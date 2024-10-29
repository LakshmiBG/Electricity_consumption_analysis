import pandas as pd
import streamlit as st


#Reading csv files
url1 = "https://raw.githubusercontent.com/LakshmiBG/Electricity_consumption_analysis/refs/heads/main/Electricity_20-09-2024.csv"
url2 = "https://raw.githubusercontent.com/LakshmiBG/Electricity_consumption_analysis/refs/heads/main/sahkon-hinta-010121-240924.csv"
dfEl = pd.read_csv(url1,delimiter=';', decimal=',')
dfSh = pd.read_csv(url2)

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

st.write(f'Showing range:', start_date, end_date)

if option == 'Daily':
    # filter dates
    df_daily_avg.set_index('datetime')
    df_filtered = df_daily_avg[(df_daily_avg['datetime']> start_date) & (df_daily_avg['datetime']<end_date)]
    st.line_chart(data=df_filtered, x='time', y='energy_kwh', y_label = 'Energy consumption kWh', x_label = 'Time')
    st.line_chart(data=df_filtered, x='time', y='price_kwh_cent', y_label = 'Electricity price [cents]', x_label = 'Time')
    st.line_chart(data=df_filtered, x='time', y='bill_euro', y_label = 'Electricity bill [Euros]', x_label = 'Time')
    st.line_chart(data=df_filtered, x='time', y='Temperature', y_label = 'Temperature', x_label = 'Time')
elif option == 'Weekly':
    df_weekly_avg.set_index('datetime')
    df_filtered = df_weekly_avg[(df_weekly_avg['datetime']> start_date) & (df_weekly_avg['datetime']<end_date)]
    st.line_chart(data=df_filtered, x='time', y='energy_kwh', y_label = 'Energy consumption kWh', x_label = 'Time')
    st.line_chart(data=df_filtered, x='time', y='price_kwh_cent', y_label = 'Electricity price [cents]', x_label = 'Time')
    st.line_chart(data=df_filtered, x='time', y='bill_euro', y_label = 'Electricity bill [Euros]', x_label = 'Time')
    st.line_chart(data=df_filtered, x='time', y='Temperature', y_label = 'Temperature', x_label = 'Time')
else:
    df_monthly_avg.set_index('datetime')
    df_filtered = df_monthly_avg[(df_monthly_avg['datetime']> start_date) & (df_monthly_avg['datetime']<end_date)]
    st.line_chart(data=df_filtered, x='time', y='energy_kwh', y_label = 'Energy consumption kWh', x_label = 'Time')
    st.line_chart(data=df_filtered, x='time', y='price_kwh_cent', y_label = 'Electricity price [cents]', x_label = 'Time')
    st.line_chart(data=df_filtered, x='time', y='bill_euro', y_label = 'Electricity bill [Euros]', x_label = 'Time')
    st.line_chart(data=df_filtered, x='time', y='Temperature', y_label = 'Temperature', x_label = 'Time')


# Display summary statistics for the selected period
total_consumption = df_filtered['energy_kwh'].sum().round(2)
total_bill = df_filtered['bill_euro'].sum().round(2)
average_price = df_filtered['price_kwh_cent'].mean().round(2)
verage_paid_price = (total_bill / total_consumption) * 100 if total_consumption else 0


st.write(f'Total consumption over the period', total_consumption, 'kWh')
st.write(f'Total bill over the period:', total_bill, '€')
st.write(f'Average price:', average_price, 'cents/kWh')
st.write(f'Average paid price:', average_paid_price, 'cents/kWh'
