import os
def write_to_icloud(content, path):
    """Écrit les informations du jour dans un fichier sur iCloud Drive"""
    try:
        # Création du dossier si nécessaire
        os.makedirs(os.path.dirname(path), exist_ok=True)

        with open(path, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Informations écrites avec succès dans le fichier iCloud!")
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier: {str(e)}")