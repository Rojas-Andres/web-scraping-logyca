import requests
import csv
from bs4 import BeautifulSoup
import pandas as pd


def remove_spaces(item):
    """
    Remueve espacios inncesarios de los item
    """
    item = item.strip().rstrip()
    return item


def export_csv(data):
    """
    Exportar a csv los datos obtenidos de cafam
    """
    df = pd.DataFrame(data)
    df.to_csv("datos.csv", index=False)


def web_scraping():
    """
    Web scraping ofertas pagina cafam
    """
    data = {"Producto": [], "Precio": []}
    url = "https://www.drogueriascafam.com.co/176-precios-especiales"
    while True:
        r = requests.get(url)
        soup = BeautifulSoup(r.content, "html.parser")
        # Obtenemos todos los productos de la pagina
        products = soup.find("div", attrs={"class": "product_list"}).find_all("article")
        for product in products:
            name = remove_spaces(
                product.find("div", attrs={"class": "product-desc-wrap"})
                .find("h3", attrs={"itemprop": "name"})
                .get_text()
            )
            price = remove_spaces(
                product.find("div", attrs={"class": "product-price-and-shipping"})
                .find("span", attrs={"itemprop": "price"})
                .get_text()
                .replace("$", "")
                .replace(".", "")
            )
            data["Producto"].append(name)
            data["Precio"].append(price)
        # Validamos si hay otra pagina para realizar el scraping
        try:
            url = (
                soup.find("div", attrs={"class": "product_list"})
                .find("a", attrs={"rel": "next"})
                .get("href")
            )
        except AttributeError:
            break
    return data


if __name__ == "__main__":
    data = web_scraping()
    export_csv(data)
