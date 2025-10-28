"""
Collecteur NewsAPI - Actualités internationales
Source : https://newsapi.org (API officielle)
"""
import os
import requests
from datetime import datetime, timedelta
from typing import List, Dict
from dotenv import load_dotenv

load_dotenv()


class NewsAPICollector:
    """Collecte d'actualités depuis NewsAPI"""
    
    def __init__(self):
        self.api_key = os.getenv("NEWSAPI_KEY")
        self.base_url = "https://newsapi.org/v2"
    
    def collect(self, query: str = "France", sources: str = None, days_back: int = 7, page_size: int = 100) -> List[Dict]:
        """
        Collecte les articles récents
        
        Args:
            query: Mot-clé de recherche
            sources: Sources spécifiques (ex: "bbc-news,cnn")
            days_back: Nombre de jours en arrière
            page_size: Nombre d'articles
            
        Returns:
            Liste de dictionnaires contenant les articles
        """
        documents = []
        
        try:
            url = f"{self.base_url}/everything"
            from_date = (datetime.now() - timedelta(days=days_back)).strftime('%Y-%m-%d')
            
            params = {
                "q": query,
                "from": from_date,
                "sortBy": "publishedAt",
                "pageSize": page_size,
                "language": "fr",
                "apiKey": self.api_key
            }
            
            if sources:
                params["sources"] = sources
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()
            
            for article in data.get('articles', []):
                doc = {
                    "id_externe": f"newsapi_{article.get('url', '').split('/')[-1]}",
                    "titre": article.get('title', 'Sans titre'),
                    "texte": article.get('description', '')[:1000],
                    "url": article.get('url'),
                    "date_publication": datetime.fromisoformat(article.get('publishedAt', datetime.now().isoformat()).replace('Z', '+00:00')),
                    "auteur": article.get('author'),
                    "source_nom": article.get('source', {}).get('name'),
                    "image_url": article.get('urlToImage'),
                    "source": "NewsAPI",
                    "type_donnee": "API"
                }
                documents.append(doc)
                
        except Exception as e:
            print(f"❌ Erreur NewsAPI: {e}")
        
        return documents


if __name__ == "__main__":
    collector = NewsAPICollector()
    articles = collector.collect(query="France", page_size=50)
    print(f"✅ {len(articles)} articles NewsAPI collectés")
