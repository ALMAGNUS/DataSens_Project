# 📘 DataSens - Dictionnaire des Données E1

**Version** : E1
**Date** : 2025-01-29
**Base de données** : PostgreSQL
**Schéma** : Merise (18 tables)

---

## 🗂️ Tables par domaine fonctionnel

### 📥 COLLECTE (Traçabilité des sources)

#### `type_donnee`
Catégorisation des types de sources de données.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_type_donnee` | SERIAL | Clé primaire |
| `libelle` | VARCHAR(100) | Type (Fichier plat, Base de données, API, Web Scraping, Big Data) |
| `description` | TEXT | Description détaillée |

#### `source`
Sources réelles de collecte de données.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_source` | SERIAL | Clé primaire |
| `id_type_donnee` | INT | FK vers `type_donnee` |
| `nom` | VARCHAR(100) | Nom de la source (ex: Kaggle, OpenWeatherMap) |
| `url` | TEXT | URL de la source |
| `fiabilite` | FLOAT | Score de fiabilité (0.0 à 1.0) |

#### `flux`
Traçabilité des collectes de données.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_flux` | SERIAL | Clé primaire |
| `id_source` | INT | FK vers `source` |
| `date_collecte` | TIMESTAMP | Date/heure de collecte |
| `format` | VARCHAR(20) | Format des données (csv, json, xml...) |
| `manifest_uri` | TEXT | URI du manifest JSON de traçabilité |

---

### 📄 CORPUS (Documents et territoires)

#### `document`
Documents bruts collectés depuis toutes les sources.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_doc` | SERIAL | Clé primaire |
| `id_flux` | INT | FK vers `flux` (peut être NULL) |
| `id_territoire` | INT | FK vers `territoire` (géolocalisation) |
| `titre` | TEXT | Titre du document |
| `texte` | TEXT | Contenu textuel complet |
| `langue` | VARCHAR(10) | Code langue (fr, en, es...) |
| `date_publication` | TIMESTAMP | Date de publication originale |
| `hash_fingerprint` | VARCHAR(64) | Hash SHA-256 pour déduplication (UNIQUE) |

#### `territoire`
Géolocalisation (communes, villes, départements).

| Colonne | Type | Description |
|---------|------|-------------|
| `id_territoire` | SERIAL | Clé primaire |
| `ville` | VARCHAR(120) | Nom de la ville |
| `code_insee` | VARCHAR(10) | Code INSEE (UNIQUE) |
| `lat` | FLOAT | Latitude |
| `lon` | FLOAT | Longitude |

---

### 🌦️ CONTEXTE (Météo et indicateurs)

#### `type_meteo`
Types de conditions météorologiques.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_type_meteo` | SERIAL | Clé primaire |
| `code` | VARCHAR(20) | Code météo (CLEAR, CLOUDS, RAIN...) |
| `libelle` | VARCHAR(100) | Libellé français |

#### `meteo`
Relevés météorologiques par territoire.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_meteo` | SERIAL | Clé primaire |
| `id_territoire` | INT | FK vers `territoire` |
| `id_type_meteo` | INT | FK vers `type_meteo` |
| `date_obs` | TIMESTAMP | Date/heure d'observation |
| `temperature` | FLOAT | Température en °C |
| `humidite` | FLOAT | Humidité relative (0-100%) |
| `vent_kmh` | FLOAT | Vitesse du vent en km/h (>= 0) |
| `pression` | FLOAT | Pression atmosphérique en hPa (> 0) |
| `meteo_type` | VARCHAR(50) | Type météo (legacy) |

#### `type_indicateur`
Types d'indicateurs socio-économiques.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_type_indic` | SERIAL | Clé primaire |
| `code` | VARCHAR(50) | Code indicateur (POPULATION, REVENU_MEDIAN...) |
| `libelle` | VARCHAR(100) | Libellé |
| `unite` | VARCHAR(20) | Unité de mesure (habitants, €, %, km²...) |

#### `source_indicateur`
Sources des indicateurs (INSEE, IGN, data.gouv.fr...).

| Colonne | Type | Description |
|---------|------|-------------|
| `id_source_indic` | SERIAL | Clé primaire |
| `nom` | VARCHAR(100) | Nom de la source |
| `url` | TEXT | URL de la source |

#### `indicateur`
Valeurs d'indicateurs par territoire et année.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_indic` | SERIAL | Clé primaire |
| `id_territoire` | INT | FK vers `territoire` |
| `id_type_indic` | INT | FK vers `type_indicateur` |
| `id_source_indic` | INT | FK vers `source_indicateur` |
| `valeur` | FLOAT | Valeur de l'indicateur |
| `annee` | INT | Année de référence (1900-2100) |

