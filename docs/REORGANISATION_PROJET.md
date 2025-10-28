# 🗂️ REORGANISATION ARBORESCENCE DATASENS

## ❌ Problèmes actuels

1. **Scripts Python à la racine** (au lieu de `scripts/`)
   - check_e1_status.py
   - collect_evenements_historiques.py
   - collect_gdelt_batch.py
   - demo_jury_simple.py
   - monitor_owm.py
   - test_api_keys.py
   - test_reddit.py

2. **Duplication folders** : `datasens/` à la racine ET dans `notebooks/`
3. **README dupliqué** : `README_VERSIONNING.md` à la racine ET dans `notebooks/`
4. **Fichier sensible à la racine** : `kaggle.json` (devrait être ignoré ou dans `.env`)

---

## ✅ Structure Propre Recommandée

```
Datasens_Project/
│
├── 📂 .github/                    # GitHub Actions workflows
│   └── workflows/
│       └── daily-collection.yml
│
├── 📂 data/                       # Données brutes et transformées
│   ├── raw/                       # Données brutes (non versionnées)
│   │   ├── kaggle/
│   │   ├── rss/
│   │   ├── scraping/
│   │   ├── gdelt/
│   │   └── meteo/
│   ├── processed/                 # Données nettoyées (optionnel)
│   └── evenements_historiques_france.csv  # Événements historiques
│
├── 📂 datasens/                   # Package Python principal
│   ├── __init__.py
│   ├── config.py                  # Configuration centralisée
│   ├── collectors/                # Modules de collecte
│   │   ├── __init__.py
│   │   ├── kaggle.py
│   │   ├── rss.py
│   │   ├── scraping.py
│   │   ├── gdelt.py
│   │   └── openweathermap.py
│   ├── transformers/              # Modules de transformation
│   │   ├── __init__.py
│   │   ├── deduplication.py
│   │   └── normalization.py
│   ├── loaders/                   # Modules de chargement
│   │   ├── __init__.py
│   │   ├── postgresql.py
│   │   └── minio.py
│   └── versions/                  # Backups PostgreSQL
│       └── datasens_pg_vXXXX.sql
│
├── 📂 notebooks/                  # Jupyter Notebooks (analyse & démo)
│   ├── datasens_E1_v2.ipynb      # Notebook principal E1
│   ├── demo_jury.ipynb           # Démo simplifiée jury
│   └── collecte_journaliere.ipynb # Orchestration quotidienne
│
├── 📂 scripts/                    # Scripts utilitaires Python
│   ├── check_e1_status.py        # ← DÉPLACER ICI
│   ├── collect_evenements_historiques.py  # ← DÉPLACER ICI
│   ├── collect_gdelt_batch.py    # ← DÉPLACER ICI
│   ├── test_api_keys.py          # ← DÉPLACER ICI
│   ├── test_reddit.py            # ← DÉPLACER ICI
│   └── verify_data_jury.py       # Déjà présent
│
├── 📂 docs/                       # Documentation
│   ├── ARCHITECTURE_ETL.md
│   ├── SOURCES_HISTORIQUES_FRANCE.md
│   └── GITHUB_SECRETS_SETUP.md   # ← DÉPLACER ICI
│
├── 📂 flows/                      # Orchestration (Prefect/Airflow)
│   └── (vide pour l'instant)
│
├── 📂 logs/                       # Logs d'exécution
│   └── (fichiers .log)
│
├── 📂 .venv/                      # Environnement virtuel (non versionné)
│
├── 📄 .env                        # Variables d'environnement (NON VERSIONNÉ)
├── 📄 .env.example                # Template variables d'environnement
├── 📄 .gitignore                  # Fichiers à ignorer
├── 📄 docker-compose.yml          # Services Docker (PostgreSQL, MinIO, Redis)
├── 📄 requirements.txt            # Dépendances Python
├── 📄 README.md                   # Documentation principale projet
└── 📄 README_VERSIONNING.md       # Historique versions (UNIQUE à la racine)
```

---

## 🚀 Actions de Réorganisation

### 1. Déplacer les scripts Python

```powershell
# Déplacer vers scripts/
mv check_e1_status.py scripts/
mv collect_evenements_historiques.py scripts/
mv collect_gdelt_batch.py scripts/
mv test_api_keys.py scripts/
mv test_reddit.py scripts/
mv monitor_owm.py scripts/

# Supprimer demo_jury_simple.py (doublon avec notebook demo_jury.ipynb)
rm demo_jury_simple.py
```

### 2. Déplacer documentation

```powershell
# Déplacer GITHUB_SECRETS_SETUP.md vers docs/
mv GITHUB_SECRETS_SETUP.md docs/
```

### 3. Nettoyer duplications

```powershell
# Supprimer datasens/ dans notebooks/ (doublon)
rm -Recurse notebooks/datasens/

# Supprimer README_VERSIONNING.md dans notebooks/ (doublon)
rm notebooks/README_VERSIONNING.md

# Garder uniquement README_VERSIONNING.md à la racine
```

### 4. Sécuriser kaggle.json

