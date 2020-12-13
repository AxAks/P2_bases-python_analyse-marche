import pandas as pd
import requests
from lxml import html


url = 'http://books.toscrape.com/catalogue/holidays-on-ice_167/index.html'


# cette fonction ne récupère que les tableaux
def get_table_one_product(url):
    print("Infos supplémentaires : ")
    product_info = pd.read_html(url)
    # print(len(product_info))
    print(product_info)


#  cette fonction ne marche pas pour récupérer les url des images
def test_lxml(url):
    path_title = '/html/body/div/div/div[2]/div[2]/article/div[1]/div[2]/h1'  # récupéré via inspect/copy/Xpath
    path_image_url = '/html/body/div/div/div[2]/div[2]/article/div[1]/div[1]/div/div/div/div/img'
    path_product_descr = '/html/body/div/div/div[2]/div[2]/article/p'
    response = requests.get(url) # verifie le code statut de la requete si 200 tout est OK !
    byte_data = response.content # le contenu brute de la page
    source_code = html.fromstring(byte_data)
    title = source_code.xpath(path_title)
    image_url = source_code.xpath(path_image_url) # pb ! a voir !
    product_descr = source_code.xpath(path_product_descr)
    print(f"1 {response}")
    print(f"2 {byte_data}")
    print(f"3 {source_code}")
    print(f"Titre : {title[0].text_content()}'\n")
    print(f"URL de l'image : {image_url[0].text_content()}\n")
    print(f"Description : {product_descr[0].text_content()}\n")

'''
Comment je recupere l'url de l'image ? à voir ! voir beautifulsoup pour recupérer les liens !
Donc 
- lxml peut récupérer les strings 
- pandas peut récupérer les tableaux 
- beautifulsoup peut récupérer les liens href html ? donc nos urls 

Est ce quil n'y a pas un moyen plus simple ...
'''

test_lxml(url)
get_table_one_product(url)
