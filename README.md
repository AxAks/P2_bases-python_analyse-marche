# P2_bases-python_analyse-marché
Bookscrapper


# à compléter
 création et activation de l'environnement virtuel
 (dans un terminal)


Installation de virtualenv :
- sudo apt install virtualenv

se déplacer dans le projet à l'endroit où le dossier doit etre créé :
- cd P2_bases-python_analyse-marche

Création de l'environnement virtuel :
- python3.9 -m virtualenv venv_bookscrapper

Activation de l'environnement :
- source venv_bookscrapper/bin/activate

Installation du gestionnaire de paquets python 'pip' :
- wget https://bootstrap.pypa.io/get-pip.py (télécharger le script d'installation du gestionnaire de paquets python pip)
- python3.9 get-pip.py (installer pip dans l'environnement virtuel via l'execution du script téléchargé précédemment)
- pip --version (vérifier la version de pip installée)

Installation des dépendances du projet :
- pip install -r requirements.txt




Exécution de l'application (depuis le terminal) :

Se déplacer dans le dossier du projet :
- cd P2_bases-python_analyse-marche

Récupérer les informations d'un livre :
    - python scrape_book.py url (url doit etre l'url d'une page produit écrite en toutes lettres)
-> C'est pour une page produit seulement, les informations sont affichées mais ne sont pas sauvegardées dans un fichier CSV

Recupérer les informations des références d'une catégorie:
    - python scrape_category.py url
-> ("url" doit etre l'url d'une page categorie écrite en toute lettres)

Récupérer les informations de toutes les références du site :
    - python scrape_site.py
