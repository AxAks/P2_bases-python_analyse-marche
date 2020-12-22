import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import csv

url = 'http://books.toscrape.com/catalogue/holidays-on-ice_167/index.html' # pas de code sauvage !!
fichier = open("./surveillance_prix.csv", "w+")  # pareil (hors fonction !)


"""
Récupération des informations du livre dans un dictionnaire
"""


def main():
    get_book_infos(url)


def get_book_infos(url):
    response = requests.get(url)  # verifie le code statut de la requete si 200 tout est OK !
    byte_data = response.content  # le contenu brut de la page
    soup = bs(byte_data, 'lxml')
    title = soup.find_all('h1')[0].get_text()
    product_descr = soup.find_all('p')[3].get_text()
    upc = soup.find_all('td')[0].get_text()
    category = soup.find_all('td')[1].get_text()
    price_no_tax = soup.find_all('td')[2].get_text()
    price_with_tax = soup.find_all('td')[3].get_text()
    availability = soup.find_all('td')[5].get_text()
    reviews_rating = soup.find_all('p', class_='star-rating')[0].get('class')[1]
    image_url = soup.find('img')['src']

    book_infos = {
        'url': url,
        'upc': upc,
        'title': title,
        'price_no_tax': price_no_tax,
        'price_with_tax': price_with_tax,
        'availability': availability,
        'product_descr': product_descr,
        'category': category,
        'reviews_rating': reviews_rating,
        'image_url': image_url
    }
    print(book_infos)
    return book_infos


"""
#  pandas pour gerer tout le csv
ecrire les resultats dans le fichier csv
def write_csv(fichier):
    fichier.file.seek(0, 2)


def read_csv(fichier):
    print(csv.reader(fichier))

"""

if __name__ == "main":
    main()


main()