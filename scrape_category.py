from utils import html_to_soup, url_args_parser
from scrape_book import get_book_infos
from urllib.parse import urljoin
import requests


# url = "http://books.toscrape.com/catalogue/category/books/default_15/index.html" #  pour tests


def main():
    args = url_args_parser()  #  à passer dans scrape_site ensuite
    pagination_pages = get_all_pages_category(args.url)
    relative_books_urls = get_books_urls(pagination_pages)
    absolute_books_urls = reformat_relative_url_to_absolute(relative_books_urls)
    scrape_category_books(absolute_books_urls)


"""
Recupere toutes les urls des livres pour une page d'une catégorie
et les copie dans un fichier CSV.
"""

"""
on donne l'url index de la categorie et on verifie s'il y a des pages supplémentaires (page-2, page-3, etc...)
"""


def get_all_pages_category(url):
    print("récupération de toutes les pages de la catégorie ...")
    pagination_pages = []
    first_page = urljoin(url, "index.html")
    pagination_pages.append(first_page)
    n = 1
    n_string = str(n)
    response = requests.get(first_page)
    while True:
        print(f"Test : Page {n}")
        if response.status_code == 200:
            print(f"Il existe une page {n}")
            print('---')
        n += 1
        n_string = str(n)
        next_page_absolute = urljoin(url, f"page-{n_string}.html")
        response = requests.get(next_page_absolute)
        if not response.ok:
            break
        pagination_pages.append(next_page_absolute)
    print(f"Nombre de pages trouvées pour la catégorie : {len(pagination_pages)}")
    print('****')
    return pagination_pages

"""
# pour test
pagination_pages = [
 'http://books.toscrape.com/catalogue/category/books/default_15/page-1.html',
 'http://books.toscrape.com/catalogue/category/books/default_15/page-2.html'
 ]
"""


def get_books_urls(pagination_pages):
    relative_books_urls = []
    for pages_url in pagination_pages:
        soup = html_to_soup(pages_url)
        print(f"Scan de la page : {pages_url}")
        liens = soup.find_all('a', href=True, title=True)
        for lien in liens:
            relative_book_url = {'titre': lien['title'], 'lien': lien['href']}
            relative_books_urls.append(relative_book_url['lien'])
            print(f"Titre Récupéré : {relative_book_url['titre']}")
            print(f"Lien -> {relative_book_url['lien']}")
            print('---')
    print(f"Nombre de titres trouvés : {len(relative_books_urls)}")
    print('****')
    return relative_books_urls


"""
Reformate les URLs relatives d'une liste en URL absolues depuis la racine du site
"""


def reformat_relative_url_to_absolute(relative_books_urls):
    absolute_books_urls = []
    for relative_book_url in relative_books_urls:
        relative_book_url = relative_book_url.replace(relative_book_url[:9], '')
        absolute_book_url = urljoin("http://books.toscrape.com/catalogue/", relative_book_url)
        absolute_books_urls.append(absolute_book_url)
    print(f"{len(absolute_books_urls)} liens ont été reformatés")
    print('****')
    return absolute_books_urls


def scrape_category_books(absolute_books_urls):
    for absolute_book_url in absolute_books_urls:
        get_book_infos(absolute_book_url)
    print(f"Infos récupérées : {len(absolute_books_urls)} réferences insérées")
    return True


"""
if __name__ == "main":
    main()
"""
main()
