import requests

def get_route(api_key):
    """Récupère le meilleur itinéraire entre deux points via Google Maps API"""
    origin = "231 boulevard Jean Jaurès, Boulogne-Billancourt"
    destination = "8 rue de la clef des champs, Saint-Ouen"

    url = f"https://maps.googleapis.com/maps/api/directions/json"
    params = {
        "origin": origin,
        "destination": destination,
        "key": api_key,
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