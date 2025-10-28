"""
Collecteur Reddit - Scraping de posts et commentaires
Source : r/france, r/Paris, r/Lyon (communautés citoyennes)
"""
import os
from datetime import datetime
from typing import List, Dict
import praw
from dotenv import load_dotenv

load_dotenv()


class RedditCollector:
    """Collecte de posts Reddit depuis des subreddits français"""
    
    def __init__(self):
        self.reddit = praw.Reddit(
            client_id=os.getenv("REDDIT_CLIENT_ID"),
            client_secret=os.getenv("REDDIT_CLIENT_SECRET"),
            user_agent="DataSens/1.0"
        )
    
    def collect(self, subreddits: List[str] = None, limit: int = 100) -> List[Dict]:
        """
        Collecte les posts récents depuis les subreddits spécifiés
        
        Args:
            subreddits: Liste des subreddits (défaut: france, Paris, Lyon)
            limit: Nombre de posts par subreddit
            
        Returns:
            Liste de dictionnaires contenant les posts
        """
        if subreddits is None:
            subreddits = ["france", "Paris", "Lyon"]
        
        documents = []
        
        for sub_name in subreddits:
            try:
                subreddit = self.reddit.subreddit(sub_name)
                
                for post in subreddit.hot(limit=limit):
                    doc = {
                        "id_externe": f"reddit_{post.id}",
                        "titre": post.title,
                        "texte": post.selftext[:1000] if post.selftext else "",
                        "url": f"https://reddit.com{post.permalink}",
                        "date_publication": datetime.fromtimestamp(post.created_utc),
                        "auteur": str(post.author),
                        "score": post.score,
                        "nb_commentaires": post.num_comments,
                        "subreddit": sub_name,
                        "source": "Reddit",
                        "type_donnee": "Web Scraping"
                    }
                    documents.append(doc)
                    
            except Exception as e:
                print(f"❌ Erreur Reddit r/{sub_name}: {e}")
        
        return documents


if __name__ == "__main__":
    collector = RedditCollector()
    posts = collector.collect(limit=10)
    print(f"✅ {len(posts)} posts Reddit collectés")
