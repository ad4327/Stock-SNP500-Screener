import pandas as pd
import requests
from requests_html import HTMLSession
from bs4 import BeautifulSoup

#Create HTML header session to go under detected as a bot
session = HTMLSession()

#Use pandas to read the csv file and get the stock symbol
read_stock_names = pd.read_csv('sp500_companies.csv', index_col=False)
snp500_stocks = read_stock_names['Symbol']

#Create list to store stock information
stock_data = []

def getData(symbol):
    #Use BeautifulSoup to read stock information from Yahoo Finance using symbol variable
    url = 'https://finance.yahoo.com/quote/' + symbol + '/key-statistics?p=' + symbol
    r = session.get(url)
    soup = BeautifulSoup(r.text, 'html.parser')

    #Use Beautiful to find stock information from Yahoo finance by finding the div elements
    price = float(soup.find('div', {'class' : 'D(ib) Mend(20px)'}).find_all('fin-streamer')[0].text.replace(',',''))
    year_high = float(soup.find('div', {'class' : 'Pstart(20px) smartphone_Pstart(0px)'}).find_all('td')[7].text.replace(',',''))
    percentage_change_from_52w_high = "{:.2f}".format(((price - year_high) / year_high) * 100)
    day_change = soup.find('div', {'class' : 'D(ib) Mend(20px)'}).find_all('fin-streamer')[2].text.replace(',','')
    
    #Store stock data into Dictionary
    stock = {
        'Symbol' : symbol,
        'Price' : price,
        'Day Change' : day_change,
        '52 Week High' : soup.find('div', {'class' : 'Pstart(20px) smartphone_Pstart(0px)'}).find_all('td')[7].text,
        '52 week change' : percentage_change_from_52w_high
        }

    return stock


#Iterate over snp 500 name database and use the function getData to get stock price information
for item in snp500_stocks:
    stock_data.append(getData(item))
    print('Getting:' + item)

#Append stock information into a Dataframe and store as csv
df = pd.DataFrame.from_dict(stock_data)
df.to_csv('Stock Data.csv', index=False)
print(df)

