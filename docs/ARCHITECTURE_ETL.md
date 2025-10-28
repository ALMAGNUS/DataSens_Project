# 🔄 PIPELINE ETL DATASENS - Architecture Complète

## ✅ Oui, votre architecture est un ETL classique !

```
┌─────────────────────────────────────────────────────────────────────┐
│                        🔵 EXTRACT (E)                               │
│                    Collecte Multi-Sources                            │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  📁 SOURCE 1 : Fichier Plat                                         │
│  ├─ Kaggle CSV (Sentiment140)           → 24,683 documents          │
│  └─ Événements Historiques CSV (1995-2025) → 37 événements          │
│                                                                      │
│  🗄️ SOURCE 2 : Base de Données                                      │
│  └─ Kaggle CSV → PostgreSQL (50%)       → 24,683 documents          │
│                                                                      │
│  🌐 SOURCE 3 : Web Scraping                                          │
│  ├─ Reddit (r/france)                    → ~50 posts                │
│  ├─ YouTube Comments                     → ~50 comments             │
│  ├─ SignalConso                          → ~50 signalements         │
│  ├─ Trustpilot                           → ~50 avis                 │
│  ├─ Vie-publique.fr                      → ~30 consultations        │
│  └─ data.gouv.fr                         → ~35 datasets             │
│                                          TOTAL: 265 documents        │
│                                                                      │
│  🔌 SOURCE 4 : API                                                   │
│  ├─ RSS Multi-Sources (3 flux)           → 99 articles              │
│  │   • Franceinfo                                                    │
│  │   • 20 Minutes                                                    │
│  │   • Le Monde                                                      │
│  └─ OpenWeatherMap (4 villes)           → 8 relevés météo           │
│                                                                      │
│  💾 SOURCE 5 : Big Data                                              │
│  └─ GDELT GKG France (agrégé)           → 57 événements             │
│                                                                      │
│  📜 SOURCE BONUS : Données Historiques                               │
│  └─ Événements France (CSV)              → 37 événements            │
│      • 8 attentats (2012-2020)                                       │
│      • 5 grèves nationales (1995-2023)                               │
│      • 4 catastrophes naturelles (1999-2022)                         │
│      • 11 changements politiques (2007-2024)                         │
│      • 3 crises économiques (2008-2022)                              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                             ⬇️ FLUX DE DONNÉES
┌─────────────────────────────────────────────────────────────────────┐
│                        🟡 TRANSFORM (T)                             │
│                    Nettoyage & Enrichissement                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  🔍 1. VALIDATION                                                    │
│  ├─ Vérification format (CSV, JSON, XML, HTML)                      │
│  ├─ Gestion erreurs HTTP (403, 404, 500...)                         │
│  └─ Détection encoding (UTF-8, Latin-1, CP1252)                     │
│                                                                      │
│  🧹 2. NETTOYAGE                                                     │
│  ├─ Suppression HTML tags (BeautifulSoup)                           │
│  ├─ Normalisation espaces/newlines                                  │
│  ├─ Troncature texte (200 caractères titre, illimité texte)         │
│  └─ Gestion valeurs NULL (remplacement par défauts)                 │
│                                                                      │
│  🔐 3. DÉDUPLICATION                                                 │
│  ├─ Hash SHA256 sur le texte complet                                │
│  ├─ Stockage dans hash_fingerprint (UNIQUE)                         │
│  └─ INSERT ... ON CONFLICT DO NOTHING (PostgreSQL UPSERT)           │
│                                                                      │
│  📅 4. NORMALISATION TEMPORELLE                                      │
│  ├─ Conversion dates → datetime Python                              │
│  ├─ Format ISO 8601 (YYYY-MM-DD HH:MM:SS)                           │
│  └─ Timezone UTC pour cohérence                                     │
│                                                                      │
│  🌍 5. ENRICHISSEMENT GÉOGRAPHIQUE                                   │
│  ├─ Détection langue (fr, en, auto)                                 │
│  ├─ GDELT : Filtrage France (#FR# dans V2Locations)                 │
│  └─ OWM : Géolocalisation villes (Paris, Lyon, Marseille, Lille)    │
│                                                                      │
│  📊 6. EXTRACTION MÉTADONNÉES                                        │
│  ├─ GDELT : Tonalité émotionnelle (V2Tone: -100 à +100)             │
│  ├─ GDELT : Thèmes (PROTEST, HEALTH, ECONOMY...)                    │
│  ├─ RSS : Catégorie source (presse, institutions)                   │
│  └─ Événements : Type (attentat, grève, catastrophe...)             │
│                                                                      │
│  🔄 7. AGRÉGATION                                                    │
│  ├─ Fusion 3 flux RSS → source unique "RSS Multi-Sources"           │
│  ├─ Fusion 6 sites Web Scraping → source unique                     │
│  └─ GDELT : 10 fichiers 15min → batch agrégé France                 │
│                                                                      │
│  🛡️ 8. RGPD & SÉCURITÉ                                              │
│  ├─ Pseudonymisation noms propres (non implémenté MVP)              │
│  ├─ Anonymisation emails/téléphones (non implémenté MVP)            │
│  └─ Droit à l'oubli via DELETE CASCADE (schéma Merise)              │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
                             ⬇️ DONNÉES PROPRES
┌─────────────────────────────────────────────────────────────────────┐
│                        🟢 LOAD (L)                                  │
│                    Stockage Dual Layer                               │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  🗄️ LAYER 1 : POSTGRESQL (Données Structurées)                      │
│  ├─ Modèle Merise normalisé (3NF)                                   │
│  ├─ Tables :                                                         │
│  │   • source (9 sources)                                            │
│  │   • flux (12 flux collectés)                                      │
│  │   • document (25,141 documents)                                   │
│  │   • territoire (4 villes)                                         │
│  │   • meteo (8 relevés)                                             │
│  ├─ Contraintes d'intégrité :                                        │
│  │   • PRIMARY KEY auto-incrémentées                                 │
│  │   • FOREIGN KEY avec ON DELETE CASCADE                            │
│  │   • UNIQUE sur hash_fingerprint (déduplication)                   │
│  ├─ Indexes :                                                        │
│  │   • date_publication (requêtes temporelles)                       │
│  │   • hash_fingerprint (recherche doublons)                         │
│  └─ Backup quotidien :                                               │
│      • pg_dump via Docker                                            │
│      • Versioning datasens/versions/datasens_pg_vXXXX.sql           │
│                                                                      │
│  ☁️ LAYER 2 : MINIO (DataLake Fichiers Bruts)                       │
│  ├─ Bucket : datasens-raw                                            │
│  ├─ Structure :                                                      │
│  │   • /kaggle/*.csv (fichiers CSV originaux)                        │
│  │   • /rss/*.json (flux RSS bruts)                                  │
│  │   • /scraping/*.json (données Web Scraping)                       │
│  │   • /gdelt/*.csv.zip (fichiers GDELT)                             │
│  │   • /meteo/*.json (relevés OWM)                                   │
│  │   • /historique/*.csv (événements historiques)                    │
│  ├─ Manifests JSON :                                                 │
│  │   • Métadonnées : date_collecte, source, format, taille           │
│  │   • Traçabilité : origine, transformations appliquées             │
│  │   • Versioning : hash MD5, URI MinIO                              │
│  └─ Retention : Illimitée (coût faible S3-compatible)               │
│                                                                      │
│  📊 LAYER 3 : VERSIONING (Git-like Data)                             │
│  ├─ Snapshots PostgreSQL horodatés                                  │
│  ├─ Logs dans README_VERSIONNING.md                                 │
│  └─ Format : "YYYY-MM-DD HH:MM:SS UTC | ACTION | Détails"           │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

---

## 📊 STATISTIQUES FINALES

### Données Collectées
```
TOTAL : 25,141 documents
├─ Kaggle CSV               : 24,683 (98.2%)
├─ Web Scraping             :    265 (1.1%)
├─ RSS Multi-Sources        :     99 (0.4%)
├─ GDELT Big Data           :     57 (0.2%)
├─ Événements Historiques   :     37 (0.1%)
└─ Météo (table séparée)    :      8 relevés
```

### Couverture Temporelle
```
KAGGLE        : 2009-2009 (tweets Sentiment140)
RSS           : 2025-10-28 (temps réel)
WEB SCRAPING  : 2025-10-28 (temps réel)
GDELT         : 2025-10-28 (dernières 2h30)
MÉTÉO         : 2025-10-28 (temps réel)
HISTORIQUE    : 1995-2024 (30 ans d'événements France)
```

### Types d'Événements Historiques
```
ATTENTATS            :  8 événements (Charlie Hebdo, Bataclan, Nice...)
GRÈVES               :  5 événements (1995, 2010, 2016, 2019, 2023)
CHANGEMENTS POLITIQUES : 11 événements (élections, gouvernements)
CATASTROPHES         :  4 événements (Xynthia, Klaus, canicules...)
CRISES ÉCONOMIQUES   :  3 événements (2008, 2011, 2020)
SANITAIRE            :  2 événements (COVID confinements)
INTERNATIONAL        :  2 événements (George Floyd, Guerre Ukraine)
AUTRES               :  2 événements (Notre-Dame, Gilets Jaunes)
```

---

## 🔄 CARACTÉRISTIQUES ETL

### ✅ Ce qui fait de DataSens un vrai ETL

1. **EXTRACT** :
   - ✅ Multi-sources (5 types différents)
   - ✅ Multi-formats (CSV, JSON, XML, HTML)
   - ✅ Multi-protocoles (HTTP, API REST, Scraping)
   - ✅ Gestion erreurs et retry (tenacity)
   - ✅ Rate limiting (respect robots.txt)

2. **TRANSFORM** :
   - ✅ Déduplication (SHA256 hash)
   - ✅ Nettoyage (nulls, espaces, HTML)
   - ✅ Normalisation (dates, langues)
   - ✅ Enrichissement (tonalité GDELT, géolocalisation)
   - ✅ Filtrage (France only pour GDELT)
   - ✅ Agrégation (multi-sources → source unique)

3. **LOAD** :
   - ✅ Dual Layer (PostgreSQL + MinIO)
   - ✅ Schéma normalisé (Merise 3NF)
   - ✅ Contraintes d'intégrité (PK, FK, UNIQUE)
   - ✅ Indexes optimisés
   - ✅ Versioning (snapshots quotidiens)
   - ✅ Traçabilité (manifests JSON)

### 🆚 Comparaison ETL vs ELT

Votre pipeline est **ETL** (pas ELT) car :
- ✅ Transformation **AVANT** chargement PostgreSQL
- ✅ Déduplication appliquée **AVANT** insertion
- ✅ Nettoyage/Normalisation **AVANT** base
- ❌ Pas de "data lake d'abord, transformation après"

---

## 🎯 PROCHAINES ÉTAPES

### Court Terme (Jury E1)
- ✅ 5 types de sources collectées
- ✅ 25,141 documents en base
- ✅ Événements historiques France (1995-2025)
- ✅ Pipeline ETL complet documenté

### Moyen Terme (E2 - Analyse)
- 📊 Analyse sentiments (NLP sur textes)
- 📈 Corrélations événements/sentiments
- 🗺️ Visualisations géographiques
- 📉 Séries temporelles (impact grèves/attentats)

### Long Terme (E3 - Production)
- 🔄 Automatisation collecte (GitHub Actions)
- 📊 Dashboard Grafana temps réel
- 🤖 Machine Learning (prédiction sentiments)
- 🌍 Extension internationale (Europe)

---

## 🎓 DÉMONSTRATION JURY

**Argumentaire ETL** :

> "DataSens implémente un pipeline **ETL classique** avec :
>
> 1. **EXTRACT** : 5 types de sources (fichier plat, BDD, web scraping, API, big data)
> 2. **TRANSFORM** : Déduplication SHA256, nettoyage, normalisation, enrichissement géolocalisation
> 3. **LOAD** : Architecture dual layer PostgreSQL (structuré) + MinIO (DataLake)
>
> Caractéristiques :
> - ✅ 25,141 documents collectés
> - ✅ 37 événements historiques France (1995-2025)
> - ✅ Déduplication automatique (0 doublons)
> - ✅ Versioning quotidien (snapshots PostgreSQL)
> - ✅ Traçabilité complète (manifests JSON)
> - ✅ Prêt pour collecte automatisée quotidienne (GitHub Actions)"

---

**Votre pipeline est maintenant complet avec données historiques ! 🎉**
