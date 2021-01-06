# coding=utf-8

from datetime import datetime
from urllib.parse import urljoin
from utils import html_to_soup, list_of_lists_to_flat_list
from scrape_category import get_all_pages_category, \
    get_category_books_urls, reformat_list_of_relative_urls_to_absolute,\
    add_book_infos_to_list, write_csv_loop, save_book_cover_loop


def main():
    """
    Cette fonction récupèrer les informations de toutes les références
    du site book.toscrape.com : http://books.toscrape.com/.
    Elle copie ces informations dans un fichier CSV d'après la catégorie du livre
    et télécharge l'image de couverture du livre dans un dossier dédiée à sa catégorie
    """
    timestamp_start = datetime.now()
    site_url = 'http://books.toscrape.com/'
    relative_category_urls_list = scrape_site(site_url)
    absolute_category_urls_list = get_absolute_category_urls_list(relative_category_urls_list)
    all_categories_pages_list = get_category_pagination_pages(absolute_category_urls_list)
    all_pages_list = list_of_lists_to_flat_list(all_categories_pages_list)
    relative_books_urls_lists = get_category_books_urls(all_pages_list)
    relative_books_urls_list = list_of_lists_to_flat_list(relative_books_urls_lists)
    absolute_books_urls_list = reformat_list_of_relative_urls_to_absolute(relative_books_urls_list)
    book_infos_list = add_book_infos_to_list(absolute_books_urls_list)
    write_csv_loop(book_infos_list)
    save_book_cover_loop(book_infos_list)
    print('---')
    execution_time = datetime.now() - timestamp_start
    print(f"Le programme a mis {execution_time} pour s'executer")


def scrape_site(site_url):
    """
    La fonction prend en entrée l'URL du site
    et retourne une liste des URLs de toutes les catégories.
    """
    soup = html_to_soup(site_url)
    category_urls = soup.select(".nav>li:nth-child(1)>ul:nth-child(2)>li>a")
    relative_category_urls_list = [category_url['href'] for category_url in category_urls]
    return relative_category_urls_list


def get_absolute_category_urls_list(relative_category_urls_list):
    """
    Cette fonction reformate les URLs relatives des categories en URLs absolues depuis la racine du site.
    """
    site_url = 'http://books.toscrape.com/'
    absolute_category_urls_list = [urljoin(site_url, relative_category_url)
                                   for relative_category_url in relative_category_urls_list]
    return absolute_category_urls_list


def get_category_pagination_pages(absolute_category_urls_list):
    """
    Cette fonction permet de vérifier s'il existe plusieurs pages pour une liste d'URLs de catégorie
    et recupèrer les URLs de toutes ces pages dans une liste de listes.
    """
    all_categories_pages = [get_all_pages_category(absolute_category_url)
                            for absolute_category_url in absolute_category_urls_list]
    return all_categories_pages


if __name__ == "__main__":
    main()
