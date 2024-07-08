
# scraper.py
import requests
from bs4 import BeautifulSoup

url = 'https://vostok.transneft.ru/media-center/'
response = requests.get(url)
soup = BeautifulSoup(response.text, 'lxml')
quotes = soup.find_all('span', class_='text')
authors = soup.find_all('small', class_='author')
tags = soup.find_all('div', class_='tags')

items = soup.find_all('div', class_='col-12 col-xl-4 col-xxl-3')



for i,n in enumerate(items, start=1):
    itemInfo = i.find('a').text
    itemLink= i.find('href').text
    print(itemInfo+ '\n' +itemLink)