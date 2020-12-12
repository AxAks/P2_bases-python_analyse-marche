import pandas as pd

# url = 'http://books.toscrape.com/catalogue/holidays-on-ice_167/index.html'
url = 'http://books.toscrape.com/catalogue/holidays-on-ice_167/'

def get_one_product(url):
    product_info = pd.read_html(url)
    print(len(product_info))
    print(product_info)



get_one_product(url)
