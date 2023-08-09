import cv2
import os
import shutil

from script.services.stockage import database


def lancementTraitementDesImagesLive():
    # Création du dossier "traite" s'il n'existe pas
    if not os.path.exists(os.path.abspath("assets/images/traite")):
        os.makedirs(os.path.abspath("assets/images/traite"))

    # Chargement des images de la banque de pièces
    piece_images = []
    pieces_folder = os.path.abspath("assets/images/pieces")
    for piece_file in os.listdir(pieces_folder):
        if piece_file.endswith(".jpg"):
            piece_path = os.path.join(pieces_folder, piece_file)
            piece_image = cv2.imread(piece_path, cv2.IMREAD_GRAYSCALE)
            piece_images.append((piece_file, piece_image))

    # Parcours des images du dossier "live"
    live_folder = os.path.abspath("assets/images/live")
    for live_file in os.listdir(live_folder):
        if live_file.endswith(".jpg"):
            print(f"Image Live lu : {live_file}")
            live_path = os.path.join(live_folder, live_file)
            live_image = cv2.imread(live_path, cv2.IMREAD_GRAYSCALE)

            # Comparaison avec les images de la banque de pièces
            best_similarity = 0.0
            best_piece_name = None
            for piece_name, piece_image in piece_images:
                similarity = cv2.matchTemplate(live_image, piece_image, cv2.TM_CCOEFF_NORMED)
                testSimilarity = similarity[0][0]
                # TODO : Fix la similarité
                if testSimilarity < 0:
                    testSimilarity = best_similarity
                if testSimilarity > best_similarity:
                    best_similarity = testSimilarity
                    best_piece_name = piece_name
            print(f"Image Live comparé : {live_file, best_piece_name, best_similarity}")
            database.saveFileComparaison(live_file, best_piece_name, best_similarity)

            # Déplacement de l'image vers le dossier "traite"
            treated_path = os.path.join(os.path.abspath("assets/images/traite"), live_file)
            shutil.move(live_path, treated_path)
            print(f"Image traitée: {live_file}")
    database.closeDatabase()

