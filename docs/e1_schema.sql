-- =====================================================
-- DataSens E1 - Schéma PostgreSQL (18 tables Merise)
-- Export généré depuis notebook 02_schema_create.ipynb
-- =====================================================

-- =====================================================
-- COLLECTE : Type de données, sources, flux
-- =====================================================

CREATE TABLE IF NOT EXISTS type_donnee (
  id_type_donnee SERIAL PRIMARY KEY,
  libelle VARCHAR(100) NOT NULL UNIQUE,
  description TEXT
);

CREATE TABLE IF NOT EXISTS source (
  id_source SERIAL PRIMARY KEY,
  id_type_donnee INT REFERENCES type_donnee(id_type_donnee) ON DELETE RESTRICT,
  nom VARCHAR(100) NOT NULL,
  url TEXT,
  fiabilite FLOAT CHECK (fiabilite >= 0 AND fiabilite <= 1)
);

CREATE TABLE IF NOT EXISTS flux (
  id_flux SERIAL PRIMARY KEY,
  id_source INT NOT NULL REFERENCES source(id_source) ON DELETE CASCADE,
  date_collecte TIMESTAMP NOT NULL DEFAULT NOW(),
  format VARCHAR(20),
  manifest_uri TEXT
);

-- =====================================================
-- CORPUS : Documents et territoires
-- =====================================================

CREATE TABLE IF NOT EXISTS territoire (
  id_territoire SERIAL PRIMARY KEY,
  ville VARCHAR(120),
  code_insee VARCHAR(10),
  lat FLOAT,
  lon FLOAT,
  CONSTRAINT unique_code_insee UNIQUE (code_insee)
);

CREATE TABLE IF NOT EXISTS document (
  id_doc SERIAL PRIMARY KEY,
  id_flux INT REFERENCES flux(id_flux) ON DELETE SET NULL,
  id_territoire INT REFERENCES territoire(id_territoire) ON DELETE SET NULL,
  titre TEXT,
  texte TEXT,
  langue VARCHAR(10),
  date_publication TIMESTAMP,
  hash_fingerprint VARCHAR(64) UNIQUE
);

-- =====================================================
-- CONTEXTE : Météo et indicateurs
-- =====================================================

CREATE TABLE IF NOT EXISTS type_meteo (
  id_type_meteo SERIAL PRIMARY KEY,
  code VARCHAR(20) UNIQUE NOT NULL,
  libelle VARCHAR(100) NOT NULL
);

