import cv2
import os
import shutil
import sqlite3

# Création du dossier "traité" s'il n'existe pas
if not os.path.exists("traité"):
    os.makedirs("traité")

# Connexion à la base de données (ou création si elle n'existe pas)
db_conn = sqlite3.connect("results.db")
db_cursor = db_conn.cursor()

# Création de la table dans la base de données si elle n'existe pas
db_cursor.execute('''
    CREATE TABLE IF NOT EXISTS comparison_results (
        image_name TEXT PRIMARY KEY,
        piece_name TEXT,
        similarity REAL
    )
''')

# Chargement des images de la banque de pièces
piece_images = []
for piece_file in os.listdir("pieces"):
    if piece_file.endswith(".jpg"):
        piece_path = os.path.join("pieces", piece_file)
        piece_image = cv2.imread(piece_path, cv2.IMREAD_GRAYSCALE)
        piece_images.append((piece_file, piece_image))

# Parcours des images du dossier "live"
for live_file in os.listdir("live"):
    if live_file.endswith(".jpg"):
        live_path = os.path.join("live", live_file)
        live_image = cv2.imread(live_path, cv2.IMREAD_GRAYSCALE)

        # Comparaison avec les images de la banque de pièces
        best_similarity = 0.0
        best_piece_name = None
        for piece_name, piece_image in piece_images:
            similarity = cv2.matchTemplate(live_image, piece_image, cv2.TM_CCOEFF_NORMED)
            if similarity > best_similarity:
                best_similarity = similarity
                best_piece_name = piece_name

        # Stockage du résultat dans la base de données
        db_cursor.execute('''
            INSERT INTO comparison_results (image_name, piece_name, similarity)
            VALUES (?, ?, ?)
        ''', (live_file, best_piece_name, best_similarity))
        db_conn.commit()

        # Déplacement de l'image vers le dossier "traité"
        treated_path = os.path.join("traité", live_file)
        shutil.move(live_path, treated_path)
        print(f"Image traitée: {live_file}")

# Fermeture de la base de données
db_conn.close()