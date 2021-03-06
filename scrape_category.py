# coding=utf-8

from datetime import datetime
import requests
from urllib.parse import urljoin, urlsplit
from utils import html_to_soup, url_args_parser, list_of_lists_to_flat_list
from scrape_book import get_book_infos, write_csv, save_book_cover


def main():
    """
    Cette fonction récupère toutes les urls des livres pour une page catégorie donnée
    en récupère les informations et les copie dans un fichier CSV pour cette catégorie
    Elle enregistre ensuite les images de couverture des livres dans un dossier spécifique.
    """
    timestamp_start = datetime.now()
    args = url_args_parser()
    pagination_pages = get_all_pages_category(args.url)
    relative_books_urls_list = get_category_books_urls(pagination_pages)
    relative_books_urls = list_of_lists_to_flat_list(relative_books_urls_list)
    absolute_books_urls = reformat_list_of_relative_urls_to_absolute(relative_books_urls)
    book_infos_list = add_book_infos_to_list(absolute_books_urls)
    write_csv_loop(book_infos_list)
    save_book_cover_loop(book_infos_list)
    execution_time = datetime.now() - timestamp_start
    print(f"Le programme a mis {execution_time} pour s'executer")


def get_all_pages_category(url):
    """
    Cette fonction vérifie s'il existe plusieurs pages pour une catégorie donnée.
    Elle ajoute les URLs de toutes les pages de la catégorie à une liste
    et retourne la liste.
    """
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
    print(f"Nombre de pages trouvées pour la catégorie : {len(pagination_pages)}\n"
          f"---")
    return pagination_pages


def get_books_urls(page):
    """
    Cette fonction récupère les URLs relatives des pages produit sur une page catégorie
    et les ajoute dans une liste.
    """
    soup = html_to_soup(page)
    liens = soup.find_all('a', href=True, title=True)
    print(f"Scan des URLs Produit de la page : {page}")
    relative_books_urls = [{'titre': lien['title'], 'lien': lien['href']} for lien in liens]
    print(f"Nombre de titres trouvés sur la page : {len(relative_books_urls)}\n"
          f"---")
    return relative_books_urls


def get_category_books_urls(pagination_pages):
    """
    Cette fonction récupère les URLs relatives des pages produit de toutes les pages d'une catégorie
    et les ajoute à une liste.
    """
    relative_books_urls_list = [get_books_urls(page) for page in pagination_pages]
    return relative_books_urls_list


def reformat_list_of_relative_urls_to_absolute(relative_urls):
    """
    Cette fonction reformate une liste d'URLs relatives en liste d'URLs absolues depuis la racine du site.
    """
    absolute_urls_list = [urljoin("http://books.toscrape.com/catalogue/", relative_url['lien'].lstrip('../'))
                          for relative_url in relative_urls]
    print(f"{len(absolute_urls_list)} liens ont été reformatés\n"
          f"---")
    return absolute_urls_list


def add_book_infos_to_list(absolute_books_urls):
    """
    Cette fonction récupère les informations de chaque livre pour une liste d'URLs produit sous forme de dictionnaire
    et les ajoute à une liste.
    """
    book_infos_list = [get_book_infos(absolute_book_url) for absolute_book_url in absolute_books_urls]
    return book_infos_list


def write_csv_loop(book_infos_list):
    """
    Cette fonction effectue une boucle sur write_csv pour écrire un dictionnaire de données dans un fichier CSV.
    """
    for book_infos in book_infos_list:
        write_csv(book_infos)
    print(f"{len(book_infos_list)} références copiées\n"
          f"---")


def save_book_cover_loop(book_infos_list):
    """
    Cette fonction effectue une boucle sur save_book_cover pour sauvegarder
    les images de couverture des livres dans un dossier local.
    """
    for book_infos in book_infos_list:
        save_book_cover(book_infos)
    print(f"{len(book_infos_list)} images ont été sauvegardées\n"
          f"---")


if __name__ == "__main__":
    main()
