# Instructions pour conversion PDF optimale

## Étapes pour générer un PDF propre depuis GUIDE_TECHNIQUE_JURY.md

### 1. Extensions VS Code recommandées

- **Markdown PDF** (yzane.markdown-pdf) - RECOMMANDÉ
- **Markdown Preview Enhanced** (shd101wyy.markdown-preview-enhanced)

### 2. Configuration Markdown PDF

Créer/éditer `.vscode/settings.json` :

```json
{
  "markdown-pdf.format": "A4",
  "markdown-pdf.displayHeaderFooter": true,
  "markdown-pdf.headerTemplate": "<div style='font-size:9px; margin-left:1cm;'><span class='title'></span></div>",
  "markdown-pdf.footerTemplate": "<div style='font-size:9px; margin:0 auto;'><span class='pageNumber'></span> / <span class='totalPages'></span></div>",
  "markdown-pdf.margin": {
    "top": "2cm",
    "bottom": "2cm",
    "left": "2cm",
    "right": "2cm"
  },
  "markdown-pdf.breaks": true,
  "markdown-pdf.styles": [
    "https://cdnjs.cloudflare.com/ajax/libs/github-markdown-css/5.2.0/github-markdown.min.css"
  ]
}
```

### 3. Modifications manuelles à faire dans GUIDE_TECHNIQUE_JURY.md

#### A. Remplacer tous les ``` de diagrammes par ```text

**Chercher:**
````
```
┌───
````

**Remplacer par:**
````
```text
┌───
````

#### B. Ajouter des sauts de page

**Avant chaque section PLOT, ajouter:**
```html
<div style="page-break-before: always;"></div>

## PLOT X : ...
```

**Avant l'ANNEXE, ajouter:**
```html
<div style="page-break-before: always;"></div>

# 📊 ANNEXE
```

### 4. Rechercher/Remplacer dans VS Code

**Ctrl+H** pour ouvrir Rechercher/Remplacer

**Recherche 1 - Diagrammes:**
- Chercher: `^```\n(┌|│)`
- Remplacer: ` ```text\n$1`
- Activer: Regex (Alt+R)

**Recherche 2 - PLOTS:**
- Chercher: `^(## PLOT \d+)`
- Remplacer: `<div style="page-break-before: always;"></div>\n\n$1`
- Activer: Regex (Alt+R)

**Recherche 3 - ANNEXE:**
- Chercher: `^(# 📊 ANNEXE)`
- Remplacer: `<div style="page-break-before: always;"></div>\n\n$1`
- Activer: Regex (Alt+R)

### 5. Générer le PDF

1. Ouvrir `GUIDE_TECHNIQUE_JURY.md` dans VS Code
2. **Ctrl+Shift+P** → "Markdown PDF: Export (pdf)"
3. Attendredla génération (peut prendre 30-60 secondes)
4. Le PDF sera créé dans le même dossier

### 6. Vérifications après génération

- [ ] Les diagrammes ASCII sont alignés (police monospace)
- [ ] Chaque PLOT commence sur une nouvelle page
- [ ] Les blocs de code ne sont pas coupés entre 2 pages
- [ ] La table des matières fonctionne
- [ ] Numéros de page en bas

### 7. Alternative : Pandoc (ligne de commande)

```powershell
# Installer pandoc
choco install pandoc

# Générer le PDF
pandoc GUIDE_TECHNIQUE_JURY.md -o GUIDE_TECHNIQUE_JURY.pdf --pdf-engine=wkhtmltopdf -V geometry:margin=2cm --toc --toc-depth=3
```

### 8. Alternative : Typora (GUI)

1. Installer Typora (https://typora.io/)
2. Ouvrir GUIDE_TECHNIQUE_JURY.md
3. File → Export → PDF
4. Choisir le thème "GitHub"
5. Activer "Page Break"

## Exemple de résultat attendu

### Page 1
- En-tête
- Titre principal
- Table des matières

### Pages 2-N
- Sections du guide
- Diagrammes bien formatés

### Pages ANNEXE
- Chaque PLOT sur sa propre page
- Code source complet
- Insights clairement visibles

## Troubleshooting

### Les diagrammes sont déformés
→ Utiliser ```text au lieu de ```

### Plots coupés entre pages
→ Ajouter `<div style="page-break-before: always;"></div>` avant chaque PLOT

### Code qui dépasse
→ Réduire la largeur des lignes à max 80 caractères

### Émojis manquants
→ Installer police "Segoe UI Emoji" sur Windows