```powershell
# Option 1 : Déplacer dans .env (recommandé)
# Supprimer kaggle.json et utiliser uniquement variables d'environnement

# Option 2 : Déplacer dans dossier caché
mv kaggle.json ~/.kaggle/kaggle.json  # Standard Kaggle

# Ajouter à .gitignore
echo "kaggle.json" >> .gitignore
```

### 5. Créer structure datasens/ comme package

```powershell
# Créer __init__.py pour faire de datasens/ un package Python
New-Item datasens/__init__.py -ItemType File -Force
New-Item datasens/collectors/__init__.py -ItemType File -Force
New-Item datasens/transformers/__init__.py -ItemType File -Force
New-Item datasens/loaders/__init__.py -ItemType File -Force
```

---

## 📋 Script PowerShell de Réorganisation Automatique

```powershell
# reorganize.ps1 - Exécuter dans le dossier Datasens_Project

Write-Host "🗂️ RÉORGANISATION ARBORESCENCE DATASENS" -ForegroundColor Cyan

# 1. Déplacer scripts Python vers scripts/
Write-Host "`n📦 Déplacement scripts Python..." -ForegroundColor Yellow
Move-Item -Path "check_e1_status.py" -Destination "scripts/" -Force
Move-Item -Path "collect_evenements_historiques.py" -Destination "scripts/" -Force
Move-Item -Path "collect_gdelt_batch.py" -Destination "scripts/" -Force
Move-Item -Path "test_api_keys.py" -Destination "scripts/" -Force
Move-Item -Path "test_reddit.py" -Destination "scripts/" -Force
Move-Item -Path "monitor_owm.py" -Destination "scripts/" -Force

# 2. Supprimer doublons
Write-Host "`n🧹 Suppression doublons..." -ForegroundColor Yellow
Remove-Item -Path "demo_jury_simple.py" -Force -ErrorAction SilentlyContinue
Remove-Item -Path "notebooks/datasens" -Recurse -Force -ErrorAction SilentlyContinue
Remove-Item -Path "notebooks/README_VERSIONNING.md" -Force -ErrorAction SilentlyContinue

# 3. Déplacer documentation
Write-Host "`n📄 Déplacement documentation..." -ForegroundColor Yellow
Move-Item -Path "GITHUB_SECRETS_SETUP.md" -Destination "docs/" -Force -ErrorAction SilentlyContinue

# 4. Créer structure package Python
Write-Host "`n📦 Création structure package..." -ForegroundColor Yellow
New-Item -Path "datasens/__init__.py" -ItemType File -Force | Out-Null
New-Item -Path "datasens/collectors" -ItemType Directory -Force | Out-Null
New-Item -Path "datasens/collectors/__init__.py" -ItemType File -Force | Out-Null
New-Item -Path "datasens/transformers" -ItemType Directory -Force | Out-Null
New-Item -Path "datasens/transformers/__init__.py" -ItemType File -Force | Out-Null
New-Item -Path "datasens/loaders" -ItemType Directory -Force | Out-Null
New-Item -Path "datasens/loaders/__init__.py" -ItemType File -Force | Out-Null

# 5. Sécuriser kaggle.json
Write-Host "`n🔐 Sécurisation kaggle.json..." -ForegroundColor Yellow
if (Test-Path "kaggle.json") {
    $kaggleDir = "$env:USERPROFILE\.kaggle"
    New-Item -Path $kaggleDir -ItemType Directory -Force | Out-Null
    Move-Item -Path "kaggle.json" -Destination "$kaggleDir\kaggle.json" -Force
    Write-Host "   ✅ kaggle.json déplacé vers ~/.kaggle/" -ForegroundColor Green
}

# 6. Mettre à jour .gitignore
Write-Host "`n📝 Mise à jour .gitignore..." -ForegroundColor Yellow
Add-Content -Path ".gitignore" -Value "`nkaggle.json`ndata/raw/*`n!data/raw/.gitkeep"

Write-Host "`n✅ RÉORGANISATION TERMINÉE !" -ForegroundColor Green
Write-Host "   Vérifiez avec: tree /F" -ForegroundColor Cyan
```

---

## 🎯 Résultat Final

```
Datasens_Project/
├── 📂 .github/workflows/
├── 📂 data/
│   ├── raw/
│   └── evenements_historiques_france.csv
├── 📂 datasens/
│   ├── collectors/
│   ├── transformers/
│   ├── loaders/
│   └── versions/
├── 📂 notebooks/
│   ├── datasens_E1_v2.ipynb
│   ├── demo_jury.ipynb
│   └── collecte_journaliere.ipynb
├── 📂 scripts/                    ← TOUS LES .py ICI
│   ├── check_e1_status.py
│   ├── collect_evenements_historiques.py
│   ├── collect_gdelt_batch.py
│   ├── test_api_keys.py
│   └── verify_data_jury.py
├── 📂 docs/
│   ├── ARCHITECTURE_ETL.md
│   ├── SOURCES_HISTORIQUES_FRANCE.md
│   └── GITHUB_SECRETS_SETUP.md
├── 📄 .env
├── 📄 docker-compose.yml
├── 📄 requirements.txt
└── 📄 README_VERSIONNING.md
```

---

**Voulez-vous que j'exécute la réorganisation automatique ?** 🚀
