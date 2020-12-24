import requests
from bs4 import BeautifulSoup as bs
import scrape_book
import argparse
from urllib.parse import urljoin


def main():  # ne fonctionne pas ( un argument url ne passe pas à un moment)
    parser = argparse.ArgumentParser()
    parser.add_argument("url", help="scrapes all the products URLs on the page given as argument", type=str)
    args = parser.parse_args()
    # url = "http://books.toscrape.com/catalogue/category/books/default_15/index.html"
    relative_books_urls = get_all_urls(args.url)
    absolute_books_urls = reformat_relative_url_to_absolute(relative_books_urls)
    scrape_category_books_one_page(absolute_books_urls)



"""
Recupere toutes les urls des livres pour une page d'une catégorie.
Pas encore de prise en compte de la pagination
voir class=pager,previous,current,next  et url index.html,page-2.html etc ...
try/expect , continue ?
"""


def get_all_urls(url):  # fonctionne quand lancé seul
    response = requests.get(url)
    byte_data = response.content  # le contenu brut de la page
    soup = bs(byte_data, 'lxml')
    liens = soup.find_all('a', href=True, title=True)
    relative_books_urls = []
    for lien in liens:
        relative_book_url = {'titre': lien['title'], 'lien': lien['href']}
        relative_books_urls.append(relative_book_url['lien'])
        print(f"Titre : {relative_book_url['titre']}, Lien : {relative_book_url['lien']}")
        print('---')
    print(relative_books_urls)
    print(len(relative_books_urls))
    return relative_books_urls


"""
Reformate les URLs relatives d'une liste en URL absolues depuis la racine du site
"""


def reformat_relative_url_to_absolute(relative_books_urls):
    absolute_books_urls = []
    for relative_book_url in relative_books_urls:
        relative_book_url = relative_book_url.replace(relative_book_url[:9], '')
        absolute_book_url = urljoin("http://books.toscrape.com/catalogue/", relative_book_url)
        print(absolute_book_url) # a travailler pour avoir une liste d'URL chamin absolu vers les pages produit
        absolute_books_urls.append(absolute_book_url)
    print(absolute_books_urls)
    return absolute_books_urls


def scrape_category_books_one_page(absolute_books_urls):
    for absolute_book_url in absolute_books_urls:
        scrape_book.main(absolute_book_url)
    print(absolute_book_url)
    return True

"""
if __name__ == "main":
    main()
"""
main()
#reformat_relative_url_to_absolute([''])

