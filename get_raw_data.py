import requests
import mysql.connector
import os
from dotenv import load_dotenv

def get_data_from_vantage_api(symbol, api_function, api_key):
  """This function gets data from the AlphaVantage API (https://www.alphavantage.co/documentation/)

     Args:
      symbol: The symbol of the company to get data related to 
      api_function: The function to use in the api call. ex: 'TIME_SERIES_DAILY_ADJUSTED' for daily data
      api_key: API key obtained from AlphaVantage

    Returns:
      Data returned from api in JSON form  
  """
  urlParams = {'function':api_function, 'symbol':symbol, 'apikey':api_key}
  url = 'https://www.alphavantage.co/query'
  r = requests.get(url, params=urlParams) 
  return r.json()

def insert_data_into_database(symbol, numRecords, data, dbConnection):
  # INSERT IGNORE command still autoincrements primary key values even if no data is entered into the database. 
  insertCommand = 'INSERT IGNORE INTO company_financial_data (symbol, entry_date, open_price, close_price, volume) VALUES (%s, %s, %s, %s, %s)'
  if data == None:
    return
  i = 0
  financial_data = data.get('Time Series (Daily)')
  if financial_data != None:
    for date, values in financial_data.items():
        # check keys for proper data formatting from API
        open_price = values.get('1. open')
        close_price = values.get('4. close')
        volume = values.get('6. volume')
        if None in (open_price, close_price, volume):
          print('Unable to process data from api')
        else:
          dbConnection.execute(insertCommand, (symbol, date, open_price, close_price, volume))

        i += 1
        if i > numRecords:
            return 

def main():
  load_dotenv()

  API_KEY = os.getenv('API_KEY')
  DBNAME = os.getenv('DATABASE')
  USER = os.getenv('MY_SQL_USER')
  PASSWORD = os.getenv('MY_SQL_PASSWORD')
  PORT = os.getenv('PORT')
  
  ibmdata = get_data_from_vantage_api('IBM', 'TIME_SERIES_DAILY_ADJUSTED', API_KEY)
  appledata = get_data_from_vantage_api('AAPL', 'TIME_SERIES_DAILY_ADJUSTED', API_KEY)

  db = mysql.connector.connect(
    host='localhost',
    port=PORT,
    user=USER,
    password=PASSWORD,
    database=DBNAME
  )

  dbcursor = db.cursor()

  insert_data_into_database('IBM', 13, ibmdata, dbcursor)
  insert_data_into_database('AAPL', 13, appledata, dbcursor)

  db.commit()

  print(dbcursor.rowcount, "record inserted.")

  db.close()

main()