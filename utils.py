import requests
from bs4 import BeautifulSoup as bs
import argparse

"""
Fichier général de fonctions  réutilisables 
"""


def html_to_soup(book_url):
    """
    Cette fonction  transforme le contenu d'une page web en format BeautifulSoup.
    """
    try:
        response = requests.get(book_url)
    except requests.exceptions.ConnectionError:
        response.status_code = "Connection refused"
    byte_data = response.content
    soup = bs(byte_data, 'lxml')
    return soup


def url_args_parser():
    """
    Cette fonction permet de lancer le script depuis le terminal bash en mentionnant une URL en tant qu'argument.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="scrapes all the products URLs on the page given as argument", type=str)
    args = parser.parse_args()
    return args


def list_of_lists_to_flat_list(list_of_lists):
    """
    Cette fonction transforme une liste de liste d'URLs en liste d'URLs simple.
    """
    flat_list = []
    for liste in list_of_lists:
        for item in liste:
            flat_list.append(item)
    return flat_list
