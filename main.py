import cv2
import time
import os

# Création du dossier "live" s'il n'existe pas
if not os.path.exists("live"):
    os.makedirs("live")

# Initialisation de la webcam
cap = cv2.VideoCapture(0)  # 0 correspond à la webcam principale

# Vérification si la webcam est ouverte
if not cap.isOpened():
    print("Erreur: Impossible d'ouvrir la webcam.")
    exit()

# Délai entre chaque capture d'image (en secondes)
capture_interval = 10

# Compteur pour suivre le temps écoulé
start_time = time.time()

try:
    while True:
        # Lecture d'une image de la webcam
        ret, frame = cap.read()

        if not ret:
            print("Erreur: Impossible de lire une image de la webcam.")
            break

        # Vérification du temps écoulé pour capturer une image toutes les 10 secondes
        current_time = time.time()
        if current_time - start_time >= capture_interval:
            # Création du chemin complet pour enregistrer l'image dans le dossier "live"
            image_filename = os.path.join("live", f"capture_{int(current_time)}.jpg")
            cv2.imwrite(image_filename, frame)
            print(f"Image capturée: {image_filename}")
            start_time = current_time

        # Affichage de l'image en temps réel (facultatif)
        cv2.imshow("Webcam", frame)

        # Arrêt de la boucle si la touche 'q' est pressée
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

finally:
    # Libération des ressources
    cap.release()
    cv2.destroyAllWindows()