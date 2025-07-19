import requests
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv
import schedule
import time

# Chargement des variables d'environnement
load_dotenv()

# Configuration des variables
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
RATP_API_KEY = os.getenv("RATP_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
ICLOUD_PATH = os.path.expanduser("~/GoodMorning/recap.txt")
DESTINATAIRE = "vincentleo1908@gmail.com"

print(f"Email configuré : {EMAIL_ADDRESS}")
print(f"Clé météo configurée : {'Oui' if WEATHER_API_KEY else 'Non'}")
print(f"Clé RATP configurée : {'Oui' if RATP_API_KEY else 'Non'}")
print(f"Clé Google Maps configurée : {'Oui' if GOOGLE_MAPS_API_KEY else 'Non'}")
print(f"Chemin iCloud : {ICLOUD_PATH}")

def get_weather():
    """Récupère la météo à Paris, Saint-Ouen et Boulogne-Billancourt via OpenWeatherMap API"""
    weather_info = []
    cities = {
        "Paris": "Paris",
        "Saint-Ouen": "Saint-Ouen,FR",
        "Boulogne": "Boulogne-Billancourt,FR"
    }

    for city_name, city_query in cities.items():
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_query}&units=metric&appid={WEATHER_API_KEY}"
        try:
            response = requests.get(url)
            data = response.json()
            temp = round(data['main']['temp'])
            description = data['weather'][0]['description']
            weather_info.append(f"{city_name}: {temp}°C, {description}")
        except Exception as e:
            weather_info.append(f"{city_name}: Erreur - {str(e)}")

    return "\n".join(weather_info)

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

def get_route():
    """Récupère le meilleur itinéraire entre deux points via Google Maps API"""
    origin = "231 boulevard Jean Jaurès, Boulogne-Billancourt"
    destination = "8 rue de la clef des champs, Saint-Ouen"

    url = f"https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": GOOGLE_MAPS_API_KEY,
        "mode": "transit",  # Pour les transports en commun
        "language": "fr"
    }

    try:
        response = requests.get(url, params=params)
        response.raise_for_status()
        data = response.json()

        if data['status'] != 'OK':
            return "Impossible de calculer l'itinéraire"

        route = data['routes'][0]['legs'][0]
        steps = []

        for step in route['steps']:
            if 'transit_details' in step:
                transit = step['transit_details']
                line = transit.get('line', {}).get('short_name', '')
                vehicle = transit.get('line', {}).get('vehicle', {}).get('name', '')
                steps.append(f"• {step['html_instructions']} (Ligne {line} {vehicle})")
            else:
                steps.append(f"• {step['html_instructions']}")

        duration = route['duration']['text']
        distance = route['distance']['text']

        return f"""Durée estimée : {duration}
                Distance : {distance}

                Itinéraire :
                {chr(10).join(steps)}"""

    except Exception as e:
        return f"Erreur lors de la récupération de l'itinéraire: {str(e)}"

def send_email(content):
    """Envoie l'email avec les informations du jour"""
    msg = MIMEMultipart()
    msg['From'] = EMAIL_ADDRESS
    msg['To'] = DESTINATAIRE
    msg['Subject'] = "Info du jour"

    msg.attach(MIMEText(content, 'plain'))

    # Envoi de l'email
    try:
        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(EMAIL_ADDRESS, EMAIL_PASSWORD)
        server.send_message(msg)
        server.quit()
        print("Email envoyé avec succès!")
    except Exception as e:
        print(f"Erreur lors de l'envoi de l'email: {str(e)}")

def write_to_icloud(content):
    """Écrit les informations du jour dans un fichier sur iCloud Drive"""
    try:
        # Création du dossier si nécessaire
        os.makedirs(os.path.dirname(ICLOUD_PATH), exist_ok=True)

        with open(ICLOUD_PATH, 'w', encoding='utf-8') as f:
            f.write(content)
        print("Informations écrites avec succès dans le fichier iCloud!")
    except Exception as e:
        print(f"Erreur lors de l'écriture dans le fichier: {str(e)}")

def update_info():
    """Met à jour les informations et les envoie par email et sur iCloud"""
    # Récupération des informations
    weather_info = get_weather()
    metro_info = get_metro_status()
    route_info = get_route()

    # Création du contenu
    content = f"""Info du {datetime.now().strftime('%d/%m/%Y %H:%M')}

🌤️ Météo :
{weather_info}

🚇 État des lignes :
{metro_info}

🗺️ Itinéraire du jour :
{route_info}

Bonne journée !"""

    # Envoi par email et écriture sur iCloud
    send_email(content)
    write_to_icloud(content)

def main():
    # update_info()
    """Fonction principale qui planifie l'exécution quotidienne"""
    # Planification de l'exécution à 21h00
    heure = "11:30"
    schedule.every().day.at(heure).do(update_info)

    print(f"Le script est en cours d'exécution. Une notification à {heure}")

    # Boucle principale
    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
