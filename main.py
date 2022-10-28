import requests
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager

from bs4 import BeautifulSoup
import pandas as pd
import time

driver = webdriver.Chrome(ChromeDriverManager().install())

def getProp(num):
    URL = "" + str(num)
    driver.get(URL)
    time.sleep(3)
    content = requests.get(URL)
    soup = BeautifulSoup(content.text, 'html.parser')
    print('IN FUNCTION')
    text = soup.find_all("span", {"class": "advert-link-text"})
    loc = soup.find_all("span", {"class": "advert-item-col-1-only advert-location adverts-icon-location"})
    price = soup.find_all("div", {"class": "advert-price"})
    print(text)
    print(price)

    textList = []
    locList = []
    priceList = []

    for property in text:
        textList.append(property.get_text())

    for location in loc:
        locList.append(location.get_text())

    for price in price:
        priceList.append(price.get_text())

    print(textList)
    print(locList)
    print(priceList)
    print('EXIT FUNCTION')
    return textList, locList, priceList

propertyName = []
locationName = []
propertyPrice = []

print('Gathering data...')
for pageNum in range(2, 1070, 1):
    text, location, price = getProp(pageNum)
    propertyName.extend(text)
    locationName.extend(location)
    propertyPrice.extend(price)
    print('========================')
    print('Page Number ' + str(pageNum))
    print('Total Titles: ' + str(len(propertyName)))
    print('Total Location: ' + str(len(locationName)))
    print('Total Prices: ' + str(len(propertyPrice)))
    print('========================')

df = pd.DataFrame({'Property': propertyName, 'Location': locationName, 'Price': propertyPrice})
print(df)
df.to_csv('foreclosed.csv')