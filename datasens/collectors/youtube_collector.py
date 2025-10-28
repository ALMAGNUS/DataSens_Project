"""
Collecteur YouTube - Vidéos et commentaires
Source : Chaînes officielles françaises (gouvernement, médias citoyens)
"""
import os
from datetime import datetime
from typing import List, Dict
from googleapiclient.discovery import build
from dotenv import load_dotenv

load_dotenv()


class YouTubeCollector:
    """Collecte de vidéos YouTube depuis des chaînes françaises"""

    def __init__(self):
        self.api_key = os.getenv("YOUTUBE_API_KEY")
        self.youtube = build('youtube', 'v3', developerKey=self.api_key)

    def collect(self, channel_ids: List[str] = None, max_results: int = 50) -> List[Dict]:
        """
        Collecte les vidéos récentes depuis les chaînes spécifiées

        Args:
            channel_ids: Liste des IDs de chaînes YouTube
            max_results: Nombre de vidéos par chaîne

        Returns:
            Liste de dictionnaires contenant les vidéos
        """
        if channel_ids is None:
            # Chaînes par défaut : vie-publique.fr, BFMTV, France24
            channel_ids = [
                "UCJcZQmhUE8s8Ɨ51B8X4Q",  # Vie Publique (exemple)
                "UChqUTb7kYRX8-EiaN3XFom",  # BFMTV
                "UCQfwfsi5VrQ8yKZ-UWmAEFg"   # France 24
            ]

        documents = []

        for channel_id in channel_ids:
            try:
                # Recherche des vidéos de la chaîne
                request = self.youtube.search().list(
                    part="snippet",
                    channelId=channel_id,
                    maxResults=max_results,
                    order="date",
                    type="video"
                )
                response = request.execute()

                for item in response.get('items', []):
                    snippet = item['snippet']
                    video_id = item['id']['videoId']

                    doc = {
                        "id_externe": f"youtube_{video_id}",
                        "titre": snippet['title'],
                        "texte": snippet['description'][:1000],
                        "url": f"https://www.youtube.com/watch?v={video_id}",
                        "date_publication": datetime.fromisoformat(snippet['publishedAt'].replace('Z', '+00:00')),
                        "auteur": snippet['channelTitle'],
                        "channel_id": channel_id,
                        "source": "YouTube",
                        "type_donnee": "Web Scraping"
                    }
                    documents.append(doc)

            except Exception as e:
                print(f"❌ Erreur YouTube {channel_id}: {e}")

        return documents


if __name__ == "__main__":
    collector = YouTubeCollector()
    videos = collector.collect(max_results=10)
    print(f"✅ {len(videos)} vidéos YouTube collectées")
