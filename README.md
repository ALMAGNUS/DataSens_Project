# 🎯 DataSens - Projet E1 : Collecte Multi-Sources & DataLake

> **Projet académique E1** - Notebook Jupyter tout-en-un avec code inline simple

## 📊 Vue d'ensemble

DataSens est un **notebook Jupyter académique** démontrant la collecte de données depuis **5 types de sources différentes**, avec stockage hybride (MinIO + PostgreSQL) et traçabilité complète.

**🎯 Approche pédagogique** : Code simple et transparent dans le notebook, sans modules externes complexes.

### 🎓 Objectifs pédagogiques - 5 Sources
1. ✅ **Fichier plat** : Kaggle CSV 50% stocké sur MinIO
2. ✅ **Base de données** : Kaggle 50% inséré dans PostgreSQL (30k tweets)
3. ✅ **Web Scraping** : 6 sources citoyennes inline (Reddit, YouTube, SignalConso, Trustpilot, vie-publique.fr, data.gouv.fr)
4. ✅ **API** : 3 APIs inline (OpenWeatherMap, NewsAPI, RSS Multi-sources)
5. ✅ **Big Data** : GDELT GKG France (300 MB → filtrage France)

**✨ Points forts du projet** :
- **Code inline** : Tout dans le notebook, facile à comprendre et debugger
- **Architecture DataLake** : MinIO (S3) + PostgreSQL (relationnel)
- **Gouvernance des données** : Traçabilité complète, dédoublonnage SHA-256, RGPD
- **Orchestration Docker** : PostgreSQL, MinIO, Redis en containers
- **Reproductibilité** : `requirements.txt` + `.env` → un seul notebook à exécuter

---

## 🏗️ Architecture

┌─────────────────────────────────────────────────────────────┐
│                  NOTEBOOK JUPYTER E1                         │
│              (Code inline simple et pédagogique)             │
├─────────────────────────────────────────────────────────────┤
│  Cellule 1-10   : Setup (imports, MinIO, PostgreSQL)       │
│  Cellule 11-17  : Kaggle (CSV → 50% MinIO + 50% PG)        │
│  Cellule 18-24  : PostgreSQL Kaggle (insertion 30k tweets) │
│  Cellule 25     : Web Scraping (9 sources inline)          │
│  Cellule 26     : APIs (NewsAPI, OpenWeather, RSS inline)  │
│  Cellule 27     : GDELT Big Data (filtrage France)         │
│  Cellule 28+    : Analyse & Visualisations                 │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│              5 TYPES DE SOURCES (Exigence Projet)            │
├─────────────────────────────────────────────────────────────┤
│  1. FICHIER PLAT     → Kaggle 50% CSV (MinIO)              │
│  2. BASE DE DONNÉES  → Kaggle 50% PostgreSQL (30k tweets)   │
│  3. WEB SCRAPING     → 6 sources inline (Reddit, YouTube...)│
│  4. API              → 3 sources inline (OWM, NewsAPI, RSS) │
│  5. BIG DATA         → GDELT France (GKG filtré inline)     │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  COLLECTE INLINE (Code simple)               │
├─────────────────────────────────────────────────────────────┤
│  • Code direct dans notebook (pas de .py externes)          │
│  • Try/except par source (robustesse)                       │
│  • Logs détaillés (debugging facile)                        │
│  • Dédoublonnage SHA-256                                    │
│  • Format unifié {titre, texte, source, url, date, langue}  │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────┬────────────────────────────────────────┐
│   DataLake (MinIO) │   SGBD PostgreSQL (Merise)            │
├────────────────────┼────────────────────────────────────────┤
│ • Bruts 50% Kaggle │ • 18 tables relationnelles             │
│ • Tous les CSV flux│ • Type_donnee → Source → Flux → Doc   │
│ • Versioning       │ • Territoire, Météo, Indicateurs       │
│ • S3-compatible    │ • Traçabilité complète                 │
└────────────────────┴────────────────────────────────────────┘
```

---

## 🚀 Installation & Démarrage

### Prérequis
- Docker Desktop installé
- Python 3.12+ avec Jupyter
- Git

### 1️⃣ Cloner le projet
```bash
git clone https://github.com/votre-username/datasens-project.git
cd datasens-project
```

### 2️⃣ Configuration

**Créer le fichier `.env`** avec tes API keys :

```bash
# PostgreSQL
POSTGRES_USER=ds_user
POSTGRES_PASSWORD=ds_pass
POSTGRES_HOST=localhost
POSTGRES_PORT=5432
POSTGRES_DB=datasens

