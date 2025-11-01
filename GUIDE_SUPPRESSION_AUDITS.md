"""
Guide d'utilisation - Suppression d'Audits
Instructions pour utiliser la nouvelle fonctionnalité de suppression
"""

# 🗑️ **Nouvelle Fonctionnalité : Supprimer les Audits**

## ✅ **Ce qui a été ajouté :**

### 1. **Méthode de suppression en base de données**
```python
def delete_audit(self, audit_id: int) -> bool:
    """Supprime un audit par son ID"""
    # Suppression sécurisée avec gestion d'erreur
    # Retourne True si succès, False sinon
```

### 2. **Interface utilisateur dans la page Audits**
- **Bouton "🗑️ Supprimer l'audit"** dans les détails de chaque audit
- **Confirmation de sécurité** avant suppression définitive
- **Messages de feedback** pour informer l'utilisateur du résultat

## 🎯 **Comment utiliser :**

### **Étape 1 : Accéder aux audits**
1. Aller sur la page **"Audits internes"**
2. Dans l'onglet **"📋 Liste des audits"**
3. Cliquer sur **"🔍 Détails de l'audit #X"** pour un audit

### **Étape 2 : Supprimer un audit**
1. Dans les détails de l'audit, cliquer sur **"🗑️ Supprimer l'audit"**
2. Une confirmation apparaît : **"⚠️ Êtes-vous sûr de vouloir supprimer l'audit ?"**
3. Cliquer sur **"✅ Oui, supprimer"** pour confirmer
4. Ou sur **"❌ Annuler"** pour annuler

### **Étape 3 : Vérification**
- ✅ **Succès** : Message "Audit supprimé avec succès!" + rafraîchissement automatique
- ❌ **Erreur** : Message d'erreur si problème technique

## 🔒 **Sécurité et Permissions :**

### **Qui peut supprimer ?**
- ✅ Utilisateurs avec le rôle **"Auditeur"**
- ❌ Autres utilisateurs : bouton non visible

### **Protection contre les suppressions accidentelles :**
- ⚠️ **Double confirmation** obligatoire
- 🔄 **Rafraîchissement automatique** après suppression
- 💾 **Suppression définitive** de la base de données

## 📊 **Impact sur l'application :**

### **Mises à jour automatiques :**
- **Compteur d'audits** : Se met à jour automatiquement
- **Chronologie** : Graphique recalculé sans l'audit supprimé  
- **Statistiques** : Moyennes et tendances recalculées
- **Liste** : L'audit disparaît immédiatement de la liste

### **Données liées :**
- **Suppression propre** : Seul l'audit est supprimé
- **Pas d'impact** sur les autres données (critères, utilisateurs, etc.)

## 🎨 **Interface utilisateur :**

### **Boutons disponibles dans les détails d'un audit :**
```
[📤 Exporter le rapport]  [🗑️ Supprimer l'audit]
```

### **Écran de confirmation :**
```
⚠️ Êtes-vous sûr de vouloir supprimer l'audit "Audit ISO 27001 Q1" ?

[✅ Oui, supprimer]    [❌ Annuler]
```

## 🚀 **Test de la fonctionnalité :**

1. **Créer un audit de test** dans l'onglet "➕ Nouvel audit"
2. **Vérifier qu'il apparaît** dans la liste des audits
3. **Ouvrir ses détails** et tester la suppression
4. **Confirmer** que l'audit a disparu de la liste et des statistiques

## ⚠️ **Important à retenir :**

- ✅ **Suppression définitive** : Pas de corbeille, l'audit est perdu
- ✅ **Confirmation obligatoire** : Impossible de supprimer par accident  
- ✅ **Permissions requises** : Seuls les auditeurs peuvent supprimer
- ✅ **Mise à jour en temps réel** : Interface rafraîchie automatiquement

---

**🎉 Fonctionnalité prête à l'utilisation !**

Vous pouvez maintenant gérer vos audits de manière complète : 
créer, consulter, exporter et **supprimer** en toute sécurité.