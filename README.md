# GoodMorning ☀️

Un assistant Python automatisé pour bien commencer la journée !

Chaque matin, ce script récupère et envoie par email :

- La météo de vos villes préférées
- L’état des lignes de métro importantes
- Un itinéraire Google Maps vers votre lieu de travail
- (Optionnel) Un fichier de note iCloud

---

## Structure du projet

```bash
GoodMorning/
│
├── modules/               # Fonctions regroupées par thème
│   ├── __init__.py
│   ├── weather.py         # get_weather()
│   ├── metro.py           # get_metro_status()
│   ├── maps.py            # get_route()
│   └── emailer.py         # send_email()
│
├── main.py                # Script principal
├── requirements.txt       # Dépendances Python
└── README.md              # Documentation
```
## Installation
### 1. Cloner le dépôt
```bash
git clone https://github.com/<ton-utilisateur>/GoodMorning.git
cd GoodMorning
```

### 2. Créer un environnement virtuel
```bash
python3 -m venv env
source env/bin/activate
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```
## Configuration

Ajoute dans main.py ou un fichier .env (à sécuriser) les informations suivantes :

    Ton adresse email Gmail + mot de passe applicatif

    Ta clé API OpenWeather

    Ta clé API Google Maps

EMAIL_ADDRESS = "ton_email@gmail.com"
EMAIL_PASSWORD = "ton_mot_de_passe_app"
DESTINATAIRE = "destinataire@email.com"
WEATHER_API_KEY = "ta_cle_openweather"
GOOGLE_MAPS_API_KEY = "ta_cle_google_maps"

## Lancement
```bash
python3 main.py
```
Ou bien avec screen pour l’exécuter en arrière-plan :
```bash
screen -S morning
source env/bin/activate
python3 main.py
```

## Programmation automatique

Le script utilise schedule pour s’exécuter tous les jours à 08h00 :
```python
schedule.every().day.at("08:00").do(update_info)
```

Tu peux modifier l’heure comme tu veux.
Envoi d’email

Le script assemble les infos météo, métro, itinéraire, puis envoie un email au destinataire.
## TODO / Améliorations possibles

    Interface Web ou CLI

    Ajout d'un historique journalier

    Support d'autres moyens de transport

    Intégration iCalendar / Google Calendar

## Licence

Projet personnel développé sur Raspberry Pi.

---
