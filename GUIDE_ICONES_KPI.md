# Guide d'Utilisation du Système d'Icônes - Sécurité 360

##  Vue d'ensemble

Le système d'icônes de Sécurité 360 permet de gérer facilement les icônes utilisées dans les indicateurs clés de performance (KPI) du tableau de bord.

##  Icônes Actuellement Configurées

### Indicateurs Clés de Performance

| Clé | Fichier | Description | Utilisation |
|-----|---------|-------------|-------------|
| `score_global` | Score_global.png | Score de conformité global | Affichage score principal |
| `audits_realises` | Audits_realises.png | Nombre d'audits réalisés | Compteur d'audits |
| `non_conformites` | Non-conformites.png | Non-conformités détectées | Alerte problèmes |
| `actions_correctives` | Actions_correctives.png | Actions correctives en cours | Suivi des corrections |
| `documents` | Documents.png | Documents ISO 27001 | Gestion documentaire |
| `formations` | Formations.png | Formations sécurité | Suivi formation équipe |
| `incidents` | Incidents.png | Incidents de sécurité | Gestion des incidents |
| `risques` | Risques.png | Analyse des risques | Évaluation des risques |

##  Utilisation dans le Code

### Import du Module
```python
from utils.icons import get_kpi_icon, icon_manager
```

### Utilisation Basique
```python
# Récupérer une icône KPI
icone_html = get_kpi_icon("score_global")

# Afficher dans Streamlit
st.markdown(icone_html, unsafe_allow_html=True)
```

### Utilisation Avancée avec Taille Personnalisée
```python
# Icône avec taille spécifique
icone_html = get_kpi_icon("audits_realises", size="48px")

# Intégration dans du HTML personnalisé
html_card = f"""
<div class="kpi-card">
    {get_kpi_icon("score_global", size="32px")}
    <h3>Score Global</h3>
    <p>85%</p>
</div>
"""
```

### Vérification de Disponibilité
```python
# Vérifier si une icône existe
if icon_manager.icon_exists("kpi", "ma_nouvelle_icone"):
    icone = get_kpi_icon("ma_nouvelle_icone")
else:
    # Utiliser l'icône de fallback
```

##  Structure des Fichiers

```
assets/
└── icone Indicateurs clés de performance/
    ├── Score_global.png
    ├── Audits_realises.png
    ├── Non-conformites.png
    ├── Actions_correctives.png
    ├── Documents.png
    ├── Formations.png
    ├── Incidents.png
    └── Risques.png
```

## ➕ Ajouter une Nouvelle Icône

### 1. Placer le Fichier
- Copiez votre fichier PNG dans le dossier `assets/icone Indicateurs clés de performance/`
- Nommage recommandé : `Ma_nouvelle_icone.png`

### 2. Configurer dans le Code
Éditez le fichier `utils/icons.py` :

```python
# Dans ICONS_CONFIG["kpi"], ajoutez :
"ma_nouvelle_icone": {
    "file": "Ma_nouvelle_icone.png",
    "alt": "Ma Nouvelle Icône",
    "description": "Description de votre nouvelle icône",
    "category": "custom"
}
```

### 3. Utiliser la Nouvelle Icône
```python
# Dans votre code Streamlit
nouvelle_icone = get_kpi_icon("ma_nouvelle_icone")
```

## 🔧 Maintenance et Diagnostics

### Script de Vérification
Utilisez le script de maintenance pour vérifier votre configuration :

```bash
python check_icones.py
```

Ce script va :
-  Vérifier la structure des dossiers
-  Valider les icônes configurées
-  Lister les fichiers disponibles
-  Suggérer des configurations manquantes
-  Tester le chargement des icônes
-  Générer un rapport complet

### Fonctions de Diagnostic
```python
from utils.icons import icon_manager

# Vérifier toutes les icônes
availability = icon_manager.check_icons_availability()

# Obtenir la liste des icônes manquantes
missing = icon_manager.get_missing_icons()
```

##  Personnalisation

### Tailles Recommandées
- **Petite** : `16px` - Pour les listes
- **Moyenne** : `24px` - Usage standard
- **Grande** : `32px` - Titres et KPI
- **Très grande** : `48px` - Éléments principaux

### Couleurs et Style
Les icônes sont affichées avec leurs couleurs originales. Pour appliquer un style CSS :

```python
icone_styled = f"""
<div style="filter: hue-rotate(180deg);">
    {get_kpi_icon("score_global")}
</div>
"""
```

##  Bonnes Pratiques

### Nommage des Fichiers
- Utilisez des noms descriptifs
- Évitez les espaces (utilisez `_`)
- Format PNG recommandé pour la qualité
- Taille optimale : 64x64 à 128x128 pixels

### Performance
- Les icônes sont mises en cache automatiquement
- Évitez les fichiers trop volumineux (>50KB)
- Préférez le PNG au SVG pour la compatibilité

### Fallbacks
- Chaque icône a un emoji de fallback
- Le système bascule automatiquement si le fichier n'existe pas
- Testez régulièrement avec `check_icones.py`

##  Migration et Mise à Jour

### Sauvegarde
Avant de modifier le système :
```bash
# Sauvegarder la configuration actuelle
copy utils\icons.py utils\icons_backup.py
```

### Mise à Jour en Masse
Pour changer toutes les icônes d'un coup :
1. Placez les nouveaux fichiers dans le dossier
2. Mettez à jour `ICONS_CONFIG` avec les nouveaux noms
3. Exécutez `check_icones.py` pour valider

##  Support

En cas de problème :
1. Exécutez `python check_icones.py` pour diagnostiquer
2. Vérifiez que les fichiers PNG existent dans le bon dossier
3. Validez la syntaxe dans `utils/icons.py`
4. Consultez le rapport généré `rapport_icones.md`

---

*Système d'icônes Sécurité 360 - Version 1.0*