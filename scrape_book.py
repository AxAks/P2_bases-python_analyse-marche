import requests
from bs4 import BeautifulSoup as bs
import argparse
import pandas as pd
from urllib.parse import urljoin

# url = 'http://books.toscrape.com/catalogue/holidays-on-ice_167/index.html' # passé en argument à lancer depuis bash

"""
Récupération des informations d'un livre et ecriture dans un fichier CSV
"""


def main(book_url):
    book_infos = get_book_infos(book_url)
    write_csv(book_infos)
    print('je passe ici')
    print(True)
    return True


"""
Prend en entrée l'URL d'une page produit du site et retourne un dictionnaire avec les informations recherchées 
"""


def get_book_infos(book_url):
    response = requests.get(book_url)  # verifie le code statut de la requete si 200 tout est OK !
    byte_data = response.content  # le contenu brut de la page
    soup = bs(byte_data, 'lxml')
    product_page_url = str(book_url)
    universal_product_code = soup.find_all('td')[0].get_text()
    title = soup.find_all('h1')[0].get_text()
    price_including_tax = soup.find_all('td')[3].get_text()
    price_excluding_tax = soup.find_all('td')[2].get_text()
    number_available = soup.find_all('td')[5].get_text()
    product_description = soup.find_all('p')[3].get_text()
    category = soup.find_all('a')[3].get_text()
    review_rating = soup.find_all('p', class_='star-rating')[0].get('class')[1]
    relative_image_url = soup.find('img')['src']
    relative_image_url = relative_image_url.replace(relative_image_url[:5], '')
    absolute_image_url = urljoin('http://books.toscrape.com', relative_image_url)

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
        'image_url': absolute_image_url
    }
    print(book_infos)
    return book_infos


"""
Prend en entrée un dictionnaire et copie les informations dans un fichier CSV
"""


def write_csv(book_infos):
    fichier = open("./surveillance_prix.csv", "w+")
    df = pd.DataFrame(book_infos, index=[1])  #  Indexe les lignes de valeurs à partir de 1
    print(df)
    df.to_csv(fichier, index=False)  # Ne reserve pas une colonne pour le numéro d'index


if __name__ == "main":
    main()

