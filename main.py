from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime
import os
from dotenv import load_dotenv
import schedule
import time

#Own modules importation
from modules.weather import get_weather
from modules.metro import get_metro_status
from modules.route import get_route
from modules.emailer import send_email
from modules.writing import write_to_icloud
# Chargement des variables d'environnement
load_dotenv()

# Configuration des variables
EMAIL_ADDRESS = os.getenv("EMAIL_ADDRESS")
EMAIL_PASSWORD = os.getenv("EMAIL_PASSWORD")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")
RATP_API_KEY = os.getenv("RATP_API_KEY")
GOOGLE_MAPS_API_KEY = os.getenv("GOOGLE_MAPS_API_KEY")
PATH_RECAP = os.path.expanduser("~/GoodMorning/recap.txt")
DESTINATAIRE = "vincentleo1908@gmail.com"

print(f"Email configuré : {EMAIL_ADDRESS}")
print(f"Clé météo configurée : {'Oui' if WEATHER_API_KEY else 'Non'}")
print(f"Clé RATP configurée : {'Oui' if RATP_API_KEY else 'Non'}")
print(f"Clé Google Maps configurée : {'Oui' if GOOGLE_MAPS_API_KEY else 'Non'}")
print(f"Chemin iCloud : {PATH_RECAP}")

def update_info():
    """Met à jour les informations et les envoie par email et sur iCloud"""
    # Récupération des informations
    weather_info = get_weather(WEATHER_API_KEY)
    metro_info = get_metro_status()
    route_info = get_route(GOOGLE_MAPS_API_KEY)

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
    send_email(content, EMAIL_ADDRESS, EMAIL_PASSWORD, DESTINATAIRE)
    write_to_icloud(content, PATH_RECAP)

def main():
    """Fonction principale qui planifie l'exécution quotidienne"""
    heure = "12:53"
    schedule.every().day.at(heure).do(update_info)
    print(f"Le script est en cours d'exécution. Une notification à {heure}")

    while True:
        schedule.run_pending()
        time.sleep(60)

if __name__ == "__main__":
    main()
