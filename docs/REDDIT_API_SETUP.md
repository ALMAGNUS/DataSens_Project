# 📱 GUIDE : Obtenir vos credentials Reddit API

## ⏱️ Temps requis : 3 minutes

---

## **Étape 1 : Créer un compte Reddit** (si nécessaire)

1. Allez sur : https://www.reddit.com
2. Cliquez sur "Sign Up"
3. Email : `jaffre.alan.pro@gmail.com`
4. Username : `alanjaffr` (ou autre)
5. Password : Votre choix

---

## **Étape 2 : Créer une application Reddit**

1. **Allez sur** : https://www.reddit.com/prefs/apps

2. **Scrollez en bas** et cliquez sur **"are you a developer? create an app..."**

3. **Remplissez le formulaire** :
   ```
   Name              : DataSens Educational Project
   App type          : ☑️ script (sélectionner "script")
   Description       : Educational data collection for university project
   About URL         : (laisser vide)
   Redirect URI      : http://localhost:8080
   ```

4. **Cliquez sur** : `Create app`

---

## **Étape 3 : Récupérer les credentials**

Vous verrez une carte comme ceci :

```
DataSens Educational Project
───────────────────────────────────────
personal use script

[ABC123def456ghi]  ← REDDIT_CLIENT_ID (14 caractères)

secret: xyz789abc123def456ghi789  ← REDDIT_CLIENT_SECRET (27 caractères)

───────────────────────────────────────
```

---

## **Étape 4 : Copier dans .env**

**Donnez-moi simplement** :

```
REDDIT_CLIENT_ID=ABC123def456ghi
REDDIT_CLIENT_SECRET=xyz789abc123def456ghi789
```

Je mettrai à jour le `.env` automatiquement !

---

## ℹ️ **Informations importantes**

### ✅ **Plan gratuit** :
- **60 requêtes/minute** (amplement suffisant)
- **Aucune limite de quota** journalier
- **Accès lecture seule** (parfait pour collecte)

### 🎯 **Usage dans le projet** :
```python
# Collecte 150 posts (3 subreddits × 50)
subreddits = ["france", "French", "AskFrance"]
total_posts = 150

# = 3 requêtes API seulement
# Temps : ~10 secondes
```

### 🔒 **Sécurité** :
- ✅ Credentials dans `.env` (gitignored)
- ✅ User-agent identifiable
- ✅ Respect rate limits automatique

---

## 🚀 **Alternative : Skip Reddit (optionnel)**

Si vous voulez **tester sans Reddit** :
- Les autres sources fonctionneront quand même
- Vous aurez ~1500 documents (au lieu de ~2400)
- Vous pourrez ajouter Reddit plus tard

---

**Voulez-vous créer l'app Reddit maintenant ?** ✅
