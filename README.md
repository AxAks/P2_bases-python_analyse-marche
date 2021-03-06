# P2_bases-python-analyse-marché
***
Ce scrapper permet de récupérer les informations des produits présents sur le site http://books.toscrape.com/.  
Cela peut être pour une référence unique, une catégorie entière ou l'ensemble des références du site.
***

## Chapitres

1. [Prérequis](#prerequis)
2. [Installation](#installation)
3. [Exécution du code](#execution-du-code)

***
## 1. Pré-requis <a name="prerequis"></a>

- Python 3.9
- Virtualenv

***
## 2. Installation (depuis le terminal) <a name="installation"></a>

1. __Téléchargement du projet :__

Via Git :

$ git clone https://github.com/AxAks/P2_bases-python_analyse-marche.git

Via le Web :

- Visiter la page : https://github.com/AxAks/P2_bases-python_analyse-marche
- Cliquer sur "Code"
- Télécharger le projet

2. __Création et activation de l'environnement virtuel  :__

- _Installation de virtualenv :_  
$ sudo apt install virtualenv

- _Se déplacer à la racine du projet :_  
$ cd P2_bases-python_analyse-marche

- _Création de l'environnement virtuel :_  
$ python3.9 -m virtualenv venv_bookscrapper

- _Activation de l'environnement :_  
$ source venv_bookscrapper/bin/activate

- _Installation du gestionnaire de paquets python 'pip' dans l'environnement :_  
$ wget https://bootstrap.pypa.io/get-pip.py  
$ python3.9 get-pip.py  
$ pip --version  

- _Installation des dépendances du projet dans l'environnement :_  
$ pip install -r requirements.txt

***
## 3. Exécution du code (depuis le terminal à la racine du projet) <a name="execution-du-code"></a>

- _Récupérer les informations d'une référence unique :_  
Les informations du produit sont affichées à l'ecran mais ne sont pas sauvegardées dans un fichier CSV  
("url" doit être l'url d'une page produit écrite en toutes lettres)  
$ python scrape_book.py "url"  


- _Récupérer les informations des références d'une catégorie:_  
("url" doit être l'url d'une page categorie écrite en toutes lettres)  
$ python scrape_category.py "url"  

- _Récupérer les informations de toutes les références du site :_  
$ python scrape_site.py
***