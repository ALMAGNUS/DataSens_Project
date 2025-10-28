# 🚀 Guide de Déploiement GitHub

Ce guide explique comment déployer le projet DataSens sur GitHub avec CI/CD automatique.

---

## 📋 Prérequis

- Compte GitHub
- Git installé localement
- Docker Desktop (pour tests locaux)

---

## 🔧 Étapes de déploiement

### 1️⃣ Initialiser le repo Git local

```bash
cd C:\Users\Utilisateur\Desktop\Datasens_Project

# Initialiser Git (si pas déjà fait)
git init

# Vérifier les fichiers ignorés
git status
```

### 2️⃣ Créer le repo sur GitHub

1. Aller sur https://github.com/new
2. Nom du repo : `datasens-project`
3. Description : "Projet Big Data - Collecte multi-sources avec DataLake MinIO et SGBD PostgreSQL"
4. **Visibilité** : Public (pour montrer au jury) ou Private
5. Ne pas initialiser avec README (tu en as déjà un)
6. Cliquer sur "Create repository"

### 3️⃣ Lier le repo local à GitHub

```bash
# Ajouter l'origin (remplace TON_USERNAME)
git remote add origin https://github.com/TON_USERNAME/datasens-project.git

# Vérifier
git remote -v
```

### 4️⃣ Premier commit & push

```bash
# Ajouter tous les fichiers (sauf ceux dans .gitignore)
git add .

# Vérifier ce qui sera committé
git status

# Commit
git commit -m "🎉 Initial commit - Projet DataSens E1 avec MinIO + PostgreSQL"

# Créer la branche main
git branch -M main

# Pousser vers GitHub
git push -u origin main
```

---

## ✅ Vérifications post-déploiement

### Sur GitHub

1. **README.md** s'affiche automatiquement avec architecture
2. **Actions** → onglet "Actions" → CI/CD se lance automatiquement
3. **Secrets** protégés (`.env` non pushé grâce à `.gitignore`)

### CI/CD Automatique

Le workflow `.github/workflows/ci.yml` va :
- ✅ Tester les imports Python
- ✅ Valider les notebooks
- ✅ Tester Docker (MinIO, PostgreSQL, Redis)
- ✅ Vérifier la documentation

---

## 🔒 Sécuriser les secrets (important pour le jury)

### GitHub Secrets (pour CI/CD)

Si tu veux tester avec de vraies API keys en CI :

1. GitHub → Settings → Secrets and variables → Actions
2. Ajouter :
   - `OWM_API_KEY`
   - `YOUTUBE_API_KEY`
   - `NEWSAPI_KEY`

Puis modifier `.github/workflows/ci.yml` :
```yaml
env:
  OWM_API_KEY: ${{ secrets.OWM_API_KEY }}
```

---

## 📊 Badge de statut (impression du jury)

Ajouter en haut du `README.md` :

```markdown
![CI Status](https://github.com/TON_USERNAME/datasens-project/workflows/CI%2FCD%20DataSens/badge.svg)
```

Badge vert = ✅ tous les tests passent !

---

## 🎓 Pour le jury

### Points à mettre en avant

1. **Architecture professionnelle**
   - Docker Compose (MinIO + PostgreSQL + Redis)
   - CI/CD automatique GitHub Actions
   - .gitignore sécurisé (pas de secrets commitées)

2. **Reproductibilité**
   - Un seul `docker-compose up -d` → infra prête
   - `requirements.txt` → dépendances figées
   - `.env.example` → template de configuration

3. **Best practices**
   - Structure projet claire (data/logs/docs/flows)
   - Documentation complète (README, architecture)
   - Tests automatisés (validation notebooks)

---

## 🔄 Workflow de développement

### Pour les futures modifications

```bash
# Créer une branche feature
git checkout -b feature/e2-enrichissement

# Faire des modifs
# ...

# Commit
git add .
git commit -m "✨ Ajout enrichissement IA (E2)"

# Push
git push origin feature/e2-enrichissement

# Sur GitHub : créer une Pull Request
# CI/CD testera automatiquement
```

---

## 📧 Partage avec le jury

**Lien à donner** :
```
https://github.com/TON_USERNAME/datasens-project
```

Le jury pourra :
- ✅ Voir le code
- ✅ Lire la doc
- ✅ Vérifier les tests CI/CD (badge vert)
- ✅ Cloner et lancer en 3 commandes

---

## 🎯 Commandes rapides pour démo jury

```bash
# Cloner
git clone https://github.com/TON_USERNAME/datasens-project.git
cd datasens-project

# Copier config
cp .env.example .env

# Lancer infra
docker-compose up -d

# Installer Python deps
pip install -r requirements.txt

# Ouvrir notebook
jupyter notebook datasens_E1_v2.ipynb
```

**Temps total : 2 minutes** ⚡

---

## 🆘 Troubleshooting

### Git refuse de push (trop gros fichiers)

```bash
# Vérifier la taille
git ls-files --cached | xargs du -h | sort -h

# Retirer un gros fichier
git rm --cached data/raw/huge_file.csv
echo "data/raw/*.csv" >> .gitignore
git commit -m "🔧 Fix: ignore gros fichiers CSV"
```

### CI/CD échoue

1. Vérifier les logs : GitHub → Actions → clic sur le workflow rouge
2. Corriger localement
3. Commit + push
4. CI/CD relance automatiquement

---

**✅ Setup complet prêt pour soutenance !**
