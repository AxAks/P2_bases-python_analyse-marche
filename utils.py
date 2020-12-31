import requests
from bs4 import BeautifulSoup as bs
import pandas as pd
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
    try:
        response = requests.get(book_url)  # verifie le code statut de la requete si 200 tout est OK !
    except requests.exceptions.ConnectionError:
        response.status_code = "Connection refused"
    byte_data = response.content  # le contenu brut de la page
    soup = bs(byte_data, 'lxml')
    return soup


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
    nom_fichier = f"./CSV_files/surveillance_prix-{category}.csv"
    with open(nom_fichier, "a") as fichier:
        df = pd.DataFrame(book_infos, index=[1])  #  Indexe les lignes de valeurs à partir de 1
        df.to_csv(fichier, mode='a', header=False, index=False)  # Ne reserve pas une colonne pour le numéro d'index
        print(f"Infos du Livre insérées dans le CSV : {book_infos['title']}")
        print('---')


def write_csv_loop(book_infos_list): #  doublon category et site + la write_csv de scrape_book , #  à mettre dans utils.py ?
    for book_infos in book_infos_list:
        write_csv(book_infos)


"""
transforme la liste de liste d'URLs en liste d'URLs simple
"""


def list_of_lists_to_flat_list(list_of_lists):
    flat_list = []
    for list in list_of_lists:
        for item in list:
            flat_list.append(item)
    print(flat_list)
    return flat_list