CREATE TABLE IF NOT EXISTS meteo (
  id_meteo SERIAL PRIMARY KEY,
  id_territoire INT NOT NULL REFERENCES territoire(id_territoire) ON DELETE CASCADE,
  id_type_meteo INT REFERENCES type_meteo(id_type_meteo) ON DELETE SET NULL,
  date_obs TIMESTAMP NOT NULL,
  temperature FLOAT,
  humidite FLOAT CHECK (humidite >= 0 AND humidite <= 100),
  vent_kmh FLOAT CHECK (vent_kmh >= 0),
  pression FLOAT CHECK (pression > 0),
  meteo_type VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS type_indicateur (
  id_type_indic SERIAL PRIMARY KEY,
  code VARCHAR(50) UNIQUE NOT NULL,
  libelle VARCHAR(100),
  unite VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS source_indicateur (
  id_source_indic SERIAL PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  url TEXT
);

CREATE TABLE IF NOT EXISTS indicateur (
  id_indic SERIAL PRIMARY KEY,
  id_territoire INT NOT NULL REFERENCES territoire(id_territoire) ON DELETE CASCADE,
  id_type_indic INT NOT NULL REFERENCES type_indicateur(id_type_indic) ON DELETE RESTRICT,
  id_source_indic INT REFERENCES source_indicateur(id_source_indic) ON DELETE SET NULL,
  valeur FLOAT,
  annee INT CHECK (annee >= 1900 AND annee <= 2100)
);

-- =====================================================
-- THÈMES/ÉVÉNEMENTS
-- =====================================================

CREATE TABLE IF NOT EXISTS theme (
  id_theme SERIAL PRIMARY KEY,
  libelle VARCHAR(100) NOT NULL,
  description TEXT
);

CREATE TABLE IF NOT EXISTS evenement (
  id_event SERIAL PRIMARY KEY,
  id_theme INT REFERENCES theme(id_theme) ON DELETE SET NULL,
  date_event TIMESTAMP,
  avg_tone FLOAT CHECK (avg_tone >= -100 AND avg_tone <= 100),
  source_event VARCHAR(50)
);

CREATE TABLE IF NOT EXISTS document_evenement (
  id_doc INT NOT NULL REFERENCES document(id_doc) ON DELETE CASCADE,
  id_event INT NOT NULL REFERENCES evenement(id_event) ON DELETE CASCADE,
  PRIMARY KEY (id_doc, id_event)
);

-- =====================================================
-- GOUVERNANCE PIPELINE
-- =====================================================

CREATE TABLE IF NOT EXISTS pipeline (
  id_pipeline SERIAL PRIMARY KEY,
  nom VARCHAR(100) NOT NULL,
  description TEXT,
  version VARCHAR(20)
);

CREATE TABLE IF NOT EXISTS etape_etl (
  id_etape SERIAL PRIMARY KEY,
  id_pipeline INT NOT NULL REFERENCES pipeline(id_pipeline) ON DELETE CASCADE,
  ordre INT NOT NULL CHECK (ordre > 0),
  nom_etape VARCHAR(100) NOT NULL,
  type_etape VARCHAR(20) CHECK (type_etape IN ('EXTRACT', 'TRANSFORM', 'LOAD')),
  description TEXT,
  CONSTRAINT unique_pipeline_ordre UNIQUE (id_pipeline, ordre)
);

-- =====================================================
-- UTILISATEURS (trace)
-- =====================================================

CREATE TABLE IF NOT EXISTS utilisateur (
  id_user SERIAL PRIMARY KEY,
  nom VARCHAR(100),
  role VARCHAR(50),
  organisation VARCHAR(100),
  date_creation TIMESTAMP DEFAULT NOW()
);

-- =====================================================
-- QUALITÉ (min)
-- =====================================================

CREATE TABLE IF NOT EXISTS qc_rule (
  id_qc_rule SERIAL PRIMARY KEY,
  nom_regle VARCHAR(100) NOT NULL,
  description TEXT,
  expression_sql TEXT
);

CREATE TABLE IF NOT EXISTS qc_result (
  id_qc_result SERIAL PRIMARY KEY,
  id_qc_rule INT REFERENCES qc_rule(id_qc_rule) ON DELETE CASCADE,
  id_flux INT REFERENCES flux(id_flux) ON DELETE CASCADE,
  date_check TIMESTAMP DEFAULT NOW(),
  statut VARCHAR(20) CHECK (statut IN ('PASS', 'FAIL', 'WARNING')),
  message TEXT
);

-- =====================================================
-- INDEX pour performance
-- =====================================================

-- Index sur hash_fingerprint pour déduplication rapide
CREATE INDEX IF NOT EXISTS idx_document_hash_fingerprint ON document(hash_fingerprint);

-- Index sur dates pour requêtes temporelles
CREATE INDEX IF NOT EXISTS idx_document_date_publication ON document(date_publication);
CREATE INDEX IF NOT EXISTS idx_flux_date_collecte ON flux(date_collecte);
CREATE INDEX IF NOT EXISTS idx_meteo_date_obs ON meteo(date_obs);
CREATE INDEX IF NOT EXISTS idx_evenement_date_event ON evenement(date_event);

-- Index sur clés étrangères fréquentes
CREATE INDEX IF NOT EXISTS idx_document_id_flux ON document(id_flux);
CREATE INDEX IF NOT EXISTS idx_document_id_territoire ON document(id_territoire);
CREATE INDEX IF NOT EXISTS idx_flux_id_source ON flux(id_source);
CREATE INDEX IF NOT EXISTS idx_meteo_id_territoire ON meteo(id_territoire);
CREATE INDEX IF NOT EXISTS idx_indicateur_id_territoire ON indicateur(id_territoire);

-- Index composite pour recherche par territoire + date
CREATE INDEX IF NOT EXISTS idx_meteo_territoire_date ON meteo(id_territoire, date_obs DESC);

