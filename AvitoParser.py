import requests
import csv
from bs4 import BeautifulSoup
import pandas
import dict_to_csv


def get_html(url):
    r = requests.get(url)
    return r.text


def get_total_pages(html):
    soup = BeautifulSoup(html, 'lxml')
    pages = soup.find('div', class_='pagination-pages').find_all('a', class_='pagination-page')[-1].get('href')
    total_pages = pages.split('=')[1].split('&')[0]
    return int(total_pages)


def WriteDictToCSV(csv_file, csv_columns, dicto, a):
    try:
        with open(csv_file, 'w') as csvfile:
            writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
            writer.writeheader()
            for data in dicto:
                writer.writerow(data)
    except IOError:
        print("I/O error")
    return print(a)


csv_file = "AvitoOutput.csv"
csv_columns = ['num', 'title', 'price', 'url']
a = 0
url = 'https://www.avito.ru/moskva?q=macbook+pro' #put here your url
html = get_html(url)
total_pages = get_total_pages(html)
num = 0
for page_num in range(1, total_pages):  # // 25
    url = 'https://www.avito.ru/moskva?p=' + str(page_num) + '&q=macbook+pro' #put here your's url request using this sample
    soup = BeautifulSoup(html, 'lxml')
    ads = soup.find('div', class_='catalog-list').find_all('div', class_='item_table')
    for ad in ads:
        try:
            title = ad.find('div', class_='item_table-header').find('h3').text.strip() #get title of every product
        except:
            title = ''
        try:
            url = 'https://www.avito.ru' + ad.find('div', class_='item_table-header').find('h3').find('a').get('href') #get url of every product
        except:
            url = ''
        try:
            price = ad.find('div', class_='item_table-header').find('span', class_='price').text.strip() #get price of every product
            price = ''.join(price.split())
            price = price.replace("₽", "")
        except:
            price = ''

        if int(price) > 20000: #restriction for price in Rubles
            num += 1
            dicto = [{'num': num, 'title': title, 'price': price + 'RUB', 'url': url}]
            #print(dicto) this you can use to check what you program output
            with open(r"AvitoOutput.csv", 'a', newline='') as csvfile:
                fieldnames = ['num', 'title', 'price', 'url']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                writer.writerow({'num': num, 'title': title, 'price': price + 'RUB', 'url': url})
