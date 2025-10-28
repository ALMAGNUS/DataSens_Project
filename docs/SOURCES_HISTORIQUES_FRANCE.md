# 📜 Sources de Données Historiques France - DataSens

Pour enrichir votre pipeline ETL avec des événements historiques français (grèves, tempêtes, changements politiques, attentats...), voici les meilleures sources **gratuites et légales**.

---

## 🏛️ 1. DATA.GOUV.FR (Open Data Gouvernement)

### A. Élections Présidentielles & Législatives (1958-2025)
**URL** : https://www.data.gouv.fr/fr/datasets/election-presidentielle-des-23-avril-et-7-mai-2017-resultats-definitifs-du-2nd-tour/

**Contenu** :
- Résultats élections présidentielles (tous les 5 ans depuis 1958)
- Élections législatives (2017, 2022)
- Format : CSV, JSON, Excel
- Géolocalisation : par commune, département, région

**Utilisation DataSens** :
```python
# Exemple extraction
import pandas as pd

url_elec = "https://www.data.gouv.fr/fr/datasets/r/16b9e698-64d4-4a58-8a0c-db3f50e6e6f6"
df_elections = pd.read_csv(url_elec, sep=';', encoding='utf-8')

# Événements : changements de président
elections_pres = df_elections[df_elections['Type élection'] == 'Présidentielle']
# 2017: Macron élu, 2022: Macron réélu, etc.
```

**Événements couverts** :
- ✅ 2017 : Élection Macron (président)
- ✅ 2022 : Réélection Macron
- ✅ 2020 : Remaniement Castex → Borne (Premier ministre)
- ✅ 2024 : Nouveau gouvernement Attal puis Barnier

---

### B. Données Météo Historiques (Météo-France Open Data)
**URL** : https://www.data.gouv.fr/fr/datasets/donnees-climatologiques-de-base-quotidiennes/

**Contenu** :
- Données quotidiennes depuis 1950
- Températures, précipitations, vent
- 62 stations météo France
- Format : CSV (1 fichier/station/an)

**Événements tempêtes historiques** :
- ✅ 1999 : Tempêtes Lothar et Martin (26-28 décembre)
- ✅ 2009 : Tempête Klaus (24 janvier)
- ✅ 2010 : Tempête Xynthia (27-28 février)
- ✅ 2017 : Ouragan Irma (Antilles françaises)
- ✅ 2022 : Sécheresse record (été)

```python
# Extraction tempête Xynthia (27-28 février 2010)
url_meteo = "https://www.data.gouv.fr/fr/datasets/r/90a98de0-f562-4328-aa16-fe0dd1dca60f"
df_meteo = pd.read_csv(url_meteo, sep=';')

# Filtrer février 2010, vitesse vent > 100 km/h
tempete = df_meteo[(df_meteo['date'].str.startswith('2010-02')) & 
                    (df_meteo['ff'] > 100)]  # ff = force du vent
```

---

## 📰 2. ARCHIVES INA (Institut National de l'Audiovisuel)

### A. API INA (Métadonnées vidéos historiques)
**URL** : https://www.ina.fr/ina-eclaire-actu
**Documentation API** : https://developer.ina.fr/

**Contenu** :
- Archives JT depuis 1940
- Discours présidentiels
- Événements majeurs (attentats, grèves, manifestations)
- Métadonnées : titre, date, résumé, mots-clés

**Événements couverts** :
- ✅ 2015 : Attentats Charlie Hebdo (7 janvier) + Bataclan (13 novembre)
- ✅ 2016 : Attentat Nice (14 juillet)
- ✅ 2018-2019 : Mouvement Gilets Jaunes
- ✅ 2023 : Révoltes urbaines (juin-juillet)

**Utilisation** :
```python
import requests

# API INA (nécessite clé gratuite)
ina_api_key = "VOTRE_CLE_INA"
url = "https://api.ina.fr/search"

params = {
    "q": "grève générale france",
    "dateStart": "2010-01-01",
    "dateEnd": "2025-01-01",
    "apiKey": ina_api_key
}

r = requests.get(url, params=params)
evenements_ina = r.json()
```

---

## 🔥 3. WIKIPEDIA - ÉVÉNEMENTS HISTORIQUES FRANCE

### A. Liste des grèves en France
**URL** : https://fr.wikipedia.org/wiki/Liste_de_grèves

