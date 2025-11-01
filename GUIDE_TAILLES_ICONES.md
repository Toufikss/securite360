#  Guide Rapide - Régler la Taille des Icônes

##  **J'ai déjà modifié la taille par défaut !**

**Avant** : 48px → **Maintenant** : 64px (plus grandes automatiquement)

##  **3 Façons de Modifier les Tailles**

### **1.  Fichier de Configuration (RECOMMANDÉ)**

Éditez `utils/icon_sizes.py` pour ajuster les tailles :

```python
# Dans KPI_ICON_SIZES, modifiez les valeurs :
KPI_ICON_SIZES = {
    "score_global": "xxl",          # 96px - Très grande
    "audits": "xl",                 # 80px - Grande  
    "criteres_evalues": "large",    # 64px - Normale
    "documents": "medium",          # 32px - Petite
}
```

**Tailles disponibles :**
- `"tiny"` = 16px
- `"small"` = 24px  
- `"medium"` = 32px
- `"normal"` = 48px
- `"large"` = 64px  (actuel)
- `"xl"` = 80px
- `"xxl"` = 96px

### **2.  Dans le Code Dashboard**

Modifiez directement dans `pages/dashboard.py` :

```python
# Remplacez :
get_kpi_icon("score_global")

# Par :
get_kpi_icon("score_global", "80px")  # Taille spécifique
# ou
get_kpi_icon("score_global", "xl")    # Taille nommée
```

### **3.  Interface Graphique**

Lancez l'interface de configuration :

```bash
streamlit run demo_tailles_icones.py
```

##  **Exemples Pratiques**

### Pour des Icônes Plus Grandes Partout
```python
# Dans utils/icon_sizes.py
def set_all_kpi_size("xl")  # Toutes en 80px
```

### Configuration par Importance
```python
# Score principal = très grand
KPI_ICON_SIZES["score_global"] = "xxl"  # 96px

# KPI importants = grands  
KPI_ICON_SIZES["audits"] = "xl"         # 80px

# Autres = normaux
KPI_ICON_SIZES["documents"] = "large"   # 64px
```

### Tailles Personnalisées
```python
# Ajouter vos propres tailles dans ICON_SIZES
ICON_SIZES["mega"] = "120px"

# L'utiliser
KPI_ICON_SIZES["score_global"] = "mega"
```

##  **Configuration Rapide**

### Profil "Grandes Icônes" 
Ajoutez à la fin de `utils/icon_sizes.py` :
```python
# Activer le profil "Grandes icônes"
set_all_kpi_size("xl")  # Toutes en 80px
```

### Profil "Impact Visuel"
```python
# Score très visible
KPI_ICON_SIZES["score_global"] = "xxl"      # 96px
KPI_ICON_SIZES["audits"] = "xl"             # 80px  
KPI_ICON_SIZES["criteres_evalues"] = "xl"   # 80px
# Autres restent à 64px
```

##  **Résultat Immédiat**

 **Déjà fait** : Taille par défaut passée de 48px → 64px

Pour tester, rechargez votre dashboard :
```bash
streamlit run app.py
```

Les icônes KPI seront automatiquement plus grandes ! 

##  **Quelle Option Choisir ?**

-  **Option 1** (Fichier config) = Facile, centralisé, professionnel
-  **Option 2** (Dans le code) = Contrôle précis par icône
-  **Option 3** (Interface) = Visuel, pour tester rapidement

**Recommandation** : Utilisez l'**Option 1** en éditant `utils/icon_sizes.py` pour définir vos tailles préférées, puis l'**Option 3** pour tester visuellement.

