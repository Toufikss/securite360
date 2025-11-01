# Guide d'utilisation des logos - Sécurité 360

## 📁 Structure des dossiers

```
projet/
├── logo_securite360.png                    # Logo principal
├── icone.ico                              # Favicon
├── assets/logos/                          # Logos supplémentaires (optionnel)
│   ├── logo_compact.png                   # Logo compact
│   └── logo_report.png                    # Logo pour rapports
├── assets/icons/                          # Icônes diverses
└── utils/
    └── logos.py                           # Gestionnaire de logos
```

## 🎯 Utilisation rapide

### Dans votre code Python :

```python
# Import du gestionnaire de logos
from utils.logos import display_logo, get_main_logo, logo_manager

# Affichage simple du logo principal
display_logo()                            # Logo par défaut (main)
display_logo("sidebar")                   # Logo pour sidebar
display_logo("header")                    # Logo compact pour header

# Avec taille personnalisée
display_logo("main", width=250)           # Logo principal plus grand
display_logo("sidebar", width=120)        # Logo sidebar plus petit

# Obtenir le HTML du logo (pour intégration custom)
logo_html = get_main_logo()               # Logo principal
sidebar_html = get_sidebar_logo(100)      # Logo sidebar 100px
```

### Remplacement de l'ancien système :

```python
# Ancien code (logo.py)
from logo import logo_config
logo_config.display_logo()

# Nouveau code (compatible)
from utils.logos import display_logo
display_logo("main")  # Identique au comportement précédent
```

## 🔧 Configuration des logos

### Types de logos disponibles :

