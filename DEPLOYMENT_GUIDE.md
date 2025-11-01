#  Guide de Déploiement - Sécurité 360

##  Fichiers nécessaires pour le déploiement

###  Fichiers créés/vérifiés :
- `requirements.txt`  (dépendances Python)
- `runtime.txt`  (version Python 3.11)
- `.streamlit/config.toml`  (configuration Streamlit)
- `check_imports.py`  (vérification des imports)
##  Résolution des erreurs de déploiement

### Erreur: "from database import Database"
Cette erreur survient quand le module `database.py` n'est pas trouvé. 

**Solutions :**
1. **Vérifier la structure des fichiers** dans le repo GitHub
2. **S'assurer que tous les fichiers sont commitées**
3. **Vérifier les imports relatifs**

###  Structure requise :
```
votre-repo/
├── app.py                 # Point d'entrée principal
├── auth.py               # Module d'authentification  
├── database.py           # Module base de données
├── logo.py              # Configuration du logo
├── requirements.txt      # Dépendances Python
├── runtime.txt          # Version Python
├── .streamlit/
│   └── config.toml      # Configuration Streamlit
├── pages/              # Pages de l'application
├── utils/              # Utilitaires
└── logo_securite360.png # Fichier logo
```

##  Déploiement Streamlit Community Cloud

### 1. Préparer le repository GitHub :
```bash
git add .
git commit -m "Correction pour déploiement"
git push origin main
```

### 2. Vérifier sur Streamlit Cloud :
- URL du repo : `https://github.com/votre-username/votre-repo`
- Branche : `main`
- Fichier principal : `app.py`

### 3. Variables d'environnement (si nécessaire) :
Aucune variable spéciale requise pour cette application.

##  Debugging

### Si l'erreur persiste :
1. **Exécuter le vérificateur d'imports :**
   ```bash
   python check_imports.py
   ```

2. **Vérifier les logs de déploiement**
3. **Tester localement :**
   ```bash
   streamlit run app.py
   ```

##  Support
Si le problème persiste, vérifiez :
- Que tous les fichiers Python sont dans la racine
- Que le fichier `requirements.txt` est correct
- Que la version Python est compatible (3.11)