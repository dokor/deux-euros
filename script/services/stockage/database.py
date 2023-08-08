# database.py
import sqlite3

# Connexion à la base de données (ou création si elle n'existe pas)
db_conn = sqlite3.connect("results.db")
db_cursor = db_conn.cursor()


# Création de la table dans la base de données si elle n'existe pas
def createDatabaseIfNotExist():
    db_cursor.execute('''
        CREATE TABLE IF NOT EXISTS comparison_results (
            image_name TEXT PRIMARY KEY,
            piece_name TEXT,
            similarity REAL
        )
    ''')


def saveFileComparaison(live_file, best_piece_name, best_similarity):
    createDatabaseIfNotExist()
    # Stockage du résultat dans la base de données
    db_cursor.execute('''
        INSERT INTO comparison_results (image_name, piece_name, similarity)
        VALUES (?, ?, ?)
    ''', (live_file, best_piece_name, best_similarity))
    db_conn.commit()

def closeDatabase():
    # Fermeture de la base de données
    db_conn.close()

