# Guide d'utilisation des icônes - Sécurité 360

##  Structure des dossiers

```
projet/
├── icone Indicateurs clés de performance/  # Icônes KPI actuelles
│   ├── score global.png
│   ├── critères évalués.png
│   ├── critères a risque.png
│   ├── audits.png
│   ├── évolution semestrielle.png
│   ├── délai moyen.png
│   ├── prochaine échéance.png
│   └── etoile.png
├── assets/icons/                          # Icônes futures (optionnel)
│   ├── system/                           # Icônes système
│   └── custom/                           # Icônes personnalisées
└── utils/
    └── icons.py                          # Gestionnaire d'icônes
```

##  Utilisation rapide

### Dans votre code Python :

```python
# Import du gestionnaire d'icônes
from utils.icons import get_kpi_icon, get_system_icon, icon_manager

# Utilisation simple des icônes KPI
score_icon = get_kpi_icon("score_global")           # Score global
criteres_icon = get_kpi_icon("criteres_evalues")    # Critères évalués
risque_icon = get_kpi_icon("criteres_risque")       # Critères à risque

# Avec taille personnalisée
big_icon = get_kpi_icon("audits", "64px")          # Icône plus grande
small_icon = get_kpi_icon("maturite", "32px")      # Icône plus petite

# Icônes système (si configurées)
success_icon = get_system_icon("success", "20px")
warning_icon = get_system_icon("warning", "20px")
```

### Dans les cartes KPI :

```python
# Ancien code (avec émojis)
display_stat_card("Score global", "75%", "🎯", color)

# Nouveau code (avec icônes)
display_stat_card("Score global", "75%", get_kpi_icon("score_global"), color)
```

##  Configuration des icônes

### Ajouter une nouvelle icône KPI :

1. **Placez le fichier PNG** dans le dossier `icone Indicateurs clés de performance/`
2. **Éditez `utils/icons.py`** et ajoutez dans `ICONS_CONFIG["kpi"]` :

```python
"nouvelle_icone": {
    "file": "mon_fichier.png",
    "alt": "Description de l'icône",
    "fallback": ""  # Emoji de secours
}
```

3. **Utilisez dans votre code** :
```python
mon_icone = get_kpi_icon("nouvelle_icone")
```

### Créer une nouvelle catégorie :

```python
# Dans utils/icons.py, ajoutez à ICONS_CONFIG
"ma_categorie": {
    "mon_icone": {
        "file": "fichier.png",
        "alt": "Ma super icône",
        "fallback": ""
    }
}

# Ajoutez le chemin du dossier
ICONS_PATHS["ma_categorie"] = "mon/dossier/icones"

# Utilisez avec la méthode complète
icone_html = icon_manager.get_icon_html("ma_categorie", "mon_icone", "40px")
```

## 📚 Méthodes disponibles

### `get_kpi_icon(icon_key, size="48px")`
Obtient une icône KPI avec fallback automatique.

### `get_system_icon(icon_key, size="24px")`  
Obtient une icône système.

### `icon_manager.get_icon_html(category, icon_key, size, css_class)`
Méthode complète pour toute icône.

### `icon_manager.add_custom_icon(category, key, filename, alt, fallback)`
Ajoute une icône personnalisée dynamiquement.

### `icon_manager.list_available_icons(category=None)`
Liste toutes les icônes disponibles.

### `icon_manager.preload_icons(category=None)`
Précharge les icônes en mémoire pour de meilleures performances.

##  Personnalisation CSS

Les icônes génèrent automatiquement des classes CSS :

```css
/* Toutes les icônes */
.icon {
    transition: transform 0.2s ease;
}

/* Icônes KPI spécifiquement */
.kpi-icon {
    border-radius: 4px;
    padding: 2px;
}

.kpi-icon:hover {
    transform: scale(1.1);
}

/* Icônes système */
.system-icon {
    vertical-align: middle;
}
```

##  Bonnes pratiques

###  À faire :
- **Nommage cohérent** : Utilisez des clés en snake_case (`score_global`, `criteres_risque`)
- **Tailles standards** : 24px, 32px, 48px, 64px
- **Format PNG** avec fond transparent
- **Couleurs neutres** qui s'adaptent aux thèmes
- **Préchargement** pour les icônes fréquemment utilisées

###  À éviter :
- Fichiers trop volumineux (>50KB par icône)
- Noms avec espaces ou caractères spéciaux dans les clés
- Icônes sans fallback emoji
- Chemins en dur dans le code

##  Migration depuis l'ancien système

### Remplacement automatique :
```python
# Ancien
get_icon_html("score global")

# Nouveau (compatible)
get_icon_html_legacy("score global")  # Fonction de transition

# Recommandé
get_kpi_icon("score_global")
```

##  Dépannage

### Icône ne s'affiche pas :
1. Vérifiez que le fichier existe dans le bon dossier
2. Vérifiez les permissions de lecture
3. Vérifiez la configuration dans `ICONS_CONFIG`
4. Utilisez `icon_manager.list_available_icons()` pour debug

### Performances lentes :
1. Utilisez `icon_manager.preload_icons()` au démarrage
2. Vérifiez la taille des fichiers PNG
3. Activez la mise en cache

### Fallback ne fonctionne pas :
1. Vérifiez que l'emoji fallback est défini
2. Testez avec `get_icon_html_legacy()` pour compatibilité

##  Exemples complets

### Dashboard avec icônes :
```python
from utils.icons import get_kpi_icon

# KPI Cards avec icônes
display_stat_card(
    "Score global ISO 27001",
    f"{stats['taux_conformite']}%",
    get_kpi_icon("score_global"),
    color
)

display_stat_card(
    "Critères évalués", 
    f"{total_criteres}",
    get_kpi_icon("criteres_evalues"),
    COLORS['info']
)
```

### Ajout d'icône personnalisée :
```python
# Ajouter une nouvelle icône
icon_manager.add_custom_icon(
    category="kpi",
    icon_key="nouveau_kpi", 
    filename="mon_kpi.png",
    alt_text="Nouveau KPI",
    fallback=""
)

# L'utiliser immédiatement
nouvelle_icone = get_kpi_icon("nouveau_kpi", "52px")
```