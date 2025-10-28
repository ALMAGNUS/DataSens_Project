"""
Collecteur Data.gouv.fr - Datasets publics
Source : https://www.data.gouv.fr/api (API officielle)
"""
import requests
from datetime import datetime
from typing import List, Dict


class DataGouvCollector:
    """Collecte de métadonnées de datasets depuis data.gouv.fr"""
    
    def __init__(self):
        self.api_url = "https://www.data.gouv.fr/api/1"
    
    def collect(self, query: str = "france", page_size: int = 100) -> List[Dict]:
        """
        Collecte les datasets récents
        
        Args:
            query: Mot-clé de recherche
            page_size: Nombre de résultats
            
        Returns:
            Liste de dictionnaires contenant les métadonnées des datasets
        """
        documents = []
        
        try:
            url = f"{self.api_url}/datasets/"
            params = {
                "q": query,
                "page_size": page_size,
                "sort": "-created"
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            for dataset in data.get('data', []):
                doc = {
                    "id_externe": f"datagouv_{dataset.get('id')}",
                    "titre": dataset.get('title', 'Sans titre'),
                    "texte": dataset.get('description', '')[:1000],
                    "url": dataset.get('page', ''),
                    "date_publication": datetime.fromisoformat(dataset.get('created_at', datetime.now().isoformat()).replace('Z', '+00:00')),
                    "organisation": dataset.get('organization', {}).get('name'),
                    "nb_ressources": len(dataset.get('resources', [])),
                    "frequence_maj": dataset.get('frequency'),
                    "tags": [tag for tag in dataset.get('tags', [])],
                    "source": "Data.gouv.fr",
                    "type_donnee": "Web Scraping"
                }
                documents.append(doc)
                
        except Exception as e:
            print(f"❌ Erreur Data.gouv.fr: {e}")
        
        return documents


if __name__ == "__main__":
    collector = DataGouvCollector()
    datasets = collector.collect(query="france", page_size=50)
    print(f"✅ {len(datasets)} datasets Data.gouv.fr collectés")
