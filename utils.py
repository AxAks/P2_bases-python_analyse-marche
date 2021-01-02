import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
import argparse
import os

"""
Fichier général de fonctions  réutilisables 
"""


"""
Transforme le contenu d'une page web en format BeautifulSoup.
"""


def html_to_soup(book_url):
    try:
        response = requests.get(book_url)
    except requests.exceptions.ConnectionError:
        response.status_code = "Connection refused"
    byte_data = response.content
    soup = bs(byte_data, 'lxml')
    return soup


"""
Permet de lancer le script depuis le terminal bash en mentionnant une URL en tant qu'argument. 
"""


def url_args_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="scrapes all the products URLs on the page given as argument", type=str)
    args = parser.parse_args()
    return args


"""
Prend en entrée un dictionnaire et copie les informations dans un fichier CSV.
"""


def write_csv(book_infos):
    category = book_infos['category']
    fichier = f"./references_per_category/{category}-prices_watch.csv"
    os.makedirs(os.path.dirname(fichier), exist_ok=True)
    with open(fichier, "a") as fichier:
        df = pd.DataFrame(book_infos, index=[1])
        df.to_csv(fichier, mode='a', header=False, index=False)


"""
Boucle pour ecrire un dictionnaire de données dans un fichier CSV
Utilise write_csv.
"""


def write_csv_loop(book_infos_list):
    for book_infos in book_infos_list:
        write_csv(book_infos)
    print('---')
    print(f"{len(book_infos_list)} références copiées dans le fichier CSV")


"""
transforme la liste de liste d'URLs en liste d'URLs simple
"""


def list_of_lists_to_flat_list(list_of_lists):
    flat_list = []
    for liste in list_of_lists:
        for item in liste:
            flat_list.append(item)
    return flat_list
