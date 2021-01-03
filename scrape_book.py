import requests
import os
from utils import html_to_soup, url_args_parser
from urllib.parse import urljoin


def main():
    """
    Prend en paramètre une URL de page produit
    Récupère les informations de cette référence
    Télécharge l'image de couverture
    et affiche les informations à l'ecran
    """
    args = url_args_parser()
    print(get_book_infos(args.url))


def get_book_infos(book_url):
    """
    Prend en entrée l'URL d'une page produit du site et retourne un dictionnaire avec les informations recherchées.
    """
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
    fichier = f"Book_covers/{category}/{title.replace('/', ' - ')}-cover.jpg"
    book_cover = requests.get(absolute_image_url).content
    os.makedirs(os.path.dirname(fichier), exist_ok=True)
    with open(fichier, 'wb') as handler:
        handler.write(book_cover)
        print(f"Infos du livre \"{title}\" récupérées ->"
              f" L'image de couverture a été copiée dans ./Book_covers/{category}/")
    return book_infos


if __name__ == "__main__":
    main()
