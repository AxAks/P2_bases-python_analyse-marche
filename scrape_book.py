# coding=utf-8

import requests
import os
from urllib.parse import urljoin
import pandas as pd
from utils import html_to_soup, url_args_parser


def main():
    """
    Cette fonction  prend en paramètre une URL de page produit.
    Elle récupère les informations de cette référence,
    télécharge l'image de couverture
    et affiche les informations à l'ecran.
    """
    args = url_args_parser()
    book_infos = get_book_infos(args.url)
    print(f" Voici les informations trouvées : \n\n"
          f"- product_page_url : {book_infos['product_page_url']}\n"
          f"- universal_product_code : {book_infos['universal_product_code']}\n"
          f"- title : {book_infos['title']}\n"
          f"- price_including_tax : {book_infos['price_including_tax']}\n"
          f"- price_excluding_tax : {book_infos['price_excluding_tax']}\n"
          f"- number_available : {book_infos['number_available']}\n"
          f"- product_description : {book_infos['product_description']}\n"
          f"- category : {book_infos['category']}\n"
          f"- review_rating : {book_infos['review_rating']}\n"
          f"- image_url : {book_infos['image_url']}\n")
    save_book_cover(book_infos)


def get_book_infos(book_url):
    """
    Cette fonction prend en entrée l'URL d'une page produit du site
    et retourne un dictionnaire avec les informations recherchées.
    """
    soup = html_to_soup(book_url)
    product_page_url = str(book_url)
    all_tds = soup.find_all('td')
    universal_product_code = all_tds[0].get_text()
    title = soup.find_all('h1')[0].get_text()
    price_including_tax = all_tds[3].get_text()
    price_excluding_tax = all_tds[2].get_text()
    number_available = all_tds[5].get_text()
    product_description = soup.find_all('p')[3].get_text()
    category = soup.find_all('a')[3].get_text()
    review_rating = soup.find_all('p', class_='star-rating')[0].get('class')[1]
    relative_image_url = soup.find('img')['src'].lstrip('../')
    absolute_image_url = urljoin('http://books.toscrape.com',
                                 relative_image_url)
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
    print(f'Les infos du livre "{title}\" ont été récupérées')
    return book_infos


def write_csv(book_infos):
    """
    Cette fonction prend en entrée un dictionnaire
    et copie les informations dans un fichier CSV.
    """
    category = book_infos['category']
    fichier = f"./references_per_category/{category}-prices_watch.csv"
    os.makedirs(os.path.dirname(fichier), exist_ok=True)
    if not os.path.exists(fichier):
        columns = ['product_page_url', 'universal_product_code',
                   'title', 'price_including_tax', 'price_excluding_tax',
                   'number_available', 'product_description', 'category',
                   'review_rating', 'image_url']
        with open(fichier, mode='w', encoding='utf-8') as f:
            f.write(';'.join(columns) + '\n')
    with open(fichier, "a") as fichier:
        df = pd.DataFrame(book_infos, index=[1])
        df.to_csv(fichier, encoding='utf-8', sep=';',
                  mode="a", header=False, index=False)


def save_book_cover(book_infos):
    """
    Cette fonction prend en entrée un dictionnaire
    et télécharge l'image de couverture du livre à partir de l'URL extraite.
    """
    category = book_infos['category']
    title = book_infos['title'].replace('/', ' - ')
    fichier = f"./Book_covers/{category}/{title}-cover.jpg"
    book_cover = requests.get(book_infos['image_url']).content
    os.makedirs(os.path.dirname(fichier), exist_ok=True)
    with open(fichier, 'wb') as handler:
        handler.write(book_cover)
        print(f'L\'image de couverture de "{title}" a été copiée'
              f'dans "./Book_covers/{category}/"')


if __name__ == "__main__":
    main()
