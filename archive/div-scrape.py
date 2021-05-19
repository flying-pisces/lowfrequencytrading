import requests
import datetime
import pandas as pd
from yahoo_fin import stock_info as si

calendars = []
url = 'https://api.nasdaq.com/api/calendar/dividends'
hdrs = {'Accept': 'application/json, text/plain, */*',
        'DNT': "1",
        'Origin': 'https://www.nasdaq.com/',
        'Sec-Fetch-Mode': 'cors',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0)'}

### date_str: string in yyyy - mm - dd
### example: url = 'https://api.nasdaq.com/api/calendar/dividends?date=2020-05-17'
year = 2021
month = 5
day = 17

date_obj = datetime.date(year, month, day)
date_str = date_obj.strftime(format='%Y-%m-%d')
params = {'date': date_str}

page = requests.get(url, headers=hdrs, params=params)
results = page.json()
results_list = results['data']['calendar']['rows']
new_list = []
df = pd.DataFrame(results_list, columns=['symbol','dividend_Rate', 'dividend_Ex_Date', 'payment_Date'])


now = datetime.datetime.now()
openam = now.replace(hour=6, minute=30, second=0, microsecond=0)
closepm= now.replace(hour=13, minute=0, second=0, microsecond=0)

for result in results_list:
        sym = result.get("symbol")
        print(sym)
        price = si.get_live_price(sym)
        print(price)
        now=datetime.datetime.now()
        if now > closepm:
                current_time = closepm.strftime("%Y-%m-%d %H:%M:%S")
        elif now < openam:
                current_time = openam.strftime("%Y-%m-%d %H:%M:%S")
        else:
                current_time = now.strftime("%Y-%m-%d %H:%M:%S")
        print(current_time)
        result['price'] = price
        result['time'] = current_time
        new_list.append(result)

df_new = pd.DataFrame(results_list, columns=['symbol', 'price', 'time', 'dividend_Rate', 'dividend_Ex_Date', 'payment_Date'])
breakpoint()