#!/usr/bin/env python3
"""
🔍 Validation rapide du code DataSens avec Ruff
Lance un audit complet et affiche un rapport coloré
"""

import subprocess
import sys
from pathlib import Path


def run_ruff_check():
    """Lance Ruff et retourne les statistiques"""
    print("\n" + "=" * 80)
    print("🔍 AUDIT RUFF - DataSens Code Quality Check")
    print("=" * 80 + "\n")

    project_root = Path(__file__).parent.parent
    folders_to_check = ["scripts", "datasens", "tests"]

    # Vérifier que Ruff est installé
    try:
        subprocess.run(["ruff", "--version"], capture_output=True, check=True)
    except (subprocess.CalledProcessError, FileNotFoundError):
        print("❌ Ruff non installé. Installation en cours...")
        subprocess.run([sys.executable, "-m", "pip", "install", "ruff"], check=True)
        print("✅ Ruff installé !\n")

    # Lancer l'audit
    print("📊 Analyse en cours...\n")
    result = subprocess.run(
        ["ruff", "check", *folders_to_check, "--statistics"],
        check=False, cwd=project_root,
        capture_output=True,
        text=True
    )

    # Afficher résultats
    if result.returncode == 0:
        print("✅ AUCUNE ERREUR DÉTECTÉE - Code parfait ! 🎉")
        print("   Conformité PEP8: 100% ✅")
        return 0
    print("⚠️  Erreurs détectées:\n")
    print(result.stdout)

    # Proposer auto-fix
    print("\n" + "=" * 80)
    response = input("🔧 Appliquer les corrections automatiques ? (o/N): ").lower()
    if response == "o":
        fix_result = subprocess.run(
            ["ruff", "check", *folders_to_check, "--fix"],
            check=False, cwd=project_root
        )
        if fix_result.returncode == 0:
            print("\n✅ Toutes les erreurs ont été corrigées automatiquement !")
            return 0
        print("\n⚠️  Certaines erreurs nécessitent une correction manuelle")
        print("📖 Voir docs/AUDIT_RUFF.md pour les détails")
        return 1
    print("\n📖 Consultez docs/AUDIT_RUFF.md pour les corrections manuelles")
    return 1


if __name__ == "__main__":
    sys.exit(run_ruff_check())
