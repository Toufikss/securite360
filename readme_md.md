#  Sécurité 360 - Système de Gestion ISO 27001

Application complète de gestion de la conformité ISO 27001, développée avec Streamlit et Python.

##  Description

Sécurité 360 est une solution professionnelle permettant aux organisations de gérer efficacement leur Système de Management de la Sécurité de l'Information (SMSI) selon la norme ISO/IEC 27001:2022.

### Fonctionnalités principales

- ✅ **Gestion complète des 93 critères de l'Annexe A**
- 📊 **Tableaux de bord interactifs** avec indicateurs de conformité
- 🧮 **Planification et suivi des audits internes**
- 📄 **Génération automatique de rapports PDF professionnels**
- 📘 **Gestion de la politique de sécurité** avec historique des versions
- ⚙️ **Directives et mesures de sécurité**
- 👥 **Gestion des utilisateurs** avec contrôle d'accès basé sur les rôles
- 💾 **Sauvegarde et export des données**
- 🎨 **Interface moderne et responsive** avec thème sombre

##  Installation

### Prérequis

- Python 3.11 ou supérieur
- pip (gestionnaire de paquets Python)

### Étapes d'installation

1. **Cloner ou télécharger le projet**

```bash
cd Securite360
```

2. **Installer les dépendances**

```bash
pip install -r requirements.txt
```

3. **Lancer l'application**

```bash
streamlit run app.py
```

4. **Accéder à l'application**

Ouvrez votre navigateur à l'adresse : `http://localhost:8501`

##  Structure du projet

```
Securite360/
│
├── app.py                      # Point d'entrée principal
├── auth.py                     # Authentification
├── database.py                 # Gestion de la base de données
├── requirements.txt            # Dépendances Python
├── README.md                   # Documentation
│
├── utils/                      # Utilitaires
│   ├── pdf_generator.py        # Génération de rapports PDF
│   ├── charts.py               # Graphiques Plotly
│   ├── config.py               # Configuration et constantes
│   └── helpers.py              # Fonctions utilitaires
│
├── pages/                      # Pages de l'application
│   ├── dashboard.py            # Tableau de bord
│   ├── politique.py            # Politique de sécurité
│   ├── declaration.py          # Déclaration d'applicabilité
│   ├── directive.py            # Directives et mesures
│   ├── audits.py               # Gestion des audits
│   ├── rapports.py             # Génération de rapports
│   ├── users.py                # Gestion des utilisateurs
│   └── settings.py             # Paramètres système
│
└── assets/                     # Ressources (logos, etc.)
```

##  Identifiants de test

### Administrateur
- **Identifiant:** `toufiksalah`
- **Mot de passe:** `Admin@2025`
- **Permissions:** Accès complet

### Auditeur
- **Identifiant:** `audit01`
- **Mot de passe:** `Audit@2025`
- **Permissions:** Gestion des audits et critères

### Utilisateur
- **Identifiant:** `user01`
- **Mot de passe:** `User@2025`
- **Permissions:** Consultation uniquement

##  Rôles et permissions

### Admin
- Accès complet à toutes les fonctionnalités
- Gestion des utilisateurs
- Configuration du système
- Création et modification de tous les contenus

### Auditeur
- Création et gestion des audits
- Mise à jour des critères de conformité
- Génération de rapports
- Consultation des tableaux de bord

### Utilisateur
- Consultation des tableaux de bord
- Lecture des rapports et documents
- Accès aux statistiques

##  Fonctionnalités détaillées

### Tableau de bord
- Jauge de conformité globale
- Répartition des statuts par diagramme circulaire
- Analyse par catégorie (Organisationnelle, Personnel, Physique, Technologique)
- Vue radar de conformité
- Derniers audits et points d'attention

### Déclaration d'applicabilité
- Liste complète des 93 critères ISO 27001
- Filtrage par catégorie et statut
- Mise à jour du statut de conformité
- Ajout de commentaires et preuves
- Export CSV

