# 🔧 GUIDE RAPIDE - Corriger le formatage PDF

## Problème
Les PLOTS sont de travers dans le PDF car :
1. Les diagrammes ASCII utilisent ``` au lieu de ```text
2. Pas de sauts de page entre les PLOTS
3. Les blocs de code trop longs sont coupés

## Solution EXPRESS (5 minutes)

### ÉTAPE 1 : Rechercher/Remplacer dans VS Code

**Ouvrez GUIDE_TECHNIQUE_JURY.md et appuyez sur `Ctrl+H`**

---

#### Remplacement 1 : Balises de code pour diagrammes

**Rechercher:** (activer Regex avec Alt+R)
```
^```\n┌
```

**Remplacer par:**
```
```text
┌
```

**Cliquez sur:** Remplacer tout (Ctrl+Alt+Enter)

---

#### Remplacement 2 : Sauts de page avant PLOTS

**Rechercher:** (Regex activé)
```
^## PLOT
```

**Remplacer par:**
```
<div style="page-break-before: always;"></div>

## PLOT
```

**Cliquez sur:** Remplacer tout

---

#### Remplacement 3 : Saut de page avant ANNEXE

**Rechercher:** (Regex activé)
```
^# 📊 ANNEXE
```

**Remplacer par:**
```
<div style="page-break-before: always;"></div>

# 📊 ANNEXE
```

**Cliquez sur:** Remplacer

---

### ÉTAPE 2 : Installer extension Markdown PDF

1. **Ctrl+Shift+X** (ouvrir extensions)
2. Chercher: `Markdown PDF`
3. Installer: **Markdown PDF** par `yzane`

---

### ÉTAPE 3 : Générer le PDF

1. **Ctrl+Shift+P** (command palette)
2. Taper: `Markdown PDF: Export (pdf)`
3. Appuyer sur Entrée
4. Attendre 30 secondes
5. Le PDF s'ouvre automatiquement

---

## Résultat attendu

✅ **Chaque PLOT commence sur une nouvelle page**
✅ **Les diagrammes ASCII sont alignés correctement**
✅ **Les blocs de code ne sont pas coupés**
✅ **Le PDF fait environ 60-80 pages**

---

## Vérification rapide

Ouvrez le PDF généré et vérifiez :

- [ ] Page 1 : Titre + Table des matières
- [ ] Pages 2-40 : Contenu principal
- [ ] Pages 41-60 : ANNEXE avec 8 PLOTS séparés
- [ ] Diagrammes ┌──┐ bien alignés
- [ ] Code Python visible (pas tronqué)

---

## Si ça marche pas

### Problème : Diagrammes toujours de travers

**Solution:**
Chercher manuellement chaque bloc qui commence par ┌ ou │ et ajouter `text` après les ```

Exemple:
```
Mauvais:
```
┌─────┐

Bon:
```text
┌─────┐
```

### Problème : PLOTS pas sur pages séparées

**Solution:**
Ajouter manuellement avant chaque `## PLOT X`:

```html
<div style="page-break-before: always;"></div>
```

### Problème : PDF pas généré

**Solution:**
1. Installer Chrome/Chromium (requis pour Markdown PDF)
2. Redémarrer VS Code
3. Réessayer

---

## Commande PowerShell alternative (si manuel trop long)

```powershell
# Copier ce code et exécuter dans PowerShell

cd C:\Users\Utilisateur\Desktop\Datasens_Project\docs

# Backup
Copy-Item GUIDE_TECHNIQUE_JURY.md GUIDE_TECHNIQUE_JURY_backup.md

# Lire le fichier
$content = Get-Content GUIDE_TECHNIQUE_JURY.md -Raw

# Fix 1: Diagrams
$lines = $content -split "`n"
$fixed = @()
for ($i = 0; $i -lt $lines.Count; $i++) {
    if ($lines[$i] -eq '```' -and $i+1 -lt $lines.Count -and $lines[$i+1] -match '^[┌│└]') {
        $fixed += '```text'
    } else {
        $fixed += $lines[$i]
    }
}
$content = $fixed -join "`n"

# Fix 2: Page breaks before PLOTS
$content = $content -replace '(?m)^(## PLOT)', '<div style="page-break-before: always;"></div>`r`n`r`n$1'

# Fix 3: Page break before ANNEXE  
$content = $content -replace '(?m)^(# .{1,5} ANNEXE)', '<div style="page-break-before: always;"></div>`r`n`r`n$1'

# Sauvegarder
$content | Set-Content GUIDE_TECHNIQUE_JURY.md -Encoding UTF8

Write-Host "DONE - Verifiez le fichier" -ForegroundColor Green
```

---

## Contact si problème

Regardez `PDF_FORMATTING_INSTRUCTIONS.md` pour plus de détails.

**Temps estimé:** 5 minutes
**Difficulté:** ⭐⭐☆☆☆ (facile)