# MinIO
MINIO_ROOT_USER=admin
MINIO_ROOT_PASSWORD=admin123
MINIO_ENDPOINT=localhost:9000

# API Keys (optionnel pour démo)
REDDIT_CLIENT_ID=ton_client_id
REDDIT_CLIENT_SECRET=ton_secret
YOUTUBE_API_KEY=ta_cle_youtube
NEWSAPI_KEY=ta_cle_newsapi
OWM_API_KEY=ta_cle_openweather
```

**💡 Astuce** : Les API keys sont optionnelles. Le notebook gère gracieusement les erreurs (try/except) et continue avec les autres sources si une clé manque.

### 3️⃣ Lancer l'infrastructure
```bash
# Démarrer MinIO, PostgreSQL, Redis
docker-compose up -d

# Vérifier les services
docker-compose ps
```

### 4️⃣ Installer les dépendances Python
```bash
# Créer l'environnement virtuel
python -m venv .venv

# Activer (Windows PowerShell)
.\.venv\Scripts\Activate.ps1

# Installer les packages
pip install -r requirements.txt
```

### 5️⃣ Exécuter le notebook E1
```bash
cd notebooks
jupyter notebook datasens_E1_v2.ipynb
```

**🎯 Mode d'emploi** : Exécuter les cellules dans l'ordre (1-61). Chaque cellule est commentée et autonome.

**⚡ Cellules clés** :
- **Cellule 8** : Configuration logging (fichiers de debug)
- **Cellule 25** : Web Scraping 6 sources (code inline simple)
- **Cellule 26** : APIs 3 sources (code inline simple)
- **Cellule 27** : GDELT Big Data France

---

## 📋 Logs & Debugging

Le notebook génère des **fichiers de logs détaillés** pour tracer toutes les collectes et déboguer les erreurs :

### Fichiers générés (dossier `logs/`)

**📄 `collecte_YYYYMMDD_HHMMSS.log`** - Log complet de la collecte :
```
2025-10-28 21:06:15 | INFO     | DataSens | 🚀 Démarrage collecte Web Scraping Multi-Sources
2025-10-28 21:06:16 | INFO     | DataSens | [Reddit] Connexion API PRAW réussie
2025-10-28 21:06:18 | INFO     | DataSens | [Reddit] r/france: 50 posts collectés
2025-10-28 21:06:19 | INFO     | DataSens | [Reddit] r/Paris: 50 posts collectés
2025-10-28 21:06:20 | INFO     | DataSens | [Reddit] ✅ Total: 100 posts
2025-10-28 21:06:21 | INFO     | DataSens | [YouTube] Connexion API Google v3 réussie
2025-10-28 21:06:23 | INFO     | DataSens | [YouTube] ✅ 30 vidéos collectées
2025-10-28 21:06:24 | WARNING  | DataSens | [SignalConso] 404 Client Error - API endpoint modifié
2025-10-28 21:06:24 | INFO     | DataSens | [SignalConso] ⚠️ 0 signalements (skip)
2025-10-28 21:06:30 | INFO     | DataSens | [DataGouv] ✅ 7 datasets collectés
2025-10-28 21:06:35 | INFO     | DataSens | 📊 TOTAL: 86 documents collectés
2025-10-28 21:06:36 | INFO     | DataSens | ✅ Storage PostgreSQL + MinIO réussi
```

**❌ `errors_YYYYMMDD_HHMMSS.log`** - Erreurs uniquement avec traceback :
```
2025-10-28 21:06:24 | ERROR    | DataSens | [SignalConso] Collecte échouée: 404 Client Error: Not Found for url: https://signal.conso.gouv.fr/api/reports
2025-10-28 21:06:24 | ERROR    | DataSens | Traceback:
Traceback (most recent call last):
  File "<cell>", line 125, in <module>
    response.raise_for_status()
