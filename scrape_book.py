from utils import html_to_soup, url_args_parser
from urllib.parse import urljoin
import requests
import os

"""
Récupération des informations d'un livre et ecriture dans un fichier CSV
(Ne se lance pas seul, il doit etre appelé par une autre fonction avec une URL de page produit en argument)
"""


book_url = 'http://books.toscrape.com/catalogue/holidays-on-ice_167/index.html'  #  juste pour les tests


def main():
    args = url_args_parser()
    print(get_book_infos(args.url))
    save_book_cover(absolute_image_url)

"""
Prend en entrée l'URL d'une page produit du site et retourne un dictionnaire avec les informations recherchées 
"""


def get_book_infos(book_url):
    soup = html_to_soup(book_url)
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
    fichier = f'Book_covers/{category}/{title}-cover.jpg'
    book_cover = requests.get(absolute_image_url).content
    os.makedirs(os.path.dirname(fichier), exist_ok=True)
    with open(fichier, 'wb') as handler:
        handler.write(book_cover)
    print(f"Infos du Livre récupérées : {title}")
    print(f"image du Livre copiée dans Book_covers/{category}/")
    return book_infos


if __name__ == "main":
    main()

main()
