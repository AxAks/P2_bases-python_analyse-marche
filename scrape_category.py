from utils import html_to_soup, url_args_parser
import scrape_book
from urllib.parse import urljoin
import requests


#   url = "http://books.toscrape.com/catalogue/category/books/default_15/index.html" #  pour tests
def main():
    args = url_args_parser()
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
    pagination_pages = []
    n = 1
    n_string = str(n)
    next_page_absolute = urljoin(url, f"page-{n_string}.html")
    response = requests.get(next_page_absolute)
    while response.status_code == 200:   # pb si site temporairement inaccesible pendant la boucle
        pagination_pages.append(next_page_absolute)
        n += 1
        n_string = str(n)
        next_page_absolute = urljoin(url, f"page-{n_string}.html")
        response = requests.get(next_page_absolute)
    print(f"Nombre de pages trouvées pour la catégorie : {len(pagination_pages)}")
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
        print(f"Scan de la page {pages_url}")
        liens = soup.find_all('a', href=True, title=True)
        for lien in liens:
            relative_book_url = {'titre': lien['title'], 'lien': lien['href']}
            relative_books_urls.append(relative_book_url['lien'])
            print(f"Titre Récupéré : {relative_book_url['titre']}")
            print(f"Lien -> {relative_book_url['lien']}")
            print('---')
    print(f"Nombre de titres trouvés : {len(relative_books_urls)}")
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
    return absolute_books_urls


def scrape_category_books(absolute_books_urls):  # penser à la pagination !!
    for absolute_book_url in absolute_books_urls:
        scrape_book.main(absolute_book_url)
    print(f"Infos des livres de la catégorie récupérées")
    return True


"""
if __name__ == "main":
    main()
"""
main()