**Scraping légal** (respecter robots.txt) :
```python
from bs4 import BeautifulSoup
import requests

url = "https://fr.wikipedia.org/wiki/Liste_de_grèves"
r = requests.get(url)
soup = BeautifulSoup(r.text, 'html.parser')

# Extraire tableau grèves France
greves = []
for row in soup.select('table.wikitable tr'):
    cols = row.find_all('td')
    if len(cols) >= 3:
        greves.append({
            'date': cols[0].text.strip(),
            'evenement': cols[1].text.strip(),
            'secteur': cols[2].text.strip()
        })
```

**Événements couverts** :
- ✅ 1995 : Grève générale (réforme retraites Juppé)
- ✅ 2010 : Grève retraites (réforme Sarkozy)
- ✅ 2016 : Grève loi Travail (El Khomri)
- ✅ 2018-2020 : Grève retraites (réforme Macron)
- ✅ 2023 : Grève retraites (64 ans)

---

### B. Chronologie des attentats en France
**URL** : https://fr.wikipedia.org/wiki/Liste_d%27attentats_meurtriers_en_France

**Événements majeurs** :
- ✅ 2012 : Tuerie Toulouse/Montauban (Mohamed Merah)
- ✅ 2015 : Charlie Hebdo + Hyper Cacher (janvier)
- ✅ 2015 : Attentats 13 novembre (Bataclan, Saint-Denis, terrasses)
- ✅ 2016 : Attentat Nice (14 juillet, 86 morts)
- ✅ 2016 : Assassinat prêtre Saint-Étienne-du-Rouvray
- ✅ 2018 : Attentat Strasbourg (marché de Noël)
- ✅ 2020 : Assassinat Samuel Paty

---

## 📊 4. EUROSTAT - Statistiques Européennes

### A. Données Économiques & Sociales France
**URL** : https://ec.europa.eu/eurostat/data/database

**Contenu** :
- Taux chômage mensuel (1975-2025)
- PIB trimestriel
- Inflation mensuelle
- Grèves (jours de travail perdus)

**Utilisation** :
```python
# API Eurostat (gratuite)
import eurostat

# Taux de chômage France
df_chomage = eurostat.get_data_df('une_rt_m', flags=False)
df_france = df_chomage[df_chomage['geo'] == 'FR']

# Identifier périodes de crise
crises = df_france[df_france['values'] > 10]  # Chômage > 10%
```

**Événements économiques** :
- ✅ 2008-2009 : Crise financière mondiale
- ✅ 2011-2012 : Crise dettes souveraines (€)
- ✅ 2020 : Crise COVID-19 (confinements)
- ✅ 2022-2023 : Inflation record (énergie)

---

## 🌍 5. GDELT (Déjà intégré) - Événements Temps Réel

**Votre source actuelle** GDELT couvre déjà :
- ✅ Manifestations (PROTEST)
- ✅ Violences (RIOT, ASSAULT)
- ✅ Politique (GOVERNMENT, ELECTIONS)
- ✅ Santé (HEALTH, EPIDEMIC)

**Amélioration** : Requêter les **archives GDELT** (2015-2025) :
```python
# Archive GDELT journalière complète
import datetime as dt

def download_gdelt_day(date):
    """Télécharge tous les fichiers GDELT d'une journée"""
    date_str = date.strftime("%Y%m%d")
    
    # GDELT publie 96 fichiers/jour (toutes les 15 min)
    events = []
    for hour in range(0, 24):
        for minute in [0, 15, 30, 45]:
            timestamp = f"{date_str}{hour:02d}{minute:02d}00"
            url = f"http://data.gdeltproject.org/gdeltv2/{timestamp}.gkg.csv.zip"
            # ... téléchargement et parsing
    
    return events

# Exemple : récupérer événements attentats 13 novembre 2015
events_bataclan = download_gdelt_day(dt.datetime(2015, 11, 13))
```

---

## 🏛️ 6. ASSEMBLÉE NATIONALE - Données Parlementaires

### A. API Open Data Assemblée
**URL** : https://data.assemblee-nationale.fr/

**Contenu** :
- Votes de loi (2007-2025)
- Motions de censure
- Compositions gouvernements
- Questions au gouvernement

**Événements couverts** :
- ✅ 2017 : Élection Macron → Nouveau gouvernement Philippe
- ✅ 2020 : Démission Philippe → Castex
- ✅ 2022 : Borne Première ministre
- ✅ 2024 : Attal puis Barnier
- ✅ 2023 : Adoption 49.3 réforme retraites

