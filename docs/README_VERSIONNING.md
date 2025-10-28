# 📘 Historique des versions DataSens

## Version 1.1.0 - Migration Code Inline (2025-10-28)

- **2025-10-28 21:06:00 UTC** | `REFACTOR_INLINE` | Migration des 9 collecteurs vers code inline notebook
- **2025-10-28 21:06:00 UTC** | `COLLECTORS_REMOVED` | Suppression datasens/collectors/*.py (9 fichiers)
- **2025-10-28 21:06:00 UTC** | `NOTEBOOK_UPDATED` | Cellule 25: Web scraping inline (Reddit, YouTube, SignalConso, Trustpilot, ViePublique, DataGouv)
- **2025-10-28 21:06:00 UTC** | `TEST_SUCCESS` | Exécution notebook: 86 documents collectés (52 Reddit + 30 YouTube + 4 DataGouv)
- **2025-10-28 21:06:00 UTC** | `DOCS_UPDATED` | README.md + GUIDE_TECHNIQUE_JURY.md: approche pédagogique inline
- **2025-10-28 21:06:00 UTC** | `GIT_COMMIT` | Commit français: "refactor: Migration code inline dans notebook"
- **2025-10-28 21:06:00 UTC** | `GIT_PUSH` | Push origin/main réussi

**Changements majeurs** :
- ✅ Code inline simple et transparent (pas de .py externes)
- ✅ Gestion erreurs robuste (try/except par source)
- ✅ Logs détaillés dans cellules
- ✅ Format unifié: {titre, texte, source_site, url, date_publication, langue}
- ✅ Approche académique pour démonstration jury

---

## Version 1.0.0 - Collecteurs Externes (2025-10-28 13:52)

- **2025-10-28 13:40:43 UTC** | `COLLECTE_JOURNALIERE_INIT` | Démarrage script collecte quotidienne
- **2025-10-28 13:40:44 UTC** | `PG_SNAPSHOT_ERROR` | Error response from daemon: No such container: datasens_project-postgres-1

- **2025-10-28 13:40:44 UTC** | `COLLECTE_JOURNALIERE_FIN` | +25047 nouveaux documents en 24h
- **2025-10-28 13:45:08 UTC** | `PG_SNAPSHOT_ERROR` | Error response from daemon: No such container: datasens_project-postgres-1

- **2025-10-28 13:47:22 UTC** | `COLLECTE_JOURNALIERE_INIT` | Démarrage script collecte quotidienne
- **2025-10-28 13:47:43 UTC** | `COLLECTE_JOURNALIERE_INIT` | Démarrage script collecte quotidienne
- **2025-10-28 13:51:23 UTC** | `COLLECTE_JOURNALIERE_INIT` | Démarrage script collecte quotidienne
- **2025-10-28 13:51:53 UTC** | `PG_SNAPSHOT` | datasens_pg_v20251028_135152.sql — Backup quotidien automatique
- **2025-10-28 13:52:00 UTC** | `COLLECTE_JOURNALIERE_FIN` | +25047 nouveaux documents en 24h

**Ancienne approche** : 9 collecteurs .py dans datasens/collectors/ (supprimés en v1.1.0)
