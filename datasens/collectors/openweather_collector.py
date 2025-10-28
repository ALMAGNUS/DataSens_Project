"""
Collecteur OpenWeatherMap - Données météo
Source : https://openweathermap.org/api (API officielle)
"""
import os
import requests
from datetime import datetime
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


class OpenWeatherCollector:
    """Collecte de données météo depuis OpenWeatherMap"""
    
    def __init__(self):
        self.api_key = os.getenv("OWM_API_KEY")
        self.base_url = "https://api.openweathermap.org/data/2.5"
    
    def collect(self, cities: List[str] = None) -> List[Dict]:
        """
        Collecte les données météo pour des villes françaises
        
        Args:
            cities: Liste de villes (défaut: Paris, Lyon, Marseille)
            
        Returns:
            Liste de dictionnaires contenant les données météo
        """
        if cities is None:
            cities = ["Paris,FR", "Lyon,FR", "Marseille,FR", "Toulouse,FR", "Nice,FR"]
        
        documents = []
        
        for city in cities:
            try:
                url = f"{self.base_url}/weather"
                params = {
                    "q": city,
                    "appid": self.api_key,
                    "units": "metric",
                    "lang": "fr"
                }
                
                response = requests.get(url, params=params, timeout=30)
                response.raise_for_status()
                data = response.json()
                
                doc = {
                    "id_externe": f"owm_{data['id']}_{int(datetime.now().timestamp())}",
                    "titre": f"Météo {data['name']}",
                    "texte": f"{data['weather'][0]['description']} - {data['main']['temp']}°C",
                    "ville": data['name'],
                    "pays": data['sys']['country'],
                    "temperature": data['main']['temp'],
                    "temperature_ressentie": data['main']['feels_like'],
                    "humidite": data['main']['humidity'],
                    "pression": data['main']['pressure'],
                    "vent_vitesse": data['wind']['speed'],
                    "description": data['weather'][0]['description'],
                    "date_releve": datetime.fromtimestamp(data['dt']),
                    "source": "OpenWeatherMap",
                    "type_donnee": "API"
                }
                documents.append(doc)
                
            except Exception as e:
                print(f"❌ Erreur OpenWeatherMap {city}: {e}")
        
        return documents


if __name__ == "__main__":
    collector = OpenWeatherCollector()
    meteo = collector.collect()
    print(f"✅ {len(meteo)} relevés météo collectés")
