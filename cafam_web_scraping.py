
import requests
import csv 
from bs4 import BeautifulSoup
import pandas as pd

def remove_spaces(item):
    item = item.strip().rstrip()
    return item

def export_csv(data):
    df = pd.DataFrame(data) 
    df.to_csv("datos.csv")

def web_scraping():
    data = {
        "Producto": [],
        "Precio": []
    }
    url = 'https://www.drogueriascafam.com.co/176-precios-especiales'
    while True:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        products = soup.find('div',attrs={"class":"product_list"}).find_all('article')
        for product in products:
            name = remove_spaces(product.find('div',attrs={"class":"product-desc-wrap"}).find('h3',attrs={"itemprop":"name"}).get_text())
            price = remove_spaces(product.find('div',attrs={"class":"product-price-and-shipping"}).find('span',attrs={"itemprop":"price"}).get_text().replace('$','').replace('.',''))
            data["Producto"].append(name) 
            data["Precio"].append(price)
        try:
            url = soup.find('div',attrs={"class":"product_list"}).find('a',attrs={"rel":"next"}).get("href")
        except AttributeError:
            break
        print(data)
    return data 

if __name__ == "__main__":
    print("hola entre")
    data = web_scraping()
    export_csv(data)