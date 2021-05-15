import requests
import datetime
import pandas as pd

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

df = pd.DataFrame(results_list, columns=['symbol','dividend_Rate', 'dividend_Ex_Date', 'payment_Date'])
