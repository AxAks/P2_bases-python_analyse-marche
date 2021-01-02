from utils import html_to_soup, url_args_parser, list_of_lists_to_flat_list, write_csv_loop
from scrape_book import get_book_infos
from urllib.parse import urljoin, urlsplit
import requests


"""
Recupere toutes les urls des livres pour une page Catégorie donnée
en récupère les informations
et les copie dans un fichier CSV pour cette catégorie 
tout en enregistrant les images de couvertures des livres dans un dossier spécifique.
"""


def main():
    args = url_args_parser()
    pagination_pages = get_all_pages_category(args.url)
    relative_books_urls_list = get_category_books_urls(pagination_pages)
    relative_books_urls = list_of_lists_to_flat_list(relative_books_urls_list)
    absolute_books_urls = reformat_list_of_relative_urls_to_absolute(relative_books_urls)
    book_infos_list = add_book_infos_to_list(absolute_books_urls)
    write_csv_loop(book_infos_list)


"""
Verifie s'il existe plusieurs pages pour une catégorie donnée.
Ajoute les URLs de toutes les pages de la catégorie à une liste
Retourne la liste
"""


def get_all_pages_category(url):
    parsed_url = urlsplit(url)
    print(f"Récupération de toutes les pages liées à {parsed_url[2]} :")
    pagination_pages = []
    first_page = urljoin(url, "index.html")
    pagination_pages.append(first_page)
    n = 1
    response = requests.get(first_page)
    while True:
        print(f"Test : Page {n}")
        if response.status_code == 200:
            print(f"- Page {n} trouvée")
        n += 1
        n_string = str(n)
        next_page_absolute = urljoin(url, f"page-{n_string}.html")
        response = requests.get(next_page_absolute)
        if not response.ok:
            break
        pagination_pages.append(next_page_absolute)
    print(f"Nombre de pages trouvées pour la catégorie : {len(pagination_pages)}")
    print('---')
    return pagination_pages


"""
Récupère les URLs relatives des pages produit sur une page catégorie
et les ajoute dans une liste.
"""


def get_books_urls(page):
    relative_books_urls = []
    soup = html_to_soup(page)
    print(f"Scan des URLs Produit de la page : {page}")
    liens = soup.find_all('a', href=True, title=True)
    for lien in liens:
        relative_book_url = {'titre': lien['title'], 'lien': lien['href']}
        relative_books_urls.append(relative_book_url['lien'])
        print(f"- URL récupérée pour le titre : {relative_book_url['titre']}")
    print("---")
    print(f"Nombre de titres trouvés sur la page : {len(relative_books_urls)}")
    print("---")
    return relative_books_urls


"""
Récupère les URLs relatives des pages produit de toutes les pages d'une catégorie
et les ajoute à une liste.
"""


def get_category_books_urls(pagination_pages):
    relative_books_urls_list = []
    for page in pagination_pages:
        relative_books_urls = get_books_urls(page)
        relative_books_urls_list.append(relative_books_urls)
    return relative_books_urls_list


"""
Reformate une liste d'URLs relatives en liste d'URLs absolues depuis la racine du site
"""


def reformat_list_of_relative_urls_to_absolute(relative_urls):
    absolute_urls_list = []
    for relative_url in relative_urls:
        relative_url = relative_url.replace(relative_url[:9], '')
        absolute_url = urljoin("http://books.toscrape.com/catalogue/", relative_url)
        absolute_urls_list.append(absolute_url)
    print(f"{len(absolute_urls_list)} liens ont été reformatés")
    print("---")
    return absolute_urls_list


"""
Pour une liste d'URLs produit, récupère les informations de chaque livre sous forme de dictionnaire
et les ajoute à une liste
"""


def add_book_infos_to_list(absolute_books_urls):
    book_infos_list = []
    for absolute_book_url in absolute_books_urls:
        book_infos = get_book_infos(absolute_book_url)
        book_infos_list.append(book_infos)
    return book_infos_list


if __name__ == "__main__":
    main()
