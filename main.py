import random
from bs4 import BeautifulSoup
import requests
import time
import sqlite3

item_list = []
item_list_modified = []
item_price_list = []

for i in range(1, 6):
    URL = f'https://alta.ge/notebooks-page-{i}.html/'

    r = requests.get(URL)
    soup = BeautifulSoup(r.text, 'html.parser')
    section = soup.find('div', class_="grid-list")
    slots = section.find_all('div', class_='ty-column3')

    for slot in slots:
        nameHolder = slot.find('div', class_='ty-grid-list__item-name')
        name = nameHolder.a.text
        item_list.append(name)
        priceHolder = slot.find('span', class_='ty-price')
        price = priceHolder.span.text
        item_price_list.append(price)
    time.sleep(random.randint(15, 20))

tup_for_DB = []

for i, j in zip(item_list, item_price_list):
    items_pair = (i, j)
    tup_for_DB.append(items_pair)
print(tup_for_DB)

connect = sqlite3.connect('items.sqlite')
cursor = connect.cursor()

# cursor.execute('''create table items (
#                 id integer primary key autoincrement,
#                 title string,
#                 price float)''')


cursor.executemany('''insert into items (title, price) values(?, ?)''', tup_for_DB)


connect.commit()
connect.close()