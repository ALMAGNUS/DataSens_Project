"""
Collecteur Trustpilot - Avis consommateurs
Source : Trustpilot France (scraping éthique avec BeautifulSoup)
"""
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict
import time


class TrustpilotCollector:
    """Collecte d'avis consommateurs depuis Trustpilot (scraping éthique)"""
    
    def __init__(self):
        self.base_url = "https://fr.trustpilot.com"
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
    
    def collect(self, companies: List[str] = None, max_reviews: int = 50) -> List[Dict]:
        """
        Collecte les avis récents pour des entreprises françaises
        
        Args:
            companies: Liste des noms d'entreprises (slugs Trustpilot)
            max_reviews: Nombre d'avis par entreprise
            
        Returns:
            Liste de dictionnaires contenant les avis
        """
        if companies is None:
            # Exemples d'entreprises françaises
            companies = ["sncf", "edf", "orange-france"]
        
        documents = []
        
        for company in companies:
            try:
                url = f"{self.base_url}/review/{company}"
                response = requests.get(url, headers=self.headers, timeout=30)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.content, 'html.parser')
                reviews = soup.find_all('article', class_='review', limit=max_reviews)
                
                for review in reviews:
                    try:
                        title_elem = review.find('h2', class_='review-title')
                        text_elem = review.find('p', class_='review-text')
                        rating_elem = review.find('div', class_='star-rating')
                        
                        doc = {
                            "id_externe": f"trustpilot_{company}_{len(documents)}",
                            "titre": title_elem.get_text(strip=True) if title_elem else "Avis",
                            "texte": text_elem.get_text(strip=True)[:1000] if text_elem else "",
                            "url": url,
                            "date_publication": datetime.now(),  # Parser la date réelle si disponible
                            "note": rating_elem.get('data-rating') if rating_elem else None,
                            "entreprise": company,
                            "source": "Trustpilot",
                            "type_donnee": "Web Scraping"
                        }
                        documents.append(doc)
                    except Exception as e:
                        print(f"⚠️ Erreur parsing avis: {e}")
                
                time.sleep(2)  # Politesse : attendre entre les requêtes
                
            except Exception as e:
                print(f"❌ Erreur Trustpilot {company}: {e}")
        
        return documents


if __name__ == "__main__":
    collector = TrustpilotCollector()
    avis = collector.collect(max_reviews=10)
    print(f"✅ {len(avis)} avis Trustpilot collectés")
