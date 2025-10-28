# 📊 WEB SCRAPING MULTI-SOURCES - Documentation Détaillée

## 🎯 **Vue d'ensemble**

Le système collecte des données citoyennes depuis **5 sources diversifiées** pour maximiser la couverture du sentiment public français.

---

## 📱 **SOURCE 1 : Reddit France (API PRAW)**

### **Configuration requise** :
```properties
REDDIT_CLIENT_ID=ABC123def456ghi
REDDIT_CLIENT_SECRET=xyz789abc123def456ghi789
```

### **Comment obtenir** :
1. Créer compte sur https://www.reddit.com
2. Créer app sur https://www.reddit.com/prefs/apps (type: script)
3. Copier Client ID (14 caractères) + Secret (27 caractères)
4. Voir `REDDIT_API_SETUP.md` pour guide détaillé

### **Données collectées** :
- **Subreddits** : r/france, r/French, r/AskFrance
- **Méthode** : Hot posts (tri par popularité)
- **Volume** : 150 posts (50 par subreddit)
- **Champs** :
  - `titre` : Titre du post
  - `texte` : Contenu (selftext)
  - `source_site` : reddit.com/r/{subreddit}
  - `url` : Lien permanent
  - `score` : Upvotes - Downvotes
  - `date_publication` : Timestamp création

### **Avantages** :
- ✅ **API officielle** (100% légal)
- ✅ **60 requêtes/minute** (pas de quota journalier)
- ✅ **Sentiment authentique** (discussions citoyennes brutes)
- ✅ **Français natif** (pas de traduction)
- ✅ **Score popularité** (upvotes = indicateur engagement)

### **Code technique** :
```python
import praw

reddit = praw.Reddit(
    client_id=REDDIT_CLIENT_ID,
    client_secret=REDDIT_CLIENT_SECRET,
    user_agent="datasens/1.0 (educational project)"
)

for post in reddit.subreddit("france").hot(limit=50):
    data = {
        "titre": post.title,
        "texte": post.selftext,
        "score": post.score,
        "date_publication": pd.to_datetime(post.created_utc, unit='s')
    }
```

---

## 📺 **SOURCE 2 : YouTube Comments (API Google)**

### **Configuration requise** :
```properties
YOUTUBE_API_KEY=AIzaSyCvLuuu3Z3Ex35FfxKjrRjcgs2_d3UFCWM  # DÉJÀ CONFIGURÉ ✅
```

### **Données collectées** :
- **Chaînes** : France 24, LCI
- **Vidéos** : 3 plus récentes par chaîne
- **Volume** : ~300 commentaires (50 par vidéo)
- **Champs** :
  - `titre` : Extrait commentaire (100 premiers chars)
  - `texte` : Commentaire complet
  - `source_site` : youtube.com/{chaîne}
  - `url` : Lien vidéo
  - `score` : Nombre de likes
  - `date_publication` : Timestamp publication

### **Avantages** :
- ✅ **Déjà configuré** (vous avez la clé !)
- ✅ **Réactions temps réel** (actualités chaudes)
- ✅ **Sentiment fort** (opinions tranchées)
- ✅ **Quota généreux** (10,000 unités/jour)

### **Code technique** :
```python
from googleapiclient.discovery import build

youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

# Récupérer vidéos récentes
search_response = youtube.search().list(
    part="id",
    channelId="UCCCPCZNChQdGa9EkATeye4g",  # France 24
    maxResults=3,
    order="date"
).execute()

# Récupérer commentaires
comments_response = youtube.commentThreads().list(
    part="snippet",
    videoId=video_id,
    maxResults=50
).execute()
```

---

## 🇫🇷 **SOURCE 3 : SignalConso (Open Data Gouvernemental)**

### **Configuration requise** :
```properties
# AUCUNE ! API publique ouverte ✅
```

### **Données collectées** :
- **Source** : https://signal.conso.gouv.fr
- **Type** : Signalements consommateurs officiels
- **Volume** : 500 signalements
- **Champs** :
  - `titre` : Catégorie du signalement
  - `texte` : Description détaillée
  - `source_site` : signal.conso.gouv.fr
  - `date_publication` : Date création

### **Avantages** :
- ✅ **Données gouvernementales** (fiabilité maximale)
- ✅ **Aucune API key** (accès libre)
- ✅ **Signalements vérifiés** (qualité contrôlée)
- ✅ **RGPD compliant** (déjà anonymisé)
- ✅ **Sentiment citoyen officiel** (plaintes réelles)

