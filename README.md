# 🎯 DataSens - Projet E1 : Collecte Multi-Sources & DataLake

[![GitHub release](https://img.shields.io/github/v/release/ALMAGNUS/DataSens_Project)](https://github.com/ALMAGNUS/DataSens_Project/releases)
[![GitHub stars](https://img.shields.io/github/stars/ALMAGNUS/DataSens_Project)](https://github.com/ALMAGNUS/DataSens_Project/stargazers)
[![GitHub issues](https://img.shields.io/github/issues/ALMAGNUS/DataSens_Project)](https://github.com/ALMAGNUS/DataSens_Project/issues)
[![Code size](https://img.shields.io/github/languages/code-size/ALMAGNUS/DataSens_Project)](https://github.com/ALMAGNUS/DataSens_Project)

> **Projet académique** - Architecture Big Data avec gouvernance des données

## 📊 Vue d'ensemble

DataSens est une plateforme de collecte, stockage et analyse de données hétérogènes respectant les **5 types de sources exigées** pour le projet, avec traçabilité complète via un modèle Merise et infrastructure Big Data.

### 🎓 Objectifs pédagogiques - 5 Sources
1. ✅ **Fichier plat** : Kaggle CSV 50% stocké sur MinIO
2. ✅ **Base de données** : Kaggle 50% inséré dans PostgreSQL
3. ✅ **Web Scraping** : 6 sources citoyennes (Reddit, YouTube, SignalConso, Trustpilot, vie-publique.fr, data.gouv.fr)
4. ✅ **API** : 3 APIs (OpenWeatherMap, NewsAPI, RSS Multi-sources)
5. ✅ **Big Data** : GDELT GKG France (300 MB → filtrage France)

**Compétences démontrées :**
- Architecture DataLake (MinIO) + SGBD (PostgreSQL)
- Gouvernance des données (traçabilité, dédoublonnage, RGPD)
- Orchestration Docker & CI/CD
- Notebooks reproductibles
- Respect des règles d'éthique et légalité web scraping

---

## 🏗️ Architecture

```
┌─────────────────────────────────────────────────────────────┐
│              5 TYPES DE SOURCES (Exigence Projet)            │
├─────────────────────────────────────────────────────────────┤
│  1. FICHIER PLAT     → Kaggle 50% CSV (MinIO)              │
│  2. BASE DE DONNÉES  → Kaggle 50% PostgreSQL (30k tweets)   │
│  3. WEB SCRAPING     → 6 sources citoyennes légales         │
│  4. API              → 3 APIs (OWM, NewsAPI, RSS)           │
│  5. BIG DATA         → GDELT France (GKG filtré)            │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────────┐
│                  COUCHE INGESTION (E1)                       │
├─────────────────────────────────────────────────────────────┤
│  • Collecte automatisée                                      │
│  • Dédoublonnage (hash fingerprint)                         │
│  • Validation qualité                                        │
│  • Manifest de traçabilité                                   │
└─────────────────────────────────────────────────────────────┘
                            ↓
┌────────────────────┬────────────────────────────────────────┐
│   DataLake (MinIO) │   SGBD PostgreSQL (Merise)            │
├────────────────────┼────────────────────────────────────────┤
│ • Bruts 50% Kaggle │ • 18 tables relationnelles             │
│ • Tous les flux    │ • Type_donnee → Source → Flux → Doc   │
│ • Fichiers CSV/JSON│ • Territoire, Météo, Indicateurs      │
│ • Versioning       │ • Thèmes, Événements, Annotations     │
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
```bash
# Le fichier .env est déjà configuré avec les valeurs par défaut
# Éditer les API keys si nécessaire : OWM_API_KEY, YOUTUBE_API_KEY, etc.
```

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

Exécuter les cellules dans l'ordre (1-27)

---

## 📁 Structure du projet

```
datasens-project/
├── � notebooks/                    # Notebooks Jupyter
│   ├── datasens_E1_v2.ipynb         # Version production (MinIO+PG)
│   └── datasens_E1_v1.ipynb         # Version démo (SQLite)
│
├── 🐳 docker-compose.yml            # Infrastructure Docker
├── 📋 requirements.txt              # Dépendances Python
├── 🔐 .env                          # Configuration (secrets)
├── � .env.example                  # Template configuration
├── 🚫 .gitignore                    # Exclusions Git
│
├── 📂 data/                         # Données collectées
│   ├── raw/                         # Bruts (Kaggle, RSS, GDELT...)
│   │   ├── kaggle/                  # 60k tweets
│   │   ├── api/owm/                 # Météo 4 villes
│   │   ├── api/newsapi/             # 200 articles
│   │   ├── rss/                     # 77 articles multi-sources
│   │   ├── scraping/multi/          # Web scraping consolidé
│   │   ├── scraping/viepublique/    # Consultations citoyennes
│   │   ├── scraping/datagouv/       # Budget participatif
│   │   ├── gdelt/                   # Big Data GKG France
│   │   └── manifests/               # Traçabilité
│   ├── silver/                      # Nettoyés (E2)
│   └── gold/                        # Agrégés (E2)
│
├── 📂 docs/                         # Documentation
│   ├── README.md                    # Cette documentation
│   ├── DEPLOIEMENT_GITHUB.md        # Guide CI/CD
│   ├── REDDIT_API_SETUP.md          # Config Reddit API
│   └── WEB_SCRAPING_GUIDE.md        # Éthique scraping
│
├── 📂 datasens/                     # Métadonnées
│   └── versions/                    # Snapshots PostgreSQL
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
- **Reddit France** (API PRAW) : ~150 posts
- **YouTube Comments** (API) : ~300 commentaires texte
- **SignalConso** (Open Data gouv.fr) : ~500 signalements
- **Trustpilot FR** : ~100 avis
- **Vie-publique.fr** : ~50 consultations citoyennes
- **data.gouv.fr** : ~100 Budget Participatif
- **Total** : ~1,200 documents

#### 4️⃣ API (3 APIs officielles)
- **OpenWeatherMap** : 4 relevés météo (Paris, Lyon, Marseille, Lille)
- **NewsAPI** : ~200 articles (4 catégories FR)
- **RSS Multi-sources** : ~77 articles (Franceinfo + 20 Minutes + Le Monde)
- **Total** : ~280 documents

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
