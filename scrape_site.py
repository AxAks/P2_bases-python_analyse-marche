from utils import html_to_soup, url_args_parser
# import scrape_category

"""
On entre l'URL du site en entrée
Le module récupère la liste des URL des categories.
"""

site_url = 'http://books.toscrape.com/'  #  test


def main():
    category_urls_list = scrape_site(site_url)
    for category_urls in category_urls_list:
        pass

"""
On donne l'URL du site en entrée de fonction
Le programme retourne une liste des URLs de toutes les catégories. 
"""


def scrape_site(site_url):
    category_urls_list = []
    soup = html_to_soup(site_url)
    category_urls = soup.select(".nav>li:nth-child(1)>ul:nth-child(2)>li>a")
    for category_url in category_urls:
        category_url = category_url['href']
        category_urls_list.append(category_url)
    print(category_urls_list)
    print(len(category_urls_list))
    return category_urls_list


"""
    # trouver comment recuperer les URLS categories : 'ul', class_=nav nav-list, 'a', href=True
    .nav > li:nth-child(1) > ul:nth-child(2) > li:nth-child(1) > a:nth-child(1)
    ex pour 1 : soup.select(".nav>li:nth-child(1)>ul:nth-child(2)>li:nth-child(1)>a:nth-child(1)")
    ex pour tous, à tester : soup.select(".nav>li:nth-child(1)>ul:nth-child(2)>li:nth-child(1)>a")   !!
"""

"""
if __name__ == "main":
    main()
"""
scrape_site(site_url)
