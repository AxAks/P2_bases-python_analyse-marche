from utils import html_to_soup, url_args_parser
import scrape_book
from urllib.parse import urljoin


#    url = "http://books.toscrape.com/catalogue/category/books/default_15/index.html" # juste pour les tests
def main():
    args = url_args_parser()
    relative_books_urls = get_books_urls(args.url)
    absolute_books_urls = reformat_relative_url_to_absolute(relative_books_urls)
    scrape_category_books_one_page(absolute_books_urls)


"""
Recupere toutes les urls des livres pour une page d'une catégorie.
Pas encore de prise en compte de la pagination
voir class=pager,previous,current,next  et url index.html,page-2.html etc ...
try/expect , continue ?
"""


def get_books_urls(url):  # fonctionne quand lancé seul
    soup = html_to_soup(url)
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
        print(absolute_book_url)
        absolute_books_urls.append(absolute_book_url)
    print(absolute_books_urls)
    return absolute_books_urls


def scrape_category_books_one_page(absolute_books_urls):  # penser à la pagination !!
    for absolute_book_url in absolute_books_urls:
        scrape_book.main(absolute_book_url)
    return True


"""
if __name__ == "main":
    main()
"""
main()
