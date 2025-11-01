#  Guide d'Automatisation ISO 27001

##  Table des matières
1. [Vue d'ensemble](#vue-densemble)
2. [Interface utilisateur](#interface-utilisateur)
3. [Fonctionnalités principales](#fonctionnalités-principales)
4. [Guide d'utilisation](#guide-dutilisation)
5. [Interprétation des résultats](#interprétation-des-résultats)
6. [Configuration avancée](#configuration-avancée)
7. [Dépannage](#dépannage)

---

##  Vue d'ensemble

La fonctionnalité **Automatisation** de votre système ISO 27001 permet de :

###  Objectifs principaux
- **Collecter automatiquement** les données de sécurité de votre infrastructure
- **Calculer les scores ISO 27001** basés sur des métriques réelles
- **Surveiller en temps réel** l'état de sécurité de votre système
- **Générer des recommandations** automatiques d'amélioration
- **Réduire le travail manuel** d'évaluation de conformité

###  Types de données collectées
- **Sécurité réseau** : Firewall, ports ouverts, connexions actives
- **Sécurité système** : Antivirus, mises à jour, processus, utilisation disque
- **Logs de sécurité** : Tentatives de connexion, événements suspects
- **Métriques système** : CPU, mémoire, performances

---

##  Interface utilisateur

L'interface d'automatisation est organisée en **4 onglets principaux** :

###  Onglet 1 : Collecte automatique
- **Actions de collecte** : Boutons pour lancer les différents types de scan
- **Données temps réel** : Affichage live des métriques de sécurité
- **Scores visuels** : Barres de progression avec codes couleur

###  Onglet 2 : Configuration
- **Sources de données** : Configuration AD, APIs, bases de données
- **Planification** : Fréquence des collectes automatiques
- **Tests de connectivité** : Vérification des connexions systèmes

###  Onglet 3 : Résultats temps réel
- **Comparaison** : Scores manuels vs automatiques
- **Métriques live** : CPU, mémoire, disque, connexions
- **Alertes système** : Notifications en cas de problème

###  Onglet 4 : Logs et historique
- **Historique** : Journal des collectes effectuées
- **Logs détaillés** : Informations techniques complètes
- **Actions** : Nettoyage et export des données

---

##  Fonctionnalités principales

### 1.  Collecte complète automatique
```
Étapes de la collecte :
1. Scan sécurité réseau (firewall, ports)
2. Analyse sécurité système (antivirus, updates)
3. Collecte logs de sécurité
4. Calcul scores de conformité
5. Mise à jour base de données
```

**Résultat** : Tous les critères ISO 27001 mis à jour automatiquement

### 2.  Test de connectivité
Vérifie la disponibilité de :
- **Internet** : Connectivité externe
- **Localhost** : Services locaux (port 80)
- **DNS** : Résolution des noms de domaine

### 3.  Calcul scores automatiques
Évalue **14 catégories ISO 27001** :
- **A.5** Politiques de sécurité
- **A.6** Organisation de la sécurité
- **A.7** Sécurité des ressources humaines
- **A.8** Gestion des actifs
- **A.9** Contrôle d'accès 
- **A.10** Cryptographie
- **A.11** Sécurité physique
- **A.12** Sécurité de l'exploitation 
- **A.13** Sécurité des communications 
- **A.14** Développement sécurisé
- **A.15** Relations avec les fournisseurs
- **A.16** Gestion des incidents
- **A.17** Continuité d'activité
- **A.18** Conformité



---

##  Guide d'utilisation

###  Première utilisation

#### Étape 1 : Accès à l'automatisation
1. Connectez-vous avec un compte **Admin**
2. Cliquez sur ** Automatisation** dans le menu gauche
3. Vous arrivez sur l'onglet "Collecte automatique"

#### Étape 2 : Test initial
1. Cliquez sur ** Test de connectivité**
2. Vérifiez que les connexions sont ✅ (vertes)
3. Si des connexions sont ❌ (rouges), vérifiez votre réseau

#### Étape 3 : Premier calcul
1. Cliquez sur ** Calcul scores automatiques**
2. Attendez la fin du processus (barre de progression)
3. Consultez les résultats affichés

#### Étape 4 : Collecte complète
1. Cliquez sur ** Lancer collecte complète**
2. Suivez la progression (5 étapes)
3. Vérifiez le message de réussite

###  Utilisation régulière

#### Surveillance quotidienne
- **Onglet "Résultats temps réel"** : Vérifiez les métriques système
- **Alertes système** : Consultez les notifications 🚨
- **Graphiques de tendances** : Analysez l'évolution

#### Collecte périodique
- **Hebdomadaire** : Collecte complète recommandée
- **Mensuelle** : Calcul des scores pour rapports
- **En cas d'incident** : Collecte immédiate pour évaluation

---

##  Interprétation des résultats

###  Scores par couleur

| Couleur | Plage | Signification | Action |
|---------|-------|---------------|---------|
| 🟢 Vert | 90-100% | Excellent | Maintenir |
| 🟡 Orange | 70-89% | Bon | Surveiller |
| 🔴 Rouge | 0-69% | À améliorer | Action requise |

###  Métriques système

#### CPU
- **< 70%** :  Normal
- **70-90%** :  Surveillance
- **> 90%** :  Critique

#### Mémoire
- **< 80%** :  Normal
- **80-90%** :  Attention
- **> 90%** :  Critique

#### Disque
- **< 80%** :  Normal
- **80-90%** :  Nettoyage recommandé
- **> 90%** :  Espace critique

### 🛡️ Sécurité réseau

#### Firewall
- **ACTIVE** :  Protection activée
- **INACTIVE** :  Risque élevé
- **UNKNOWN** :  Vérification nécessaire

#### Ports ouverts
- **< 10 ports** :  Faible risque
- **10-20 ports** :  Risque modéré
- **> 20 ports** :  Risque élevé

### 💻 Sécurité système

#### Antivirus
- **ACTIVE** :  Protection activée
- **INACTIVE** :  Vulnérabilité majeure
- **UNKNOWN** :  Vérification manuelle

#### Mises à jour
- **UP_TO_DATE** :  Système à jour
- **Autres** :  Mises à jour nécessaires

---

##  Configuration avancée

###  Active Directory
```
Configuration requise :
- Serveur : ldap://dc.company.com
- Utilisateur : audit@company.com
- Mot de passe : [Sécurisé]
```

**Test** : Bouton "Tester connexion AD"
**Résultat** : Nombre d'utilisateurs trouvés

###  APIs d'entreprise
```
Paramètres :
- Nom : Nom descriptif de l'API
- URL : Point d'accès de l'API
- Token : Clé d'authentification
```

###  Bases de données
```
Types supportés :
- MySQL (port 3306)
- PostgreSQL (port 5432)
- MS SQL Server (port 1433)
- Oracle (port 1521)
```

###  Planification
- **Manuel** : Collecte sur demande uniquement
- **Toutes les heures** : Collecte automatique horaire
- **Quotidien** : Une fois par jour (recommandé)
- **Hebdomadaire** : Une fois par semaine

---

##  Dépannage

###  Erreurs communes

#### "Impossible de collecter les données"
**Causes possibles :**
- Permissions insuffisantes
- Services Windows désactivés
- Antivirus bloquant l'accès

**Solutions :**
1. Exécuter en tant qu'administrateur
2. Vérifier les services Windows
3. Ajouter une exception antivirus

#### "Connexion AD échouée"
**Causes possibles :**
- Serveur AD inaccessible
- Identifiants incorrects
- Port LDAP bloqué

**Solutions :**
1. Vérifier la connectivité réseau
2. Tester les identifiants manuellement
3. Contacter l'administrateur réseau

#### "Scores non calculés"
**Causes possibles :**
- Données insuffisantes
- Erreur de collecte système
- Problème de permissions

**Solutions :**
1. Relancer la collecte complète
2. Vérifier les logs détaillés
3. Redémarrer l'application

### 🔍 Diagnostic

#### Vérifications de base
1. **Test connectivité** : Tous les voyants verts ?
2. **Permissions** : Application lancée en admin ?
3. **Services** : Windows Defender, Firewall actifs ?
4. **Réseau** : Connexion internet stable ?

#### Logs détaillés
Les logs dans l'onglet "Logs et historique" contiennent :
- **INFO** : Informations normales
- **WARN** : Avertissements (non bloquants)
- **ERROR** : Erreurs (action requise)

###  Support

#### Auto-diagnostic
1. Onglet **"Logs et historique"**
2. Consulter les **logs détaillés**
3. Identifier les messages **ERROR** ou **WARN**
4. Appliquer les solutions correspondantes

#### Informations utiles pour le support
- Version du système d'exploitation
- Messages d'erreur exacts
- Contexte d'utilisation (première fois, après changement)
- Logs des 10 dernières minutes

---

##  Bonnes pratiques

###  Planification recommandée
- **Collecte complète** : Hebdomadaire (lundi matin)
- **Calcul scores** : Avant chaque audit/rapport
- **Surveillance temps réel** : Consultation quotidienne
- **Configuration** : Révision trimestrielle

###  Sécurité
- Changer les mots de passe de service régulièrement
- Limiter l'accès aux comptes Admin uniquement
- Surveiller les logs pour détecter les anomalies
- Maintenir les systèmes à jour

###  Utilisation des données
- **Rapports mensuels** : Tendances des scores
- **Audits internes** : Preuves de conformité automatique
- **Amélioration continue** : Suivi des recommandations
- **Tableaux de bord** : Métriques en temps réel

---

##  Conclusion

L'automatisation ISO 27001 vous permet de :
-  **Gagner du temps** sur l'évaluation manuelle
-  **Améliorer la précision** avec des données réelles
-  **Surveiller en continu** votre posture de sécurité
-  **Générer des preuves** pour les audits
-  **Identifier rapidement** les points d'amélioration

**Prochaines étapes** :
1. Configurez vos sources de données
2. Planifiez des collectes régulières  
3. Consultez quotidiennement les métriques
4. Suivez les recommandations automatiques
5. Utilisez les données pour vos rapports de conformité

---

* Dernière mise à jour : 31 octobre 2025*
* Pour plus d'informations, consultez la documentation ISO 27001*