import pandas as pd
import requests
from lxml import html
from bs4 import BeautifulSoup as bs
import csv


url = 'http://books.toscrape.com/catalogue/holidays-on-ice_167/index.html'
fichier = open("./surveillance_prix.csv", "w+")

resultat = {}
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
    path_universal_product_code = ''
    path_title = '/html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/h1'  # récupéré via inspect/copy/Xpath
    path_price_including_tax = ''
    path_price_excluding_tax = ''
    path_number_available = ''
    path_product_descr = '/html/body/div/div/div[2]/div[2]/article/p'
    path_category = ''
    path_review_rating = ''

    response = requests.get(url)  # verifie le code statut de la requete si 200 tout est OK !
    byte_data = response.content  # le contenu brut de la page
    soup = bs(byte_data, 'lxml')
    title = soup.find_all('h1')[0].get_text()
    product_descr = soup.find_all('p')[3].get_text()
    print(title)
    print(product_descr)
    table_rows = soup.find_all('tr')
    table_data = soup.find_all('td')[0].get_text()
    print('---')
    print(table_rows)
    print('---')
    print(table_data)
    image_url = soup.find('img')['src']
    print(image_url)
    """
    #  source_code = html.fromstring(byte_data)
    #  title = source_code.xpath(path_title)
    # product_descr = source_code.xpath(path_product_descr)
    
     # beautiful soup, recupération du contenu de la première balise image

    title_string = title[0].text_content()  # stockage dans une variable
    image_url_string = image_url['src']  # idem
    product_descr_string = product_descr[0].text_content() #idem
    return url, title_string, image_url_string, product_descr_string  # resultat de la fonction
    """


# à enlever !! on va utiliser que beautiful soup pour parser et recuperer
""" cette fonction ne récupère que les tableaux infos supplémentaires """
def get_table_one_product(url):
    print("Infos supplémentaires : ")
    product_info = pd.read_html(url)
    # print(len(product_info))
    print(product_info)


#  pandas pour gerer tout le csv
""" ecrire les resultats dans le fichier csv """
def write_csv(fichier):
    fichier.file.seek(0, 2)


def read_csv(fichier):
    print(csv.reader(fichier))


def main():
    get_book_infos(url)


if __name__ == "main":
    main()

get_book_infos(url)