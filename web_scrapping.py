import pandas as pd
import requests
from lxml import html
from bs4 import BeautifulSoup as bs


url = 'http://books.toscrape.com/catalogue/holidays-on-ice_167/index.html'


#  cette fonction ne récupère que les tableaux infos supplémentaires
def get_table_one_product(url):
    print("Infos supplémentaires : ")
    product_info = pd.read_html(url)
    # print(len(product_info))
    print(product_info)


#  récupération du titre et de l'url de l'image
def get_title_and_image(url):
    path_title = '/html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/h1'  # récupéré via inspect/copy/Xpath
    path_product_descr = '/html/body/div/div/div[2]/div[2]/article/p'
    response = requests.get(url)  # verifie le code statut de la requete si 200 tout est OK !
    byte_data = response.content  # le contenu brute de la page
    source_code = html.fromstring(byte_data)
    title = source_code.xpath(path_title)
    product_descr = source_code.xpath(path_product_descr)
    soup = bs(byte_data, 'lxml')
    image_url = soup.find('img')  # beautiful soup, recupération du contenu de la première balise image

    # des verifs
    print(f"1 {response}")
    print(f"2 {byte_data}")
    print(f"3 {source_code}")
    print("----")

    # les infos qu'on veut recupérer
    print(f"Titre : {title[0].text_content()}")
    print(f"L'URL de l'image ({image_url['alt']}) est : {image_url['src']}")
    print(f"Description : {product_descr[0].text_content()}")


get_title_and_image(url)
get_table_one_product(url)
