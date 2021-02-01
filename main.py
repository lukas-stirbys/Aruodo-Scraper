import pandas as pd
import requests
import numpy as np
from bs4 import BeautifulSoup
from time import sleep
from random import randint

headers = dict()
headers[
    "User-Agent"
] = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36"

classToIgnore = ["top-five-adverts__container"]

links = []
price = []
price_pm2 = []
address = []
overall_area = []
lot_area = []
house_state = []
count = 0

pages = np.arange(1, 67, 1)
for page in pages:
    url = f"https://www.aruodas.lt/namai/puslapis/{str(page)}/?FOrder=AddDate&FPriceMax=100000&FBuildYearMin=1990&detailed_search=1&date_from=1609868763"
    results = requests.get(url, headers=headers)
    soup = BeautifulSoup(results.content, 'html.parser')

    for div in soup.find_all("div", class_="top-five-adverts__wrapper"):
        div.decompose()

    listing = soup.find('table', class_="list-search")
    items = listing.find_all('tr', class_='list-row')
    photo_containers = BeautifulSoup(str(listing.find_all('div', class_="list-photo")), 'html.parser')
    address_containers = listing.find_all('td', class_="list-adress")
    sleep(randint(2, 6))
    count += 1
    print(f"Finished scraping page {count}")

    for link in photo_containers.findAll('a'):
        links.append(link.get('href'))

    for item in items:
        list_item_price = item.find(class_='list-item-price').get_text() if item.find(class_='list-item-price') is not None else ""
        price.append(list_item_price)
        price_pm = item.find(class_='price-pm').get_text() if item.find(class_='price-pm') is not None else ""
        price_pm2.append(price_pm)
        list_adress = item.find('h3').get_text() if item.find('h3') is not None else ""
        address.append(list_adress)
        list_AreaOverall = item.find(class_='list-AreaOverall').get_text() if item.find(class_='list-AreaOverall') is not None else ""
        overall_area.append(list_AreaOverall)
        list_AreaLot = item.find(class_='list-AreaLot').get_text() if item.find(class_='list-AreaLot') is not None else ""
        lot_area.append(list_AreaLot)
        list_HouseStates = item.find(class_='list-HouseStates').get_text() if item.find(class_='list-HouseStates') is not None else ""
        house_state.append(list_HouseStates)

output = pd.DataFrame(
    {
     'Price': price,
     'Price per m2': price_pm2,
     'Address': address,
     'Property area (m2)': overall_area,
     'Lot area (a)': lot_area,
     'Property state': house_state,
     })

# Data cleaning
nan_value = float("NaN")
output.replace("", nan_value, inplace=True)
output.dropna(subset=['Price'], inplace=True)

link_output = pd.DataFrame(
    {
     'Link': links,
    })
# More data cleaning
link_output.replace("#", nan_value, inplace=True)
link_output.dropna(subset=['Link'], inplace=True)

output = output.reset_index()
del output['index']

link_output = link_output.reset_index()
del link_output['index']

links = link_output["Link"]
output = output.join(links)

output.to_csv('Namai.csv', encoding='utf-8-sig')
