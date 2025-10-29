# 🔄 Architecture Pipeline DataSens E1

**Version** : Alignée avec `notebooks/datasens_E1_v2.ipynb`

---

## 📋 Architecture complète du pipeline

### 🏗️ Stack technique

```
┌─────────────────────────────────────────────────────────┐
│              NOTEBOOKS JUPYTER (Low-code)               │
├─────────────────────────────────────────────────────────┤
│  01_setup_env.ipynb      → Environnement + Git          │
│  02_schema_create.ipynb  → DDL PostgreSQL 18 tables     │
│  03_ingest_sources.ipynb → Ingestion 5 sources          │
│  04_crud_tests.ipynb     → Tests CRUD + QA               │
│  05_snapshot_and_readme.ipynb → Bilan + exports          │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│              INGESTION MULTI-SOURCES                     │
├─────────────────────────────────────────────────────────┤
│  📄 Fichier plat CSV    → Kaggle (50% PG + 50% MinIO)   │
│  🗄️ Base de données     → SQLite Kaggle → PostgreSQL    │
│  🌐 API                 → OpenWeatherMap, NewsAPI, RSS   │
│  🕷️ Web Scraping        → MonAvisCitoyen (dry-run)      │
│  🌍 Big Data            → GDELT GKG (échantillon)       │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│              STOCKAGE DUAL LAYER                         │
├─────────────────────────────────────────────────────────┤
│  ☁️ MinIO DataLake      → Fichiers bruts S3-compatible  │
│  🗄️ PostgreSQL SGBD    → Données structurées Merise     │
└─────────────────────────────────────────────────────────┘
                            ↓
┌─────────────────────────────────────────────────────────┐
│              TRAÇABILITÉ & GOUVERNANCE                    │
├─────────────────────────────────────────────────────────┤
│  📄 Manifests JSON      → data/raw/manifests/            │
│  📝 Logs structurés    → logs/collecte_*.log             │
│  🔗 Flux PostgreSQL     → Table flux (id_source, date)    │
│  🏷️ Git tags            → E1_REAL_YYYYMMDD              │
└─────────────────────────────────────────────────────────┘
```

---

## 🔧 Fonctions helpers centralisées

### Utilitaires générales

```python
def ts() -> str:
    """Timestamp UTC ISO compact (YYYYMMDDTHHMMSSZ)"""
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")

def sha256(s: str) -> str:
    """Hash SHA-256 pour déduplication"""
    return hashlib.sha256(s.encode("utf-8")).hexdigest()
```

### MinIO DataLake

```python
def ensure_bucket(bucket: str = MINIO_BUCKET):
    """Crée le bucket MinIO s'il n'existe pas"""
    if not minio_client.bucket_exists(bucket):
        minio_client.make_bucket(bucket)

def minio_upload(local_path: Path, dest_key: str) -> str:
    """Upload fichier vers MinIO et retourne URI S3"""
    ensure_bucket(MINIO_BUCKET)
    minio_client.fput_object(MINIO_BUCKET, dest_key, str(local_path))
    return f"s3://{MINIO_BUCKET}/{dest_key}"
```

### PostgreSQL helpers

```python
def get_source_id(conn, nom: str) -> int:
    """Récupère l'id_source depuis le nom (avec logging)"""
    logger.info(f"[get_source_id] Recherche source: {nom}")
    result = conn.execute(text("SELECT id_source FROM source WHERE nom = :nom"), {"nom": nom}).fetchone()
    return result[0] if result else None

def create_flux(conn, id_source: int, format_type: str = "csv", manifest_uri: str = None) -> int:
    """Crée un flux et retourne id_flux (traçabilité)"""
    logger.info(f"[create_flux] Création flux pour id_source={id_source}")
    result = conn.execute(text("""
        INSERT INTO flux (id_source, format, manifest_uri)
        VALUES (:id_source, :format, :manifest_uri)
        RETURNING id_flux
    """), {"id_source": id_source, "format": format_type, "manifest_uri": manifest_uri})
    return result.scalar()

def ensure_territoire(conn, ville: str, code_insee: str = None, lat: float = None, lon: float = None) -> int:
    """Crée ou récupère un territoire"""
    result = conn.execute(text("SELECT id_territoire FROM territoire WHERE ville = :ville"), {"ville": ville}).fetchone()
    if result:
        return result[0]
    result = conn.execute(text("""
        INSERT INTO territoire (ville, code_insee, lat, lon)
        VALUES (:ville, :code_insee, :lat, :lon)
        RETURNING id_territoire
    """), {"ville": ville, "code_insee": code_insee, "lat": lat, "lon": lon})
    return result.scalar()

def insert_documents(conn, docs: list) -> int:
    """Insertion batch avec gestion doublons (ON CONFLICT)"""
    logger.info(f"[insert_documents] Insertion de {len(docs)} documents...")
    inserted = 0
    for doc in docs:
        try:
            result = conn.execute(text("""
                INSERT INTO document (id_flux, id_territoire, titre, texte, langue, date_publication, hash_fingerprint)
                VALUES (:id_flux, :id_territoire, :titre, :texte, :langue, :date_publication, :hash_fingerprint)
                ON CONFLICT (hash_fingerprint) DO NOTHING
                RETURNING id_doc
            """), doc)
            if result.scalar():
                inserted += 1
        except Exception as e:
            log_error("insert_documents", e, "Erreur insertion")
    return inserted
```

