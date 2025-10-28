#!/usr/bin/env python3
"""
Test Reddit API credentials
"""

import os

from dotenv import load_dotenv

load_dotenv()

try:
    import praw

    REDDIT_CLIENT_ID = os.getenv("REDDIT_CLIENT_ID")
    REDDIT_CLIENT_SECRET = os.getenv("REDDIT_CLIENT_SECRET")

    print("🔍 Test Reddit API")
    print(f"   Client ID: {REDDIT_CLIENT_ID[:10]}...")
    print(f"   Secret: {REDDIT_CLIENT_SECRET[:10]}...")

    reddit = praw.Reddit(
        client_id=REDDIT_CLIENT_ID,
        client_secret=REDDIT_CLIENT_SECRET,
        user_agent="datasens/1.0 (educational project)"
    )

    # Test : récupérer 5 posts de r/france
    subreddit = reddit.subreddit("france")
    posts = list(subreddit.hot(limit=5))

    print("\n✅ Connexion Reddit réussie !")
    print("   Subreddit: r/france")
    print(f"   Posts récupérés: {len(posts)}")
    print("\n📄 Aperçu (3 premiers) :")

    for idx, post in enumerate(posts[:3], 1):
        print(f"\n   {idx}. {post.title}")
        print(f"      Score: {post.score} | Commentaires: {post.num_comments}")

    print("\n🎉 Reddit API 100% opérationnel !")

except ImportError:
    print("❌ PRAW non installé : pip install praw")
except Exception as e:
    print(f"❌ Erreur : {e!s}")
