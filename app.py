__author__ = "Flying pisces"
__note__ = "Dividend Capturing by Writing Off ITM Cover call"

import streamlit as st
import pandas as pd
import yfinance as yf
import requests, datetime

# App title
st.markdown('''
# Dividend Capturing Bot 
Description: Buy Stocks and Sell Covered Call to capture dividends For Coming Week
''')
st.write('---')

# Sidebar
st.sidebar.subheader('Query parameters')
today =  datetime.date.today()
next_friday = today + datetime.timedelta((4-today.weekday())%7)
start_date = st.sidebar.date_input("Start date", today)
end_date = st.sidebar.date_input("End date", next_friday)
date_range = pd.date_range(start_date,end_date-datetime.timedelta(days=1),freq='d')

# data

@st.cache
def load_data(date_range):
    calendars = []
    url = 'https://api.nasdaq.com/api/calendar/dividends'
    hdrs = {'Accept': 'application/json, text/plain, */*',
            'DNT': "1",
            'Origin': 'https://www.nasdaq.com/',
            'Sec-Fetch-Mode': 'cors',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0)'}
    df_sum = pd.DataFrame()
    ### date_str: string in yyyy - mm - dd
    ### example: url = 'https://api.nasdaq.com/api/calendar/dividends?date=2020-05-17'
###    year = 2021
###    month = 5
###    day = 17
###    date_obj = datetime.date(year, month, day)
    for date_obj in date_range:
        date_str = date_obj.strftime(format='%Y-%m-%d')
        params = {'date': date_str}

        page = requests.get(url, headers=hdrs, params=params)
        results = page.json()
        results_list = results['data']['calendar']['rows']

        df = pd.DataFrame(results_list, columns=['symbol', 'dividend_Rate', 'dividend_Ex_Date', 'payment_Date'])
        df_sum = df_sum.append(df)
    return df_sum

df = load_data(date_range)
sector = df.groupby('symbol')
st.header('Dividend Calendar in Coming Week')
#st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
st.dataframe(df)