### **Code technique** :
```python
signal_url = "https://signal.conso.gouv.fr/api/reports"
params = {"limit": 500, "offset": 0}

r = requests.get(signal_url, params=params, timeout=15)
reports = r.json()

for report in reports:
    data = {
        "titre": report.get("category"),
        "texte": report.get("description"),
        "date_publication": pd.to_datetime(report.get("creationDate"))
    }
```

---

## ⭐ **SOURCE 4 : Trustpilot France (Web Scraping)**

### **Configuration requise** :
```properties
# AUCUNE ! Scraping modéré avec respect robots.txt
```

### **Données collectées** :
- **URL** : https://fr.trustpilot.com/categories/public_local_services
- **Type** : Avis sur services publics
- **Volume** : ~100 avis
- **Champs** :
  - `titre` : Titre de l'avis
  - `texte` : Contenu complet
  - `source_site` : trustpilot.com

### **Avantages** :
- ✅ **Notes + texte** (double signal)
- ✅ **Avis vérifiés** (authentification Trustpilot)
- ✅ **Respect robots.txt** (vérifié avant scraping)
- ✅ **Rate limiting** (2 sec entre requêtes)

### **Code technique** :
```python
from bs4 import BeautifulSoup

# Vérifier robots.txt
robots_r = requests.get("https://fr.trustpilot.com/robots.txt")
if "Disallow: /categories" not in robots_r.text:
    
    r = requests.get(trust_url, headers={
        "User-Agent": "DataSensBot/1.0 (educational)"
    })
    
    soup = BeautifulSoup(r.text, "html.parser")
    reviews = soup.select(".review-card")
    
    for review in reviews:
        text_el = review.select_one(".review-content__text")
        data = {"texte": text_el.get_text(strip=True)}
```

---

## 🧪 **SOURCE 5 : MonAvisCitoyen (Dry-run Test)**

### **Configuration requise** :
```properties
# AUCUNE ! Test simulé
```

### **Données collectées** :
- **Volume** : 0 (simulation)
- **Usage** : Validation code scraping

### **Avantages** :
- ✅ **Aucun risque** (pas de requêtes réelles)
- ✅ **Démo technique** (robots.txt check, rate limiting)
- ✅ **Fallback** (si autres sources échouent)

---

## 📊 **VOLUMÉTRIE ATTENDUE**

| Source | Documents | Type |
|--------|-----------|------|
| Reddit France | 150 | Posts discussions |
| YouTube | 300 | Commentaires vidéos |
| SignalConso | 500 | Signalements officiels |
| Trustpilot | 100 | Avis services publics |
| MonAvisCitoyen | 0 | Test (dry-run) |
| **TOTAL** | **~1050** | Documents citoyens |

**Note** : Volume peut varier selon disponibilité APIs et contenu du jour.

---

## 🔒 **SÉCURITÉ & CONFORMITÉ**

### **RGPD** :
- ✅ Anonymisation automatique (pas de données personnelles stockées)
- ✅ Sources publiques uniquement
- ✅ Respect ToS de chaque plateforme

### **Rate Limiting** :
```python
# Reddit : 60 req/min (géré par PRAW)
time.sleep(2)  # Entre subreddits

# YouTube : 10,000 unités/jour
time.sleep(1)  # Entre vidéos

# Trustpilot : Custom
time.sleep(2)  # Entre pages
```

### **robots.txt** :
- ✅ Vérification systématique avant scraping
- ✅ Respect des Disallow
- ✅ User-Agent identifiable

---

## 🚀 **INSTRUCTIONS D'EXÉCUTION**

### **Prérequis** :
1. ✅ Installer dépendances : `pip install praw google-api-python-client`
2. ✅ Configurer Reddit API (voir `REDDIT_API_SETUP.md`)
3. ✅ YouTube API déjà configurée

### **Exécution** :
1. Ouvrir `notebooks/datasens_E1_v2.ipynb`
2. Exécuter cellule 18 (Web Scraping Multi-Sources)
3. Durée : ~2-3 minutes
4. Résultat : ~1050 documents en PostgreSQL + MinIO

### **Optionnel** :
- Reddit peut être skippé (autres sources fonctionneront)
- Si erreur : vérifier credentials `.env`
- Logs détaillés affichés pour chaque source

---

## 📈 **AMÉLIORATIONS FUTURES (E2/E3)**

- [ ] Ajouter Twitter/X via nitter
- [ ] Commentaires Facebook Pages publiques
- [ ] Forums jeuxvideo.com, Dealabs
- [ ] Scraping asynchrone (asyncio)
- [ ] Détection langue automatique
- [ ] Sentiment analysis en temps réel

---

**Questions ?** Consultez `REDDIT_API_SETUP.md` pour Reddit ou demandez de l'aide ! 🤝