1. **`main`** - Logo principal (pages d'accueil, auth)
2. **`sidebar`** - Logo pour barre latérale  
3. **`header`** - Logo compact pour en-têtes
4. **`favicon`** - Icône de l'application
5. **`report`** - Logo pour rapports/exports

### Ajouter un nouveau logo :

1. **Placez le fichier** dans le dossier approprié
2. **Éditez `utils/logos.py`** et ajoutez dans `LOGOS_CONFIG` :

```python
"mon_logo": {
    "file": "mon_fichier.png",
    "alt": "Description du logo", 
    "width": 180,
    "fallback": {
        "type": "css",  # ou "text", "emoji"
        "content": "ML",
        "background": "linear-gradient(135deg, #ff6b6b 0%, #feca57 100%)"
    }
}
```

3. **Utilisez dans votre code** :
```python
display_logo("mon_logo")
# ou
logo_html = logo_manager.get_logo_html("mon_logo", custom_width=200)
```

## 📚 Méthodes disponibles

### `display_logo(logo_key, custom_width, container_class)`
Affiche un logo avec ses styles CSS intégrés.

### `get_main_logo(width)` / `get_sidebar_logo(width)` / `get_header_logo(width)`
Raccourcis pour obtenir les logos principaux.

### `logo_manager.get_logo_html(key, width, css_class, style)`
Méthode complète pour générer le HTML d'un logo.

### `logo_manager.add_custom_logo(key, filename, alt, width, fallback)`
Ajoute un logo personnalisé dynamiquement.

### `logo_manager.list_available_logos()`
Liste tous les logos disponibles.

### `logo_manager.logo_exists(logo_key)`
Vérifie si un fichier logo existe.

### `logo_manager.get_logo_info(logo_key)`
Obtient toutes les informations d'un logo.

## 🎨 Types de fallback

### CSS (Recommandé)
```python
"fallback": {
    "type": "css",
    "content": "S360",
    "background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)"
}
```
Crée un logo circulaire avec dégradé et texte.

### Texte simple
```python
"fallback": {
    "type": "text", 
    "content": "SÉCURITÉ 360"
}
```
Affiche du texte stylisé.

### Emoji
```python
"fallback": {
    "type": "emoji",
    "content": "🔐"
}
```
Utilise un emoji comme logo de secours.

## 🎨 Personnalisation CSS

Les logos génèrent automatiquement des classes CSS :

```css
/* Logo principal */
.logo-main {
    display: flex;
    justify-content: center;
    margin: 1rem 0 2rem 0;
}

.logo-main img:hover {
    transform: scale(1.05);
    filter: drop-shadow(0 6px 12px rgba(0,0,0,0.15));
}

/* Logo sidebar */
.logo-sidebar {
    text-align: center;
    margin: 0.5rem 0 1rem 0;
}

/* Logo header */
.logo-header {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
}
```

## ✅ Bonnes pratiques

### ✅ À faire :
- **Nommage cohérent** : `main`, `sidebar`, `header`, `report`
- **Formats supportés** : PNG (transparent), JPG, SVG, GIF
- **Tailles optimales** :
  - Principal : 200-400px de largeur
  - Sidebar : 100-200px
  - Header : 80-150px
  - Favicon : 32x32px
- **Fallback** pour chaque logo
- **Préchargement** pour de meilleures performances

### ❌ À éviter :
- Fichiers trop volumineux (>200KB par logo)
- Logos sans fallback
- Chemins en dur dans le code
- Noms avec espaces dans les clés

## 🔄 Migration depuis l'ancien système

### Remplacement automatique :

```python
# Ancien (logo.py)
from logo import logo_config
logo_config.display_logo()

# Nouveau (utils/logos.py) - compatible
from utils.logos import logo_config  # Classe de compatibilité
logo_config.display_logo()

# Recommandé
from utils.logos import display_logo
display_logo("main")
```

### Configuration équivalente :

```python
# Ancien logo.py
class LogoConfig:
    LOGO_FILENAME = "logo_securite360.png"
    LOGO_WIDTH = 200

# Nouveau utils/logos.py
LOGOS_CONFIG = {
    "main": {
        "file": "logo_securite360.png",
        "width": 200,
        # ...
    }
}
```

## 🐛 Dépannage

### Logo ne s'affiche pas :
1. Vérifiez que le fichier existe dans le bon dossier
2. Vérifiez les permissions de lecture
3. Vérifiez la configuration dans `LOGOS_CONFIG`
4. Utilisez `logo_manager.get_logo_info("key")` pour debug

### Fallback ne fonctionne pas :
1. Vérifiez la configuration fallback
2. Testez avec différents types (css, text, emoji)
3. Vérifiez les styles CSS

### Performance lente :
1. Utilisez `logo_manager.preload_logos()` au démarrage
2. Optimisez la taille des fichiers
3. Utilisez le cache intégré

## 📝 Exemples complets

### Application complète :

```python
# app.py
from utils.logos import display_logo

# Logo principal dans la page d'accueil
display_logo("main")

# Logo compact dans la sidebar
with st.sidebar:
    display_logo("sidebar", width=120)
```

### HTML personnalisé :

```python
# Intégration dans du HTML custom
from utils.logos import get_main_logo

logo_html = get_main_logo(150)
st.markdown(f"""
<div class="custom-header">
    {logo_html}
    <h1>Mon Application</h1>
</div>
""", unsafe_allow_html=True)
```

### Ajout dynamique :

```python
# Ajouter un nouveau logo
logo_manager.add_custom_logo(
    logo_key="client_logo",
    filename="logo_client.png", 
    alt_text="Logo Client",
    width=180,
    fallback_content="CLIENT"
)

# L'utiliser immédiatement
display_logo("client_logo")
```

### Vérification d'existence :

```python
# Vérifier si un logo existe avant de l'afficher
if logo_manager.logo_exists("main"):
    display_logo("main")
else:
    st.warning("Logo principal manquant")
    
# Ou obtenir des infos complètes
info = logo_manager.get_logo_info("main")
st.json(info)  # Debug
```

## 🚀 Fonctionnalités avancées

### Logos conditionnels :

```python
# Logo différent selon le contexte
if st.session_state.get('theme') == 'dark':
    display_logo("main_dark")
else:
    display_logo("main") 
```

### Multi-tenant :

```python
# Logo selon l'organisation
org_id = st.session_state.get('organization')
display_logo(f"org_{org_id}", width=200)
```

### Cache et performance :

```python
# Précharger au démarrage de l'app
@st.cache_resource
def init_logos():
    logo_manager.preload_logos()
    return logo_manager

logo_mgr = init_logos()
```