str# 📋 Instructions pour changer le logo

## 🎯 Étapes pour remplacer le logo :

### 1. Préparer votre logo
- Format : PNG (recommandé pour la transparence)
- Taille optimale : 200-300 pixels de largeur
- Fond transparent de préférence

### 2. Remplacer le fichier
1. **Copiez votre logo PNG** dans le dossier de l'application :
   ```
   c:\Users\Toufikmp3\Desktop\version final iso27001\
   ```

2. **Renommez votre fichier** exactement comme ceci :
   ```
   logo_securite360.png
   ```
   ⚠️ **Important** : Le nom doit être exactement identique !

3. **Remplacez** le fichier existant si demandé

### 3. Redémarrer l'application
- Arrêtez Streamlit (Ctrl+C dans le terminal)
- Relancez avec : `streamlit run app.py`

## 🔧 Configuration avancée (optionnel)

Si vous voulez personnaliser davantage :

### Changer le nom du fichier logo
1. Ouvrez le fichier `logo.py`
2. Modifiez cette ligne :
   ```python
   self.LOGO_FILENAME = "votre_nouveau_nom.png"
   ```

### Ajuster la taille d'affichage
1. Dans le fichier `logo.py`, modifiez :
   ```python
   self.LOGO_WIDTH = 250  # Changez la valeur
   ```

### Modifier les styles CSS
1. Dans le fichier `logo.py`, section `LOGO_STYLES`
2. Personnalisez les effets visuels

## 📁 Structure des fichiers
```
version final iso27001/
├── logo.py                    ← Configuration du logo
├── logo_securite360.png       ← Votre fichier logo
├── auth.py                    ← Page de connexion
└── app.py                     ← Application principale
```

## ✅ Vérification
Après avoir suivi les étapes :
1. La page de connexion devrait afficher votre logo
2. Si le logo n'apparaît pas, vérifiez le nom du fichier
3. Consultez les messages d'erreur dans Streamlit

## 🆘 En cas de problème
- Vérifiez que le fichier PNG n'est pas corrompu
- Assurez-vous que le nom est exactement `logo_securite360.png`
- Vérifiez que le fichier est bien dans le bon dossier
- Redémarrez complètement l'application