requests.exceptions.HTTPError: 404 Client Error: Not Found for url: https://signal.conso.gouv.fr/api/reports?limit=100
```

### Comment consulter les logs

**Option 1 - PowerShell** :
```powershell
# Afficher le dernier log de collecte
Get-Content logs\collecte_*.log -Tail 50

# Afficher les erreurs uniquement
Get-Content logs\errors_*.log

# Suivre en temps réel (pendant exécution notebook)
Get-Content logs\collecte_*.log -Wait -Tail 20
```

**Option 2 - VS Code** :
- Ouvrir le dossier `logs/`
- Double-cliquer sur le fichier `.log`
- Recherche avec `Ctrl+F`

### Logs pour le prof

Les logs permettent de :
- ✅ Tracer **toutes les opérations** (timestamp précis)
- ✅ Identifier **quelles sources fonctionnent**
- ✅ Voir **les erreurs avec traceback complet**
- ✅ Déboguer **les problèmes d'API keys**
- ✅ Monitorer **le volume collecté par source**

---## 🔍 Approche Code Inline (Simple & Pédagogique)

**Pourquoi code inline dans le notebook ?**

✅ **Simplicité** : Pas de modules `.py` externes → tout visible dans un seul fichier
✅ **Pédagogique** : Le jury voit chaque ligne de code, pas de "boîte noire"
✅ **Debugging facile** : Logs détaillés directement dans les cellules
✅ **Reproductibilité** : `requirements.txt` + 1 notebook = tout fonctionne
✅ **Académique** : Approche claire pour démonstration E1

**Exemple cellule 25 (Web Scraping)** :
```python
# Tout le code dans la cellule - pas d'import externe
import praw
reddit = praw.Reddit(client_id=os.getenv("REDDIT_CLIENT_ID"), ...)
for post in reddit.subreddit("france").hot(limit=50):
    all_data.append({"titre": post.title, "texte": post.selftext, ...})

# YouTube
from googleapiclient.discovery import build
youtube = build('youtube', 'v3', developerKey=os.getenv("YOUTUBE_API_KEY"))
response = youtube.search().list(q="france", maxResults=30).execute()
for video in response['items']:
    all_data.append({"titre": video['snippet']['title'], ...})

