"""
Collecteur RSS Multi-Sources - Flux d'actualités
Sources : Le Monde, Franceinfo, 20 Minutes, BBC News
"""
import feedparser
from datetime import datetime
from typing import List, Dict


class RSSCollector:
    """Collecte d'articles depuis plusieurs flux RSS"""

    # Flux RSS français et internationaux
    RSS_FEEDS = {
        "Le Monde": "https://www.lemonde.fr/rss/une.xml",
        "Franceinfo": "https://www.francetvinfo.fr/titres.rss",
        "20 Minutes": "https://www.20minutes.fr/feeds/rss-une.xml",
        "BBC News France": "http://feeds.bbci.co.uk/news/world/europe/rss.xml",
        "France 24": "https://www.france24.com/fr/rss",
        "RFI": "https://www.rfi.fr/fr/rss"
    }

    def collect(self, feeds: Dict[str, str] = None, limit_per_feed: int = 50) -> List[Dict]:
        """
        Collecte les articles depuis les flux RSS

        Args:
            feeds: Dictionnaire {nom_source: url_rss} (utilise RSS_FEEDS par défaut)
            limit_per_feed: Nombre d'articles par flux

        Returns:
            Liste de dictionnaires contenant les articles
        """
        if feeds is None:
            feeds = self.RSS_FEEDS

        documents = []

        for source_name, rss_url in feeds.items():
            try:
                feed = feedparser.parse(rss_url)

                for entry in feed.entries[:limit_per_feed]:
                    # Parser la date de publication
                    if hasattr(entry, 'published_parsed') and entry.published_parsed:
                        date_pub = datetime(*entry.published_parsed[:6])
                    elif hasattr(entry, 'updated_parsed') and entry.updated_parsed:
                        date_pub = datetime(*entry.updated_parsed[:6])
                    else:
                        date_pub = datetime.now()

                    doc = {
                        "id_externe": f"rss_{source_name.lower().replace(' ', '_')}_{entry.get('id', len(documents))}",
                        "titre": entry.get('title', 'Sans titre'),
                        "texte": entry.get('summary', entry.get('description', ''))[:1000],
                        "url": entry.get('link'),
                        "date_publication": date_pub,
                        "auteur": entry.get('author'),
                        "categorie": entry.get('tags', [{}])[0].get('term') if entry.get('tags') else None,
                        "source": f"RSS - {source_name}",
                        "type_donnee": "API"
                    }
                    documents.append(doc)

                print(f"✅ {source_name}: {len(feed.entries[:limit_per_feed])} articles collectés")

            except Exception as e:
                print(f"❌ Erreur RSS {source_name}: {e}")

        return documents


if __name__ == "__main__":
    collector = RSSCollector()
    articles = collector.collect(limit_per_feed=20)
    print(f"\n✅ TOTAL: {len(articles)} articles RSS collectés")
