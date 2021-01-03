from utils import html_to_soup, write_csv_loop, list_of_lists_to_flat_list
from urllib.parse import urljoin
from scrape_category import get_all_pages_category, \
    get_books_urls
from scrape_book import get_book_infos
from datetime import datetime


"""
absolute_category_urls_list = ['http://books.toscrape.com/catalogue/category/books/mystery_3/index.html',
                               'http://books.toscrape.com/catalogue/category/books/romance_8/index.html'
                               ] # valeurs tests
"""


def main():
    """
    Récupèrer les informations de toutes les références du site book.toscrape.com : http://books.toscrape.com/,
    copie ces informations dans un fichier CSV d'après la catégorie du livre
    et télécharge l'image de couverture du livre dans un dossier dédiée à sa catégorie
    """
    timestamp_start = datetime.now()
    site_url = 'http://books.toscrape.com/'
    relative_category_urls_list = scrape_site(site_url)
    absolute_category_urls_list = get_absolute_category_urls_list(relative_category_urls_list)
    all_categories_pages_list = get_category_pagination_pages(absolute_category_urls_list)
    all_pages_list = list_of_lists_to_flat_list(all_categories_pages_list)
    relative_books_urls_lists = get_relative_books_urls_list(all_pages_list)
    relative_books_urls_list = list_of_lists_to_flat_list(relative_books_urls_lists)
    absolute_books_urls_list = relative_to_absolute_books_url_list(relative_books_urls_list)
    book_infos_list = get_all_books_infos_list(absolute_books_urls_list)
    write_csv_loop(book_infos_list)
    print('---')
    execution_time = datetime.now() - timestamp_start
    print(f"Le programme a mis {execution_time} pour s'executer")


def scrape_site(site_url):
    """
    La fonction prend en entrée l'URL du site
    et retourne une liste des URLs de toutes les catégories.
    """
    relative_category_urls_list = []
    soup = html_to_soup(site_url)
    category_urls = soup.select(".nav>li:nth-child(1)>ul:nth-child(2)>li>a")
    for category_url in category_urls:
        category_url = category_url['href']
        relative_category_urls_list.append(category_url)
    return relative_category_urls_list


def get_absolute_category_urls_list(relative_category_urls_list):
    """
    Reformate les URLs Categories relatives en URLs Absolues.
    """
    site_url = 'http://books.toscrape.com/'  # test
    absolute_category_urls_list = []
    for relative_category_url in relative_category_urls_list:
        absolute_category_url = urljoin(site_url, relative_category_url)
        absolute_category_urls_list.append(absolute_category_url)
    print(absolute_category_urls_list)
    print(len(absolute_category_urls_list))
    return absolute_category_urls_list


def get_category_pagination_pages(absolute_category_urls_list):
    """
    Permet de vérifier s'il existe plusieurs pages pour une liste d'URLs de categorie
    et recupèrer les URLs de toutes ces pages.
    """
    all_categories_pages = []
    for absolute_category_url in absolute_category_urls_list:
        category_pagination_pages = get_all_pages_category(absolute_category_url)
        all_categories_pages.append(category_pagination_pages)
    return all_categories_pages


def get_relative_books_urls_list(all_pages_list):
    """
    Permet de récupérer une liste de toutes les URLs relatives des des pages produit à partir
    d'une liste des différentes pages de categorie.
    """
    relative_books_urls_list = []
    for page in all_pages_list:
        relative_books_urls = get_books_urls(page)
        relative_books_urls_list.append(relative_books_urls)
    return relative_books_urls_list


def relative_to_absolute_books_url_list(relative_books_urls_list):
    """
    Reformate la liste des URLs relatives récupérées en liste d'URLs absolues
    Boucle sur reformat_relative_url_to_absolute pour créer une nouvelle liste.
    """
    absolute_book_url_list = []
    for relative_book_url in relative_books_urls_list:
        absolute_book_url = reformat_relative_url_to_absolute(relative_book_url)
        absolute_book_url_list.append(absolute_book_url)
    return absolute_book_url_list


def reformat_relative_url_to_absolute(relative_url):
    """
    Reformate une URL relative en URL absolue depuis la racine du site
    """
    relative_url = relative_url.lstrip('../')
    absolute_url = urljoin("http://books.toscrape.com/catalogue/", relative_url)
    return absolute_url


def get_all_books_infos_list(absolute_books_urls_list):
    """
    Permet de récupérer les informations des livres à partir de la liste de leurs URLs
    """
    book_infos_list = []
    for absolute_book_url in absolute_books_urls_list:
        book_infos = get_book_infos(absolute_book_url)
        book_infos_list.append(book_infos)
    return book_infos_list


if __name__ == "__main__":
    main()
