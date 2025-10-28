"""
Collecteur Vie Publique - Actualités gouvernementales
Source : https://www.vie-publique.fr (flux RSS + scraping)
"""
import feedparser
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from typing import List, Dict


class ViePubliqueCollector:
    """Collecte d'actualités depuis vie-publique.fr"""
    
    def __init__(self):
        self.rss_url = "https://www.vie-publique.fr/rss.xml"
        self.base_url = "https://www.vie-publique.fr"
    
    def collect(self, limit: int = 100) -> List[Dict]:
        """
        Collecte les actualités récentes via RSS
        
        Args:
            limit: Nombre d'articles à récupérer
            
        Returns:
            Liste de dictionnaires contenant les articles
        """
        documents = []
        
        try:
            feed = feedparser.parse(self.rss_url)
            
            for entry in feed.entries[:limit]:
                # Enrichissement avec scraping de la page complète
                texte_complet = self._scrape_article(entry.link)
                
                doc = {
                    "id_externe": f"vie_publique_{entry.id}",
                    "titre": entry.title,
                    "texte": texte_complet[:1000] if texte_complet else entry.summary[:1000],
                    "url": entry.link,
                    "date_publication": datetime(*entry.published_parsed[:6]) if hasattr(entry, 'published_parsed') else datetime.now(),
                    "categorie": entry.get('tags', [{}])[0].get('term', 'Actualité'),
                    "source": "Vie Publique",
                    "type_donnee": "Web Scraping"
                }
                documents.append(doc)
                
        except Exception as e:
            print(f"❌ Erreur Vie Publique RSS: {e}")
        
        return documents
    
    def _scrape_article(self, url: str) -> str:
        """Scrape le contenu complet d'un article"""
        try:
            response = requests.get(url, timeout=10)
            response.raise_for_status()
            soup = BeautifulSoup(response.content, 'html.parser')
            
            # Trouver le contenu principal (adapter selon structure réelle)
            content = soup.find('div', class_='content-article')
            if content:
                return content.get_text(strip=True)
        except:
            pass
        return ""


if __name__ == "__main__":
    collector = ViePubliqueCollector()
    articles = collector.collect(limit=20)
    print(f"✅ {len(articles)} articles Vie Publique collectés")
