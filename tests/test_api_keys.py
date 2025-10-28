#!/usr/bin/env python3
"""
Script de validation des clés API - DataSens E1_v2
Teste toutes les APIs avant l'exécution du notebook
"""

import json
import os
import sys
from datetime import UTC, datetime
from pathlib import Path

import psycopg2
import requests
from dotenv import load_dotenv
from minio import Minio

# Charger .env
load_dotenv()

def print_header(title):
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}")

def test_openweathermap():
    """Test OpenWeatherMap API"""
    print("\n🌦️  OpenWeatherMap API")
    api_key = os.getenv("OWM_API_KEY")

    if not api_key:
        print("   ❌ OWM_API_KEY manquante dans .env")
        return False

    try:
        url = "https://api.openweathermap.org/data/2.5/weather"
        params = {
            "q": "Paris,FR",
            "appid": api_key,
            "units": "metric",
            "lang": "fr"
        }
        r = requests.get(url, params=params, timeout=10)

        if r.status_code == 200:
            data = r.json()
            temp = data["main"]["temp"]
            ville = data["name"]
            print(f"   ✅ Clé active | Test : {ville} = {temp}°C")
            return True
        if r.status_code == 401:
            print("   ⏳ Clé en cours d'activation (attendre 10-15 min)")
            print("   💡 Code 401: Invalid API key")
            return False
        print(f"   ❌ Erreur {r.status_code}: {r.text[:100]}")
        return False
    except Exception as e:
        print(f"   ❌ Exception: {e!s}")
        return False

def test_newsapi():
    """Test NewsAPI"""
    print("\n📰 NewsAPI")
    api_key = os.getenv("NEWSAPI_KEY")

    if not api_key:
        print("   ❌ NEWSAPI_KEY manquante dans .env")
        return False

    try:
        url = "https://newsapi.org/v2/top-headlines"
        params = {
            "apiKey": api_key,
            "country": "fr",
            "pageSize": 1
        }
        r = requests.get(url, params=params, timeout=10)

        if r.status_code == 200:
            data = r.json()
            total = data.get("totalResults", 0)
            print(f"   ✅ Clé active | {total} articles disponibles")
            return True
        if r.status_code == 401:
            print("   ❌ Clé invalide (code 401)")
            return False
        if r.status_code == 429:
            print("   ⚠️  Rate limit atteint (quota épuisé)")
            return False
        print(f"   ❌ Erreur {r.status_code}: {r.text[:100]}")
        return False
    except Exception as e:
        print(f"   ❌ Exception: {e!s}")
        return False

def test_kaggle():
    """Test Kaggle credentials"""
    print("\n📊 Kaggle API")
    username = os.getenv("KAGGLE_USERNAME")
    key = os.getenv("KAGGLE_KEY")

    if not username or not key:
        print("   ❌ KAGGLE_USERNAME ou KAGGLE_KEY manquants")
        return False

    # Vérifier si kaggle.json existe
    home_kaggle = Path.home() / ".kaggle" / "kaggle.json"
    project_kaggle = Path("kaggle.json")

    if project_kaggle.exists():
        print("   ✅ kaggle.json trouvé dans le projet")
        with project_kaggle.open() as f:
            data = json.load(f)
            if data.get("username") == username:
                print(f"   ✅ Username OK: {username}")
                return True
            print("   ⚠️  Username mismatch")
            return False
    else:
        print("   ⚠️  kaggle.json non trouvé (mais credentials dans .env)")
        print(f"   💡 Username: {username}")
        return True

def test_postgres():
    """Test PostgreSQL connection"""
    print("\n🗄️  PostgreSQL")
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    db = os.getenv("POSTGRES_DB", "datasens")
    user = os.getenv("POSTGRES_USER", "ds_user")
    password = os.getenv("POSTGRES_PASS", "ds_pass")

    try:
        conn = psycopg2.connect(
            host=host,
            port=port,
            database=db,
            user=user,
            password=password,
            connect_timeout=5
        )
        conn.close()
        print(f"   ✅ Connexion OK | {user}@{host}:{port}/{db}")
        return True
    except ImportError:
        print("   ⚠️  psycopg2 non installé (pip install psycopg2-binary)")
        return False
    except Exception as e:
        print(f"   ❌ Connexion échouée: {e!s}")
        print("   💡 Vérifier que Docker Compose est lancé")
        return False

def test_minio():
    """Test MinIO connection"""
    print("\n☁️  MinIO DataLake")
    endpoint = os.getenv("MINIO_ENDPOINT", "http://localhost:9000")
    access_key = os.getenv("MINIO_ACCESS_KEY", "admin")
    secret_key = os.getenv("MINIO_SECRET_KEY", "admin123")

    try:
        client = Minio(
            endpoint.replace("http://", "").replace("https://", ""),
            access_key=access_key,
            secret_key=secret_key,
            secure=endpoint.startswith("https")
        )
        # Test simple
        buckets = list(client.list_buckets())
        print(f"   ✅ Connexion OK | {len(buckets)} bucket(s)")
        return True
    except ImportError:
        print("   ⚠️  minio non installé (pip install minio)")
        return False
    except Exception as e:
        print(f"   ❌ Connexion échouée: {e!s}")
        print("   💡 Vérifier que Docker Compose est lancé")
        return False

def main():
    print_header("🔍 VALIDATION DES CLÉS API - DataSens E1_v2")
    print(f"📅 {datetime.now(UTC).strftime('%Y-%m-%d %H:%M:%S')}")

    results = {
        "Kaggle": test_kaggle(),
        "PostgreSQL": test_postgres(),
        "MinIO": test_minio(),
        "NewsAPI": test_newsapi(),
        "OpenWeatherMap": test_openweathermap()
    }

    print_header("📊 RÉSUMÉ")

    total = len(results)
    success = sum(1 for v in results.values() if v)

    for service, status in results.items():
        icon = "✅" if status else "❌"
        print(f"   {icon} {service}")

    print(f"\n   Score : {success}/{total} services OK")

    if success == total:
        print("\n   🎉 Toutes les APIs sont prêtes !")
        print("   🚀 Vous pouvez lancer le notebook datasens_E1_v2.ipynb")
        return 0
    print("\n   ⚠️  Certains services ne sont pas prêts")
    if not results["OpenWeatherMap"]:
        print("   ⏳ Attendez 10-15 min pour l'activation OWM")
        print("   🔄 Relancez ce script : python test_api_keys.py")
    return 1

if __name__ == "__main__":
    sys.exit(main())
