import pandas, requests, datetime, calendar
class dividend_calendar:
    #class attributes 
    calendars = [] 
    url = 'https://api.nasdaq.com/api/calendar/dividends'
    hdrs =  {'Accept': 'application/json, text/plain, */*',
                 'DNT': "1",
                 'Origin': 'https://www.nasdaq.com/',
                 'Sec-Fetch-Mode': 'cors',
                 'User-Agent': 'Mozilla/5.0 (Windows NT 10.0)'}
    def __init__(self, year, month):
          '''
        Parameters
        ----------
        year : year int
        month : month int
        
        Returns
        -------
        Sets instance attributes for year and month of object.
        
          '''
          #instance attributes
          self.year = int(year)
          self.month = int(month)
     
    def date_str(self, day):
        date_obj = datetime.date(self.year, self.month, day)
        date_str = date_obj.strftime(format='%Y-%m-%d')
        return date_str
    def scraper(self, date_str):
         ''' 
          Scrapes JSON object from page using requests module.
           
           Parameters
           - - - - - 
           url : URL string
           hdrs : Header information
           date_str: string in yyyy-mm-dd format
               
           Returns
           - - - -
           dictionary : Returns a JSON dictionary at a given URL.
         
         '''
         params = {'date': date_str}
         page=requests.get(self.url,headers=self.hdrs,params=params)
         dictionary = page.json()
         return dictionary
    
    def dict_to_df(self, dicti):
         ''' 
         Converts the JSON dictionary into a pandas dataframe
         Appends the dataframe to calendars class attribute         
         
         Parameters
         ----------
         dicti : Output from the scraper method as input.
         
         Returns
         -------
         calendar : Dataframe of stocks with that exdividend date
         
         Appends the dataframe to calendars class attribute
         
         If the date is formatted correctly, it will append a 
         dataframe to the calendars list (class attribute).  
         Otherwise, it will return an empty dataframe.         
         '''
         
         rows = dicti.get('data').get('calendar').get('rows')
         calendar = pandas.DataFrame(rows)
         self.calendars.append(calendar)
         return calendar
   
            
    def calendar(self, day):
          '''
          Combines the scrape and dict_to_df methods
          
          Parameters
          ----------
          day : day of the month as string or number.
          
          Returns
          -------
          dictionary : Returns a JSON dictionary with keys 
          dictionary.keys() => data, message, status
          
          Next Levels: 
          dictionary['data'].keys() => calendar, timeframe
          dictionary['data']['calendar'].keys() => headers, rows
          dictionary['data']['calendar']['headers'] => column names
          dictionary['data']['calendar']['rows'] => dictionary list
    
          '''
          day = int(day)
          date_str = self.date_str(day)      
          dictionary = self.scraper(date_str)
          self.dict_to_df(dictionary)          
          return dictionary
           
if __name__ == '__main__':
    year = 2021
    month = 5

#get number of days in month
    days_in_month = calendar.monthrange(year, month)[1]
#create calendar object    
    february = dividend_calendar(year, month)
#define lambda function to iterate over list of days     
    function = lambda days: february.calendar(days)
    
#define list of ints between 1 and the number of days in the month
    iterator = list(range(1, days_in_month+1))
#Scrape calendar for each day of the month                    
    objects = list(map(function, iterator))
#concatenate all the calendars in the class attribute
    concat_df = pandas.concat(february.calendars)
    
#Drop any rows with missing data
    drop_df = concat_df.dropna(how='any')
    
#set the dataframe's row index to the company name
    final_df = drop_df.set_index('companyName')