```python
# API Assemblée Nationale
url_votes = "https://data.assemblee-nationale.fr/travaux-parlementaires/scrutins"
r = requests.get(url_votes, headers={"Accept": "application/json"})
votes = r.json()

# Filtrer lois majeures
lois_retraite = [v for v in votes if 'retraite' in v['titre'].lower()]
```

---

## 🗂️ 7. LEGIFRANCE - Textes Officiels

### A. Journal Officiel (JO)
**URL** : https://www.legifrance.gouv.fr/

**Contenu** :
- Décrets présidentiels
- Nominations ministres
- Dissolutions Assemblée
- États d'urgence

**Événements** :
- ✅ 2015 : État d'urgence (attentats)
- ✅ 2020 : État d'urgence sanitaire (COVID)
- ✅ 2024 : Dissolution Assemblée Nationale (juin)

---

## 📅 8. BASE ÉVÉNEMENTS HISTORIQUES (À CRÉER)

Je vous propose de créer un **fichier CSV d'événements majeurs** à intégrer dans votre pipeline :

```csv
date,type,titre,description,impact
2015-01-07,attentat,Charlie Hebdo,"Attaque terroriste contre Charlie Hebdo, 12 morts",5
2015-11-13,attentat,Attentats Paris,"Bataclan + terrasses + Saint-Denis, 130 morts",5
2016-07-14,attentat,Attentat Nice,"Camion-bélier 14 juillet, 86 morts",5
2018-11-17,manifestation,Début Gilets Jaunes,"Première manifestation nationale",4
2019-12-05,greve,Grève retraites 2019,"Grève générale contre réforme Macron",4
2020-03-17,sanitaire,Confinement COVID-19,"1er confinement national",5
2022-04-24,politique,Réélection Macron,"2e mandat présidentiel",3
2023-03-16,politique,49.3 Retraites,"Passage en force réforme 64 ans",4
2024-06-09,politique,Dissolution Assemblée,"Macron dissout l'Assemblée Nationale",4
```

---

## 🚀 Intégration dans votre pipeline ETL

Créez une nouvelle étape dans `datasens_E1_v2.ipynb` :

```python
# Étape 13 : Événements Historiques France

print("📜 COLLECTE ÉVÉNEMENTS HISTORIQUES FRANCE")
print("="*60)

# 1. Télécharger CSV événements
evenements_url = "https://raw.githubusercontent.com/votre_compte/datasens/main/data/evenements_france.csv"
df_events = pd.read_csv(evenements_url)

# 2. Transformer
df_events['date_publication'] = pd.to_datetime(df_events['date'])
df_events['hash_fingerprint'] = df_events.apply(
    lambda row: hashlib.sha256(row['description'].encode()).hexdigest(),
    axis=1
)

# 3. Charger PostgreSQL
for _, event in df_events.iterrows():
    # Créer flux historique
    # Insérer document
    pass

print(f"✅ {len(df_events)} événements historiques chargés")
```

---

## 📊 Résumé des sources recommandées

| Source | Type | Période | Événements | Gratuit | API |
|--------|------|---------|-----------|---------|-----|
| **data.gouv.fr** | Élections, Météo | 1950-2025 | Présidents, Tempêtes | ✅ | ❌ |
| **INA** | Vidéos archives | 1940-2025 | Attentats, Grèves | ✅ | ✅ |
| **Wikipedia** | Encyclopédie | 1789-2025 | Tous événements | ✅ | ❌ |
| **Eurostat** | Économie | 1975-2025 | Crises, Chômage | ✅ | ✅ |
| **GDELT Archives** | Big Data | 2015-2025 | Temps réel mondial | ✅ | ✅ |
| **Assemblée Nationale** | Parlementaire | 2007-2025 | Lois, Votes | ✅ | ✅ |
| **Legifrance** | Juridique | 1789-2025 | JO, Décrets | ✅ | ❌ |

---

## 🎯 Plan d'action recommandé

1. **Phase 1 (immédiat)** : Créer CSV événements majeurs (2015-2025)
2. **Phase 2** : Scraper Wikipedia grèves + attentats
3. **Phase 3** : Intégrer API data.gouv.fr (élections)
4. **Phase 4** : Requêter GDELT archives (2015-2025)
5. **Phase 5** : Ajouter Eurostat économie

**Voulez-vous que je crée le fichier CSV des événements majeurs 2015-2025 ?** 📅
