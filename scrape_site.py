from utils import html_to_soup


url = 'http://books.toscrape.com/'


def scrape_site():
    soup = html_to_soup(url)
    side_categories = soup.find_all('div', class_='side_categories')
    """
    trouver comment recuperer les URLS categories : 'ul', class_=nav nav-list, 'a', href=True 
    """
    #for categories in side_categories:
    #    categories = soup.find_all('ul', class_='nav-list')
    #    for categorie in categories:
    #        url_categorie = soup.find_all('a', href=True)
    #    print(url_categorie)


scrape_site()