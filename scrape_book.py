import requests
from bs4 import BeautifulSoup as bs
import argparse
import pandas as pd
import csv

# url = 'http://books.toscrape.com/catalogue/holidays-on-ice_167/index.html' # passé en argument à lancer depuis bash
fichier = open("./surveillance_prix.csv", "w+")  # pas de code sauvage (hors fonction !)


"""
Récupération des informations du livre dans un dictionnaire
"""


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="scapes the product infos on the page given as argument", type=str)
    args = parser.parse_args()
    print(args.url)
    return get_book_infos(args.url)


def get_book_infos(*args):
    response = requests.get(*args)  # verifie le code statut de la requete si 200 tout est OK !
    byte_data = response.content  # le contenu brut de la page
    soup = bs(byte_data, 'lxml')
    product_page_url = str(*args)
    universal_product_code = soup.find_all('td')[0].get_text()
    title = soup.find_all('h1')[0].get_text()
    price_including_tax = soup.find_all('td')[3].get_text()
    price_excluding_tax = soup.find_all('td')[2].get_text()
    number_available = soup.find_all('td')[5].get_text()
    product_description = soup.find_all('p')[3].get_text()
    category = soup.find_all('a')[3].get_text()
    review_rating = soup.find_all('p', class_='star-rating')[0].get('class')[1]
    image_url = soup.find('img')['src']

    book_infos = {
        'product_page_url': product_page_url,
        'universal_product_code': universal_product_code,
        'title': title,
        'price_including_tax': price_including_tax,
        'price_excluding_tax': price_excluding_tax,
        'number_available': number_available,
        'product_description': product_description,
        'category': category,
        'review_rating': review_rating,
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


if __name__ == "main":
    main()
"""

main()
