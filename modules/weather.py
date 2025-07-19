import requests

def get_weather(api_key):
    """Récupère la météo à Paris, Saint-Ouen et Boulogne-Billancourt via OpenWeatherMap API"""
    weather_info = []
    cities = {
        "Paris": "Paris",
        "Saint-Ouen": "Saint-Ouen,FR",
        "Boulogne": "Boulogne-Billancourt,FR"
    }

    for city_name, city_query in cities.items():
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_query}&units=metric&appid={api_key}"
        try:
            response = requests.get(url)
            data = response.json()
            temp = round(data['main']['temp'])
            description = data['weather'][0]['description']
            weather_info.append(f"{city_name}: {temp}°C, {description}")
        except Exception as e:
            weather_info.append(f"{city_name}: Erreur - {str(e)}")

    return "\n".join(weather_info)