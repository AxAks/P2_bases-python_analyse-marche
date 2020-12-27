from utils import html_to_soup, url_args_parser
import scrape_category

"""
On entre l'URL du site en entrée
Le module récupère la liste des URL des categories.
"""

# site_url = 'http://books.toscrape.com/'


def main():
    categories_url = [
        "http://books.toscrape.com/catalogue/category/books/travel_2/index.html",
        "http://books.toscrape.com/catalogue/category/books/mystery_3/index.html"
    ]  #  juste un test
    for url in categories_url:
        scrape_category.main()
        print(url)
        print("ici")
    return True
"""
    args = url_args_parser()
    site_url = scrape_site(args.url)
"""
"""
def scrape_site(site_url):
    category_urls = []
    soup = html_to_soup(site_url)
    side_categories = soup.find_all('div', class_='side_categories')
    
    # trouver comment recuperer les URLS categories : 'ul', class_=nav nav-list, 'a', href=True
    .nav > li:nth-child(1) > ul:nth-child(2) > li:nth-child(1) > a:nth-child(1)
    ex pour 1 : soup.select(".nav>li:nth-child(1)>ul:nth-child(2)>li:nth-child(1)>a:nth-child(1)")
    ex pour tous, à tester : soup.select(".nav>li:nth-child(1)>ul:nth-child(2)>li:nth-child(1)>a")   !!

    for categories in side_categories:
        categories = soup.find_all('ul', class_='nav-list')
        for category in categories:
            url_category = soup.find_all('a', href=True)
            category_urls.append(url_category)
    print(category_urls)
    return category_urls
"""

main()
