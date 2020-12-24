import requests
from bs4 import BeautifulSoup as bs

url = "http://books.toscrape.com/catalogue/category/books/default_15/index.html"


def get_all_urls(url):
    response = requests.get(url)
    byte_data = response.content  # le contenu brut de la page
    soup = bs(byte_data, 'lxml')
    liens = soup.find_all('a', href=True, title=True)
    urls = []
    for lien in liens:
        book_url = {'titre': lien['title'], 'lien': lien['href']}
        urls.append(book_url['lien'])
        print(f"Titre : {book_url['titre']}, Lien : {book_url['lien']}")
        print('---')
    print(urls)
    print(len(urls))
    return urls


get_all_urls(url)
