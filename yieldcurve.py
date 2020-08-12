from bs4 import BeautifulSoup as bs
import urllib
import requests
import csv
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import style

#url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldYear&year=2020'
url = 'https://www.treasury.gov/resource-center/data-chart-center/interest-rates/Pages/TextView.aspx?data=yieldAll'
resp = requests.get(url)
soup = bs(resp.text, 'lxml')

table = soup.find('table', {'class':'t-chart'})

with open('yielddata.csv', 'w') as csvfile:
    filewriter = csv.writer(csvfile, delimiter=',',quotechar='|', quoting=csv.QUOTE_MINIMAL)
    filewriter.writerow(['date', 'yieldspread'])
    #starting from 1 instead of 0 to ignore table-header
    for row in table.findAll('tr')[1:]:
        date = row.findAll('td')[0].text
        yield2y = row.findAll('td')[6].text
        yield10y = row.findAll('td')[10].text
        try:
            yieldspread = round(float(yield10y) - float(yield2y),2)
        except ValueError:
            print("Value error. Skipping data from ", date)
            continue
        
        filewriter.writerow([date, yieldspread])

print('Yield data has been collected.')

df = pd.read_csv("yielddata.csv",parse_dates = True, index_col = 0)
print(df)
df.dropna(inplace=True) # drops null values, not sure if inplace = True is needed here

style.use('ggplot')
df['yieldspread'].plot()
plt.show()

