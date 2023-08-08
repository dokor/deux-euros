import os
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
def crawl():
    # URL du site à analyser
    url = "https://www.collectiondemonnaie.net/euro/2/cotation_et_valeur_2_euro_commemorative.html"

    # En-tête de l'utilisateur pour simuler un navigateur
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"}

    # Obtenir le contenu HTML de la page
    response = requests.get(url, headers=headers)
    html_content = response.content

    # Utiliser BeautifulSoup pour analyser le HTML
    soup = BeautifulSoup(html_content, "html.parser")

    # Trouver toutes les balises <img> avec l'attribut src
    img_tags = soup.find_all("img", src=True)

    # Dossier pour enregistrer les images
    output_folder = "images/pieces"
    os.makedirs(output_folder, exist_ok=True)

    # Télécharger et enregistrer les images
    for img_tag in img_tags:
        img_url = img_tag["src"]
        img_url = urljoin(url, img_url)  # Gérer les URLs relatives
        img_name = img_url.split("/")[-1]  # Utiliser le dernier segment de l'URL comme nom de fichier

        img_response = requests.get(img_url)
        print("download ", img_name)
        with open(os.path.join(output_folder, img_name), "wb") as img_file:
            img_file.write(img_response.content)


    print("Téléchargement terminé.")