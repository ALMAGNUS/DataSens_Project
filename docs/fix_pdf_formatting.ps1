# Script pour améliorer le formatage PDF du guide technique

$file = "GUIDE_TECHNIQUE_JURY.md"
$content = Get-Content $file -Raw -Encoding UTF8

# Remplacer ``` suivi de diagramme par ```text
$content = $content -replace '```(\r?\n┌)', '```text$1'
$content = $content -replace '```(\r?\n│)', '```text$1'

# Ajouter des sauts de page avant chaque PLOT
$content = $content -replace '(?m)^(## PLOT \d+)', '<div class="plot-section"></div>' + "`r`n`r`n" + '$1'

# Ajouter saut de page avant l'annexe
$content = $content -replace '(?m)^(# 📊 ANNEXE)', '<div class="page-break"></div>' + "`r`n`r`n" + '$1'

# Ajouter sauts de page avant sections principales
$content = $content -replace '(?m)^(## 📊 Diagrammes)', '<div class="page-break"></div>' + "`r`n`r`n" + '$1'

# Sauvegarder
$content | Set-Content $file -Encoding UTF8 -NoNewline

Write-Host "Done - Formatage PDF ameliore" -ForegroundColor Green
