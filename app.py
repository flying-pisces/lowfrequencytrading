__author__ = "Flying pisces"
__note__ = "Dividend Capturing by Writing Off ITM Cover call"

import streamlit as st
import pandas as pd
from yahoo_fin import stock_info as si
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
date_range = pd.date_range(start_date, end_date-datetime.timedelta(days=1),freq='d')

# data
now = datetime.datetime.now()
openam = now.replace(hour=6, minute=30, second=0, microsecond=0)
closepm = now.replace(hour=13, minute=0, second=0, microsecond=0)

def make_list(results_json):
    new_list = []
    for result in results_json:
        sym = result.get("symbol")
        try:
            price = si.get_live_price(sym)
        except Exception:
            price = 'NaN'
        now = datetime.datetime.now()
        if now > closepm:
            current_time = closepm.strftime("%Y-%m-%d %H:%M:%S")
        elif now < openam:
            current_time = openam.strftime("%Y-%m-%d %H:%M:%S")
        else:
            current_time = now.strftime("%Y-%m-%d %H:%M:%S")
###        print(current_time)
        result['price'] = price
        result['time'] = current_time
        new_list.append(result)
    return new_list

@st.cache
def load_data(date_range):
    url = 'https://api.nasdaq.com/api/calendar/dividends'
    hdrs = {'Accept': 'application/json, text/plain, */*',
            'DNT': "1",
            'Origin': 'https://www.nasdaq.com/',
            'Sec-Fetch-Mode': 'cors',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0)'}
    df_sum = pd.DataFrame()

    for date_obj in date_range:
        date_str = date_obj.strftime(format='%Y-%m-%d')
        params = {'date': date_str}
        page = requests.get(url, headers=hdrs, params=params)
        results = page.json()
        results_list = results['data']['calendar']['rows']
        new_list = make_list(results_list)
        df = pd.DataFrame(new_list, columns=['symbol','price', 'time', 'dividend_Rate', 'dividend_Ex_Date', 'payment_Date'])
        df_sum = df_sum.append(df, ignore_index=True)
    return df_sum

df = load_data(date_range)
sector = df.groupby('symbol')
st.header('Dividend Calendar in Coming Week')
#st.write('Data Dimension: ' + str(df_selected_sector.shape[0]) + ' rows and ' + str(df_selected_sector.shape[1]) + ' columns.')
df_width = 1800
df_height = 3000
st.dataframe(df, width=df_width, height=df_height)
