import requests
from bs4 import BeautifulSoup as bs
import argparse

"""
fichier général de fonctions  réutilisables 
"""


"""
Verifie le code statut de la requete si 200 tout est OK
Récupère le contenu brut de la page
Transforme le contenu brut en format BeautifulSoup
"""


def html_to_soup(book_url):
    response = requests.get(book_url)  # verifie le code statut de la requete si 200 tout est OK !
    byte_data = response.content  # le contenu brut de la page
    soup = bs(byte_data, 'lxml')
    return soup


def url_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="scrapes all the products URLs on the page given as argument", type=str)
    args = parser.parse_args()
    return args
