__author__ = "Chuck Yin, flying pisces"

import streamlit as st
import datetime

# App title
st.markdown('''
# Autonomous Stock Bot 
Description: Buy Stocks and Sell Covered Call 
''')
st.write('---')

# Sidebar
st.sidebar.subheader('Query parameters')
start_date = st.sidebar.date_input("Start date", datetime.date(2019, 1, 1))
end_date = st.sidebar.date_input("End date", datetime.date.today())


####
#st.write('---')
#st.write(tickerData.info)
