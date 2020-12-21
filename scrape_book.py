import pandas as pd
import requests
from lxml import html
from bs4 import BeautifulSoup as bs
import csv

url = 'http://books.toscrape.com/catalogue/holidays-on-ice_167/index.html'
fichier = open("./surveillance_prix.csv", "w+")


"""
clés du dictionnaire (10):
product_page_url
universal_product_code
title
price_including_tax
price_excluding_tax
number_available
product_description
category
review_rating
image_url
"""

""" récupération des informations du livre dans un dictionnaire """


def get_book_infos(url):
    resultat = {}
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
    print(f"URL : {url}")
    print(f"UPC : {upc}")
    print(f"Titre : {title}")
    print(f"Prix sans TVA :{price_no_tax}")
    print(f"Prix avec TVA : {price_with_tax}")
    print(f"Disponibilité : {availability}")
    print(f"Résumé : {product_descr}")
    print(f"Categorie : {category}")
    print(f"Note : {reviews_rating}")
    print(f"URL de l'image : {image_url}")
    """
    return url, upc, title, price_no_tax, price_with_tax, availability,\
           product_descr, category, reviews_rating, image_url  # resultat de la fonction
    """


"""
#  pandas pour gerer tout le csv
ecrire les resultats dans le fichier csv
def write_csv(fichier):
    fichier.file.seek(0, 2)


def read_csv(fichier):
    print(csv.reader(fichier))


def main():
    get_book_infos(url)


if __name__ == "main":
    main()
"""
get_book_infos(url)