### Logging

```python
def log_error(source: str, error: Exception, context: str = ""):
    """Log une erreur avec traceback complet"""
    error_msg = f"[{source}] {context}: {error!s}"
    logger.error(error_msg)
    logger.error(f"Traceback:\n{traceback.format_exc()}")
```

---

## 📊 Pattern d'ingestion standard

Pour chaque source, le pattern est :

```python
logger.info("📄 SOURCE X/5 : [Nom source]")
logger.info("=" * 80)

# 1. Collecte
data = collect_from_source()  # API, scraping, CSV...
df = pd.DataFrame(data)

# 2. Préparation (hash, nettoyage)
df["hash_fingerprint"] = df.apply(lambda x: sha256(...), axis=1)
df = df.drop_duplicates(subset=["hash_fingerprint"])

# 3. Sauvegarde locale
local_path = RAW_DIR / "source" / f"source_{ts()}.csv"
df.to_csv(local_path, index=False)

# 4. Upload MinIO (DataLake)
minio_uri = minio_upload(local_path, f"source/{local_path.name}")
logger.info(f"☁️ MinIO : {minio_uri}")

# 5. Insertion PostgreSQL
with engine.begin() as conn:
    id_source = get_source_id(conn, "Source Name")
    if not id_source:
        # Créer la source si elle n'existe pas
        ...
    id_flux = create_flux(conn, id_source, "csv", minio_uri)

    docs = [prepare_document(row, id_flux) for _, row in df.iterrows()]
    inserted = insert_documents(conn, docs)

logger.info(f"✅ {inserted} documents insérés")
```

---

## 🔄 Architecture hybride 50/50 (Kaggle)

**Pattern spécial pour fichier plat** :

```python
# Split 50/50
mid_point = len(df_kaggle) // 2
df_pg = df_kaggle.iloc[:mid_point].copy()  # 50% → PostgreSQL
df_raw = df_kaggle.iloc[mid_point:].copy()  # 50% → MinIO

# Upload 50% vers MinIO
raw_output = RAW_DIR / "kaggle" / f"kaggle_raw_{ts()}.csv"
df_raw.to_csv(raw_output, index=False)
minio_uri = minio_upload(raw_output, f"kaggle/{raw_output.name}")

# Insertion 50% dans PostgreSQL
with engine.begin() as conn:
    id_flux = create_flux(conn, id_source, "csv", minio_uri)
    docs = [prepare_doc(row, id_flux) for _, row in df_pg.iterrows()]
    inserted = insert_documents(conn, docs)
```

---

## 📋 Manifest JSON

**Structure standard** :

```json
{
  "run_id": "20251029T123337Z",
  "timestamp_utc": "2025-10-29T12:33:37Z",
  "notebook_version": "03_ingest_sources.ipynb",
  "sources_ingested": [
    "Kaggle CSV (fichier plat)",
    "Kaggle DB (base de données)",
    "OpenWeatherMap (API)",
    "MonAvisCitoyen (scraping)",
    "GDELT GKG (big data)"
  ],
  "counts": {
    "documents": 25000,
    "flux": 5,
    "sources": 5,
    "meteo": 20,
    "evenements": 57
  },
  "postgres_db": "datasens",
  "minio_bucket": "datasens-raw",
  "raw_data_location": "data/raw",
  "log_file": "logs/collecte_20251029_124242.log"
}
```

**Stockage** :
- Local : `data/raw/manifests/manifest_*.json`
- MinIO : `s3://datasens-raw/manifests/manifest_*.json`

---

## ✅ Checklist conformité pipeline

- [x] Système de logging structuré (logs/ + errors/)
- [x] MinIO DataLake intégré (upload automatique)
- [x] Fonctions helpers centralisées réutilisables
- [x] Architecture hybride 50/50 (PostgreSQL + MinIO)
- [x] Déduplication SHA-256
- [x] Traçabilité complète (flux, manifests, logs)
- [x] RGPD compliant (hash auteurs, pas de données personnelles)

---

**📝 Note** : Ce document décrit l'architecture pipeline conforme au notebook `datasens_E1_v2.ipynb`.
