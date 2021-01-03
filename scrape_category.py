import requests
from urllib.parse import urljoin, urlsplit
from utils import html_to_soup, url_args_parser, list_of_lists_to_flat_list
from scrape_book import get_book_infos, write_csv


def main():
    """
    Recupere toutes les urls des livres pour une page Catégorie donnée
    en récupère les informations
    et les copie dans un fichier CSV pour cette catégorie
    tout en enregistrant les images de couvertures des livres dans un dossier spécifique.
    """
    args = url_args_parser()
    pagination_pages = get_all_pages_category(args.url)
    relative_books_urls_list = get_category_books_urls(pagination_pages)
    relative_books_urls = list_of_lists_to_flat_list(relative_books_urls_list)
    absolute_books_urls = reformat_list_of_relative_urls_to_absolute(relative_books_urls)
    book_infos_list = add_book_infos_to_list(absolute_books_urls)
    write_csv_loop(book_infos_list)


def get_all_pages_category(url):
    """
    Verifie s'il existe plusieurs pages pour une catégorie donnée.
    Ajoute les URLs de toutes les pages de la catégorie à une liste
    Retourne la liste
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
    print(f"Nombre de pages trouvées pour la catégorie : {len(pagination_pages)}")
    print('---')
    return pagination_pages


def get_books_urls(page):
    """
    Récupère les URLs relatives des pages produit sur une page catégorie
    et les ajoute dans une liste.
    """
    soup = html_to_soup(page)
    liens = soup.find_all('a', href=True, title=True)
    print(f"Scan des URLs Produit de la page : {page}")
    relative_books_urls = [{'titre': lien['title'], 'lien': lien['href']} for lien in liens]
    print(f"Nombre de titres trouvés sur la page : {len(relative_books_urls)}")
    print("---")
    return relative_books_urls


def get_category_books_urls(pagination_pages):
    """
    Récupère les URLs relatives des pages produit de toutes les pages d'une catégorie
    et les ajoute à une liste.
    """
    relative_books_urls_list = [get_books_urls(page) for page in pagination_pages]
    return relative_books_urls_list


def reformat_list_of_relative_urls_to_absolute(relative_urls):
    """
    Reformate une liste d'URLs relatives en liste d'URLs absolues depuis la racine du site
    """
    absolute_urls_list = [urljoin("http://books.toscrape.com/catalogue/", relative_url['lien'].lstrip('../'))
                          for relative_url in relative_urls]
    print(f"{len(absolute_urls_list)} liens ont été reformatés")
    print("---")
    return absolute_urls_list


def add_book_infos_to_list(absolute_books_urls):
    """
    Pour une liste d'URLs produit, récupère les informations de chaque livre sous forme de dictionnaire
    et les ajoute à une liste
    """
    book_infos_list = [get_book_infos(absolute_book_url) for absolute_book_url in absolute_books_urls]
    return book_infos_list


def write_csv_loop(book_infos_list):
    """
    Boucle pour ecrire un dictionnaire de données dans un fichier CSV
    Utilise write_csv.
    """
    for book_infos in book_infos_list:
        write_csv(book_infos)
    print('---')
    print(f"{len(book_infos_list)} références copiées dans le fichier CSV")


if __name__ == "__main__":
    main()
