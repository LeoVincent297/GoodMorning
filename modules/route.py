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

        steps = []

        for step in route.get('steps', []):
            instruction = step.get('html_instructions', '')
            
            if 'transit_details' in step:
                transit = step['transit_details']
                line_info = transit.get('line', {})
                line_name = line_info.get('short_name', '')
                vehicle_type = line_info.get('vehicle', {}).get('name', '')
                transit_info = f" (Ligne {line_name} - {vehicle_type})" if line_name or vehicle_type else ''
            else:
                transit_info = ''

            steps.append(f"• {instruction}{transit_info}")

        duration = route.get('duration', {}).get('text', 'N/A')
        distance = route.get('distance', {}).get('text', 'N/A')

        return (
            f"Durée estimée : {duration}\n"
            f"Distance : {distance}\n\n"
            "Itinéraire :\n"
            f"{chr(10).join(steps)}"
        )


    except Exception as e:
        return f"Erreur lors de la récupération de l'itinéraire: {str(e)}"