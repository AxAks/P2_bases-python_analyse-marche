# P2_bases-python_analyse-marche
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


Exécution de l'application :

- cd P2_bases-python_analyse-marche
- python scrape_book.py url (url doit etre une url écrite en toutes lettres)
-> C'est pour une page produit seulement, à l'envler et remplacer quand le scrapping site sera complet