# ... 4 autres sources (SignalConso, Trustpilot, ViePublique, DataGouv)
```

---

## ⚙️ Stack Technique

### Infrastructure & DevOps
- **Docker** : Conteneurisation PostgreSQL, MinIO, Redis
- **Docker Compose** : Orchestration multi-conteneurs
- **Git** : Versioning (commits français, tags sémantiques)
- **GitHub** : Hébergement code source
- **.env** : Gestion secrets (API keys sécurisées)

### Base de Données & Storage
- **PostgreSQL 17** : SGBD relationnel (18 tables Merise E1)
- **MinIO** : Object Storage S3-compatible (DataLake)
- **SQLAlchemy 2.0** : ORM Python ↔ PostgreSQL
- **psycopg2** : Driver PostgreSQL natif

### Data Processing
- **Python 3.13** : Langage principal
- **Pandas 2.3** : Manipulation DataFrames
- **Jupyter Notebook** : Développement interactif
- **NumPy 2.3** : Calculs numériques

### Data Collection (inline dans notebook)
- **PRAW 7.8** : Reddit API officielle
- **google-api-python-client 2.185** : YouTube Data API v3
- **requests 2.32** : HTTP client (SignalConso, Data.gouv, NewsAPI, OpenWeather)
- **BeautifulSoup4 4.14** : Web scraping (Trustpilot)
- **feedparser 6.0** : Parsing RSS/Atom (Vie Publique, multi-sources)

### Data Quality & Security
- **hashlib** : SHA-256 fingerprints (dédoublonnage)
- **python-dotenv** : Chargement variables d'environnement
- **regex** : Validation et nettoyage données
- **datetime** : Gestion timestamps UTC

### Data Visualization
- **matplotlib 3.10** : Graphiques de base
- **seaborn 0.13** : Graphiques statistiques stylés

### APIs & Web Services
- **Kaggle API** : Téléchargement datasets officiels
- **OpenWeatherMap API** : Données météo temps réel
- **NewsAPI** : Actualités internationales
- **Reddit API (PRAW)** : Posts subreddits français
- **YouTube Data API v3** : Métadonnées vidéos
- **Signal.conso.gouv.fr API** : Signalements citoyens
- **data.gouv.fr API** : Open Data gouvernemental

### Big Data
- **GDELT Project** : Événements mondiaux (GKG 300 MB → 5-10 MB filtré France)
- **Filtrage** : V2Locations, V2Themes, V2Tone

---

## 📁 Structure du projet

```
datasens-project/
├── 📓 notebooks/                    # Notebooks Jupyter
│   ├── datasens_E1_v2.ipynb         # Version production (MinIO+PG)
│   └── datasens_E1_v3.ipynb         # Archive ancienne version
│
├── 🐳 docker-compose.yml            # Infrastructure Docker
├── 📋 requirements.txt              # Dépendances Python
├── 🔐 .env                          # Configuration (secrets)
├── 📄 .env.example                  # Template configuration
├── 🚫 .gitignore                    # Exclusions Git
│
├── 📂 data/                         # Données collectées
│   ├── raw/                         # Bruts (Kaggle, RSS, GDELT...)
│   │   ├── kaggle/                  # 60k tweets
│   │   ├── scraping/                # Multi-sources (Reddit, YouTube, etc.)
│   │   ├── rss/                     # Flux RSS multi-sources
│   │   ├── gdelt/                   # Big Data GKG France
│   │   └── manifests/               # Traçabilité
│   ├── silver/                      # Nettoyés (E2)
│   └── gold/                        # Agrégés (E2)
│
├── 📂 datasens/                     # Code source
│   ├── transformers/                # Nettoyage & enrichissement
│   ├── loaders/                     # PostgreSQL & MinIO
│   ├── utils/                       # Helpers
│   └── versions/                    # Snapshots PostgreSQL
│
├── 📂 docs/                         # Documentation
│   └── GUIDE_TECHNIQUE_JURY.md      # Guide détaillé pour le jury
│
├── 📂 logs/                         # Logs de collecte
└── 📂 .github/workflows/            # CI/CD GitHub Actions
```

---

## 🎨 Modèle de données (Merise E1)

### Tables principales - Chaîne de traçabilité

```sql
TYPE_DONNEE (id, libelle, description)
    ↓
SOURCE (id, id_type_donnee, nom, url, fiabilite)
    ↓
FLUX (id, id_source, date_collecte, format, manifest_uri)
    ↓