---

### 🏷️ THÈMES/ÉVÉNEMENTS

#### `theme`
Thèmes documentaires pour classification.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_theme` | SERIAL | Clé primaire |
| `libelle` | VARCHAR(100) | Libellé (Politique, Économie, Environnement...) |
| `description` | TEXT | Description détaillée |

#### `evenement`
Événements temporels avec tonalité émotionnelle.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_event` | SERIAL | Clé primaire |
| `id_theme` | INT | FK vers `theme` |
| `date_event` | TIMESTAMP | Date de l'événement |
| `avg_tone` | FLOAT | Tonalité moyenne (-100 très négatif, +100 très positif) |
| `source_event` | VARCHAR(50) | Source de l'événement (ex: GDELT) |

#### `document_evenement`
Relation N-N entre documents et événements.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_doc` | INT | FK vers `document` (PK composée) |
| `id_event` | INT | FK vers `evenement` (PK composée) |

---

### 🔄 GOUVERNANCE PIPELINE

#### `pipeline`
Description des pipelines ETL.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_pipeline` | SERIAL | Clé primaire |
| `nom` | VARCHAR(100) | Nom du pipeline |
| `description` | TEXT | Description |
| `version` | VARCHAR(20) | Version du pipeline |

#### `etape_etl`
Étapes du pipeline avec ordre d'exécution.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_etape` | SERIAL | Clé primaire |
| `id_pipeline` | INT | FK vers `pipeline` |
| `ordre` | INT | Ordre d'exécution (> 0, UNIQUE par pipeline) |
| `nom_etape` | VARCHAR(100) | Nom de l'étape |
| `type_etape` | VARCHAR(20) | Type (EXTRACT, TRANSFORM, LOAD) |
| `description` | TEXT | Description |

---

### 👤 UTILISATEURS

#### `utilisateur`
Utilisateurs du système (pour futures annotations).

| Colonne | Type | Description |
|---------|------|-------------|
| `id_user` | SERIAL | Clé primaire |
| `nom` | VARCHAR(100) | Nom de l'utilisateur |
| `role` | VARCHAR(50) | Rôle (admin, annotateur, lecteur...) |
| `organisation` | VARCHAR(100) | Organisation |
| `date_creation` | TIMESTAMP | Date de création (défaut: NOW()) |

---

### ✅ QUALITÉ (Contrôles qualité)

#### `qc_rule`
Règles de contrôle qualité.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_qc_rule` | SERIAL | Clé primaire |
| `nom_regle` | VARCHAR(100) | Nom de la règle |
| `description` | TEXT | Description |
| `expression_sql` | TEXT | Expression SQL pour vérification |

#### `qc_result`
Résultats des contrôles qualité par flux.

| Colonne | Type | Description |
|---------|------|-------------|
| `id_qc_result` | SERIAL | Clé primaire |
| `id_qc_rule` | INT | FK vers `qc_rule` |
| `id_flux` | INT | FK vers `flux` |
| `date_check` | TIMESTAMP | Date de vérification (défaut: NOW()) |
| `statut` | VARCHAR(20) | Statut (PASS, FAIL, WARNING) |
| `message` | TEXT | Message détaillé |

---

## 🔗 Relations principales

```
type_donnee → source → flux → document
territoire → document, meteo, indicateur
theme → evenement → document_evenement ← document
pipeline → etape_etl
qc_rule → qc_result ← flux
```

---

## 📊 Statistiques (E1)

- **Total tables** : 18
- **Total contraintes FK** : 15
- **Total index** : 11
- **Tables de référence** : 8 (type_donnee, source, type_meteo, type_indicateur, source_indicateur, theme, qc_rule, utilisateur)
- **Tables métier** : 10 (flux, document, territoire, meteo, indicateur, evenement, document_evenement, pipeline, etape_etl, qc_result)

---

## 🔒 RGPD & Sécurité

- ✅ **Hash SHA-256** : `hash_fingerprint` pour déduplication sans stocker données sensibles
- ✅ **Anonymisation** : Aucune donnée personnelle directe stockée
- ✅ **ON DELETE** : Contraintes CASCADE/SET NULL pour intégrité référentielle
- ✅ **Contraintes CHECK** : Validation des valeurs (fiabilite 0-1, humidite 0-100, etc.)

---

**📝 Note** : Ce dictionnaire est généré depuis le schéma PostgreSQL E1. Pour plus de détails, consulter `docs/e1_schema.sql`.
