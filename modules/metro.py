import requests

def get_metro_status():
    """Récupère l'état des lignes de métro via l'API RATP"""
    status_info = []
    lines = {
        "6": "6",
        "9": "9",
        "10": "10",
        "13": "13",
        "14": "14"
    }

    url = "https://api-ratp.pierre-grimaud.fr/v4/traffic/metros"
    print(f"Tentative de connexion à l'API RATP...")

    try:
        response = requests.get(url)
        print(f"Statut de la réponse: {response.status_code}")
        response.raise_for_status()
        data = response.json()

        if 'result' not in data:
            raise Exception("Format de réponse invalide")

        # Création d'un dictionnaire pour un accès rapide aux statuts
        metro_status = {line['line']: line['message'] for line in data['result']['metros']}

        # Parcours des lignes demandées
        for line_num in lines:
            if line_num in metro_status:
                status_info.append(f"Ligne {line_num}: {metro_status[line_num]}")
            else:
                status_info.append(f"Ligne {line_num}: Information non disponible")

    except requests.exceptions.RequestException as e:
        print(f"Erreur de connexion à l'API RATP: {str(e)}")
        return f"Erreur de connexion à l'API RATP: {str(e)}"
    except Exception as e:
        print(f"Erreur inattendue: {str(e)}")
        return f"Erreur inattendue: {str(e)}"

    return "\n".join(status_info)