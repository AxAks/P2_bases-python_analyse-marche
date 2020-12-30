from utils import html_to_soup, write_csv_loop
from urllib.parse import urljoin
from scrape_category import get_all_pages_category,\
    get_books_urls, reformat_relative_url_to_absolute, scrape_category_books

"""
On entre l'URL du site en entrée
Le module récupère la liste des URL des categories.
"""

site_url = 'http://books.toscrape.com/'  #  test


def main():
    relative_category_urls_list = scrape_site(site_url)
    absolute_category_urls_list = get_absolute_category_urls_list(relative_category_urls_list) # liste des URL categories index
    all_categories_pages_list = get_category_pagination_pages(absolute_category_urls_list)  #  liste de listes des URL des différentes pages categories (pas juste une liste de str!!!
    all_pages_list = reformat_category_pages_list(all_categories_pages_list)
    relative_books_urls_list = get_relative_books_urls_list(all_pages_list)
    absolute_books_urls_list = relative_to_absolute_books_url_list(relative_books_urls_list)
    book_infos_list = get_all_books_infos_list(absolute_books_urls_list)
    write_csv_loop(book_infos_list)
    print(f"{len(book_infos_list)} références copiées")


"""
On donne l'URL du site en entrée de fonction
Le programme retourne une liste des URLs de toutes les catégories. 
"""


def scrape_site(site_url):
    relative_category_urls_list = []
    soup = html_to_soup(site_url)
    category_urls = soup.select(".nav>li:nth-child(1)>ul:nth-child(2)>li>a")
    for category_url in category_urls:
        category_url = category_url['href']
        relative_category_urls_list.append(category_url)
    return relative_category_urls_list


"""
Reformate les URLs Categories relatives en URLs Absolues.
"""


def get_absolute_category_urls_list(relative_category_urls_list):
    absolute_category_urls_list = []
    for relative_category_url in relative_category_urls_list:
        absolute_category_url = urljoin(site_url, relative_category_url)
        absolute_category_urls_list.append(absolute_category_url)
    print(absolute_category_urls_list)
    print(len(absolute_category_urls_list))
    return absolute_category_urls_list


"""
On recupère les URLs de toutes les pages pour chaque categorie. 
"""


def get_category_pagination_pages(absolute_category_urls_list):
    all_categories_pages = []
    for absolute_category_url in absolute_category_urls_list:
        category_pagination_pages = get_all_pages_category(absolute_category_url)
        all_categories_pages.append(category_pagination_pages)
        print(category_pagination_pages)
        print(all_categories_pages)
    return all_categories_pages


def get_relative_books_urls_list(all_pages_list):
    relative_books_urls_list = []
    for page in all_pages_list:
        relative_books_urls = get_books_urls(page)
        relative_books_urls_list.append(relative_books_urls)
        print(page)
    print('*****')
    print('*****')
    print(relative_books_urls_list)
    print(len(relative_books_urls_list))
    return relative_books_urls_list


def relative_to_absolute_books_url_list(relative_books_urls_list):
    absolute_book_url_list = []
    for relative_book_url in relative_books_urls_list:
        absolute_book_url = reformat_relative_url_to_absolute(relative_book_url)
        absolute_book_url_list.append(absolute_book_url)
    return absolute_book_url_list


def get_all_books_infos_list(absolute_books_urls_list):
    book_infos_list = []
    for absolute_book_url in absolute_books_urls_list: # on boucle bien sur toutes les pages produit
        book_infos = scrape_category_books(absolute_book_url)
        book_infos_list.append(book_infos)
        print(book_infos)
        print(book_infos_list)
        print('****')
    print('****')
    print(book_infos_list) # mais à la fin je n'ai que 50 entrées dans la liste
    print(len(book_infos_list))
    return book_infos_list

"""
transforme la liste de liste en liste simple
"""


def reformat_category_pages_list(all_categories_pages_list):
    all_pages_list = []
    for category_pages_list in all_categories_pages_list:
        for category_page in category_pages_list:
            all_pages_list.append(category_page)
    print(all_pages_list)
    return all_pages_list

"""
if __name__ == "main":
    main()
"""
main()