### Politique de sécurité
- Création et gestion de la politique de sécurité
- Versioning des documents
- Historique des modifications
- Template pré-rempli conforme ISO 27001

### Directives et mesures
- Gestion des mesures techniques et organisationnelles
- Évaluation de l'efficacité
- Classification par type
- Analyse graphique

### Audits internes
- Planification des audits
- Suivi des scores
- Chronologie et tendances
- Génération de rapports d'audit
- Checklist intégrée

### Rapports
- Rapport de conformité global (PDF)
- Rapport d'audit individuel (PDF)
- Rapport par catégorie
- Rapport des non-conformités
- Export CSV et Excel

### Gestion des utilisateurs
- Création/modification/suppression de comptes
- Affectation de rôles
- Validation de mot de passe fort
- Historique des connexions

### Paramètres
- Personnalisation de l'apparence
- Configuration de la sécurité
- Sauvegarde et restauration
- Export des données

##  Technologies utilisées

- **Streamlit 1.31** - Framework d'interface utilisateur
- **SQLite3** - Base de données locale
- **Bcrypt** - Hachage sécurisé des mots de passe
- **Plotly** - Graphiques interactifs
- **ReportLab** - Génération de PDF
- **Pandas** - Manipulation de données

##  Conseils d'utilisation

### Premier démarrage
1. Connectez-vous avec le compte administrateur
2. Personnalisez l'apparence (Paramètres > Apparence)
3. Créez les comptes utilisateurs nécessaires
4. Commencez par mettre à jour les critères de conformité

### Workflow recommandé
1. **Évaluation initiale** : Parcourir tous les critères et mettre à jour leur statut
2. **Planification** : Créer un audit pour formaliser l'évaluation
3. **Actions correctives** : Créer des directives pour traiter les non-conformités
4. **Suivi** : Générer des rapports réguliers
5. **Amélioration continue** : Planifier des audits de suivi

### Bonnes pratiques
- Effectuer une sauvegarde hebdomadaire de la base de données
- Mettre à jour régulièrement les critères (au moins trimestriellement)
- Générer des rapports mensuels pour le suivi
- Documenter toutes les actions correctives
- Former régulièrement les utilisateurs

##  Sécurité

- Mots de passe hashés avec Bcrypt
- Contrôle d'accès basé sur les rôles (RBAC)
- Validation de la force des mots de passe
- Session sécurisée
- Aucune donnée sensible en clair

##  Maintenance

### Sauvegarde
La sauvegarde de la base de données peut être effectuée depuis :
**Paramètres > Sauvegarde > Sauvegarder la base de données**

### Mise à jour
Pour mettre à jour l'application :
```bash
git pull origin main
pip install -r requirements.txt --upgrade
streamlit run app.py
```

##  Résolution de problèmes

### L'application ne démarre pas
- Vérifiez que Python 3.11+ est installé
- Vérifiez que toutes les dépendances sont installées
- Supprimez le dossier `__pycache__` et relancez

### Erreur de connexion à la base de données
- Vérifiez que le fichier `securite360.db` existe
- Supprimez-le pour le régénérer automatiquement

### Les graphiques ne s'affichent pas
- Vérifiez que Plotly est correctement installé
- Videz le cache du navigateur

##  Licence

© 2025 Sécurité 360. Tous droits réservés.
Ce logiciel est propriétaire et confidentiel.

##  Développement

Développé pour la sécurité de l'information.

### Améliorations futures prévues
- [ ] Export Excel natif
- [ ] Notifications par email
- [ ] API REST
- [ ] Mode multi-tenant
- [ ] Intégration LDAP/Active Directory
- [ ] Tableau de bord temps réel
- [ ] Mobile app

##  Support

Pour toute question ou problème :
- Email : salah.toufik.staoueli@gmail.com
- Documentation : https://docs.securite360.com

---

**Note :** Cette application est conçue pour Windows avec Python 3.11+. 
Pour d'autres systèmes d'exploitation, des ajustements mineurs peuvent être nécessaires.