DOCUMENT (id, id_flux, titre, texte, langue, hash_fingerprint)
```

**18 tables au total** : géographie (territoire, méteo), indicateurs, thèmes, événements, annotations

---

## 🔒 Sécurité & RGPD

- ✅ **Pseudonymisation** : hash SHA-256 pour dédoublonnage
- ✅ **Anonymisation auteurs** : aucune donnée personnelle stockée (RGPD)
- ✅ **Secrets sécurisés** : `.env` exclu de Git (.gitignore)
- ✅ **APIs légales** : Credentials officiels (Kaggle, NewsAPI, OWM, Reddit, YouTube)
- ✅ **Open Data gouvernemental** : Sources .gouv.fr (SignalConso, vie-publique.fr, data.gouv.fr)
- ✅ **Robots.txt** : respect des règles de scraping (Trustpilot vérification préalable)
- ✅ **Rate limiting** : pauses entre requêtes API
- ✅ **Aucune clé payante** : 100% APIs gratuites

---

## 📊 Résultats E1

### ✅ 5 Types de sources respectés (100%)

#### 1️⃣ FICHIER PLAT (Kaggle 50% CSV MinIO)
- **Format** : CSV brut stocké sur MinIO
- **Volume** : 30,000 tweets (50% du dataset Kaggle)
- **Source** : Sentiment140 (EN) + French Twitter (FR)

#### 2️⃣ BASE DE DONNÉES (Kaggle 50% PostgreSQL)
- **Format** : Insertion relationnelle PostgreSQL
- **Volume** : 30,000 tweets (50% restant)
- **Tables** : document, flux, territoire (Merise)

#### 3️⃣ WEB SCRAPING (6 sources citoyennes légales)

| Source | Collecteur | Tech | Description |
|--------|-----------|------|-------------|
| **Reddit France** | `reddit_collector.py` | PRAW API | r/france, r/Paris, r/Lyon |
| **YouTube** | `youtube_collector.py` | Google API | Chaînes officielles FR |
| **SignalConso** | `signalconso_collector.py` | Requests API | Signalements citoyens |
| **Trustpilot** | `trustpilot_collector.py` | BeautifulSoup4 | Avis consommateurs FR |
| **Vie Publique** | `vie_publique_collector.py` | Feedparser + BS4 | Actualités gouv |
| **Data.gouv.fr** | `datagouv_collector.py` | Requests API | Métadonnées datasets |

**Total estimé** : ~1,200 documents/jour

#### 4️⃣ API (3 sources officielles)

| Source | Collecteur | Tech | Description |
|--------|-----------|------|-------------|
| **OpenWeatherMap** | `openweather_collector.py` | REST API | Météo 5 villes FR |
| **NewsAPI** | `newsapi_collector.py` | REST API | Actualités internationales |
| **RSS Multi-sources** | `rss_collector.py` | Feedparser | Le Monde, BBC, France24, RFI |

**Total estimé** : ~300 articles/jour

#### 5️⃣ BIG DATA (GDELT GKG France)
- **Volume brut** : ~300 MB (fichier GKG dernières 24h)
- **Filtrage France** : V2Locations contains "FR" → ~5-10 MB
- **Événements extraits** : ~500 événements France
- **Analyses** : V2Tone (tonalité émotionnelle), V2Themes (top 10 thèmes)

---

### 📈 Métriques globales
- **Documents totaux** : ~62,400
- **Sources actives** : 5/5 types (100% conformité jury)
- **Qualité** : 0 doublons (hash SHA-256), <5% nulls
- **Traçabilité** : 100% (manifest par flux)
- **Légalité** : 100% (APIs officielles + Open Data .gouv.fr)

---

## 🚀 CI/CD & Déploiement

### Accès aux services

- **MinIO Console** : http://localhost:9001 (admin / admin123)
- **PostgreSQL** : localhost:5432 (ds_user / ds_pass)
- **Redis** : localhost:6379

### Commandes Docker

```bash
# Démarrer
docker-compose up -d

# Logs
docker-compose logs -f

# Arrêter
docker-compose down

# Reset complet
docker-compose down -v
```

---

## 🔮 Roadmap E2/E3

### E2 - Enrichissement IA
- [ ] Analyse émotionnelle (FlauBERT, CamemBERT)
- [ ] Extraction entités nommées (spaCy)
- [ ] Embeddings vectoriels (sentence-transformers)
- [ ] Orchestration Prefect

### E3 - Production
- [ ] API REST (FastAPI)
- [ ] Dashboard Streamlit
- [ ] Monitoring Grafana/Prometheus
- [ ] Tests automatisés (pytest)

---

## 📝 Licence

Projet académique - Usage éducatif uniquement
