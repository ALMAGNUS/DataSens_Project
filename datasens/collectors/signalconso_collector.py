"""
Collecteur SignalConso - Signalements citoyens
Source : https://signal.conso.gouv.fr (API publique)
"""
import requests
from datetime import datetime
from typing import List, Dict


class SignalConsoCollector:
    """Collecte des signalements citoyens depuis SignalConso"""
    
    def __init__(self):
        self.base_url = "https://signal.conso.gouv.fr/api/reports"
    
    def collect(self, limit: int = 100) -> List[Dict]:
        """
        Collecte les signalements récents
        
        Args:
            limit: Nombre de signalements à récupérer
            
        Returns:
            Liste de dictionnaires contenant les signalements
        """
        documents = []
        
        try:
            # API publique SignalConso (hypothétique, adapter selon la vraie API)
            params = {
                "limit": limit,
                "offset": 0,
                "sortBy": "creationDate"
            }
            
            response = requests.get(self.base_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            for item in data.get('reports', []):
                doc = {
                    "id_externe": f"signalconso_{item.get('id')}",
                    "titre": f"Signalement {item.get('category', 'Inconnu')}",
                    "texte": item.get('description', '')[:1000],
                    "url": f"https://signal.conso.gouv.fr/report/{item.get('id')}",
                    "date_publication": datetime.fromisoformat(item.get('creationDate', datetime.now().isoformat())),
                    "categorie": item.get('category'),
                    "entreprise": item.get('company', {}).get('name'),
                    "statut": item.get('status'),
                    "source": "SignalConso",
                    "type_donnee": "Web Scraping"
                }
                documents.append(doc)
                
        except Exception as e:
            print(f"❌ Erreur SignalConso: {e}")
        
        return documents


if __name__ == "__main__":
    collector = SignalConsoCollector()
    signalements = collector.collect(limit=50)
    print(f"✅ {len(signalements)} signalements SignalConso collectés")
