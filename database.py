"""
Module de gestion de la base de données SQLite pour Sécurité 360
Gère les utilisateurs, critères ISO 27001, audits et documents
"""

import sqlite3
import bcrypt
import os
from datetime import datetime
from typing import List, Dict, Optional, Tuple

class Database:
    def __init__(self, db_path: str = "securite360.db"):
        """Initialise la connexion à la base de données"""
        self.db_path = db_path
        # connection persistante pour les bases en mémoire
        self._persistent_conn: sqlite3.Connection | None = None
        if self.db_path == ':memory:':
            self._persistent_conn = sqlite3.connect(self.db_path, check_same_thread=False)
            self._persistent_conn.row_factory = sqlite3.Row
        self.init_database()
        
    def get_connection(self) -> sqlite3.Connection:
        """Crée une connexion à la base de données"""
        # Si une connexion persistante a été créée (ex: ':memory:'), la réutiliser
        if self._persistent_conn is not None:
            return self._persistent_conn
        conn = sqlite3.connect(self.db_path, check_same_thread=False)
        conn.row_factory = sqlite3.Row
        return conn

    def _close_conn(self, conn: sqlite3.Connection | None):
        """Ferme la connexion seulement si ce n'est pas la connexion persistante"""
        if conn is None:
            return
        if getattr(self, '_persistent_conn', None) is conn:
            return
        conn.close()
    
    def init_database(self):
        """Initialise les tables de la base de données"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cle = "theme"
        valeur = "sombre"
        cursor.execute("""
    CREATE TABLE IF NOT EXISTS settings (
        cle TEXT PRIMARY KEY,
        valeur TEXT
    )
""")

        cursor.execute("""
            INSERT OR REPLACE INTO settings (cle, valeur)
            VALUES (?, ?)
        """, (cle, valeur))
        conn.commit()
        
        # Table des utilisateurs
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password_hash TEXT NOT NULL,
                role TEXT NOT NULL,
                created_at TEXT NOT NULL,
                last_login TEXT
            )
        """)
        
        # Table des critères ISO 27001
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS criteres (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                code TEXT UNIQUE NOT NULL,
                titre TEXT NOT NULL,
                description TEXT NOT NULL,
                categorie TEXT NOT NULL,
                statut TEXT DEFAULT 'Non conforme',
                commentaire TEXT,
                preuve_path TEXT,
                derniere_maj TEXT
            )
        """)
        
        # Table des audits
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS audits (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                date_audit TEXT NOT NULL,
                auditeur TEXT NOT NULL,
                statut TEXT NOT NULL,
                score REAL,
                rapport_path TEXT,
                commentaires TEXT,
                created_at TEXT NOT NULL
            )
        """)
        
        # Table des documents
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS documents (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                categorie TEXT NOT NULL,
                version TEXT NOT NULL,
                fichier_path TEXT,
                contenu TEXT,
                auteur TEXT NOT NULL,
                date_creation TEXT NOT NULL,
                derniere_modification TEXT
            )
        """)
        
        # Note: la table `settings` est déjà créée ci-dessus; ne pas la recréer (évite doublon)
        
        # Table des directives
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS directives (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                titre TEXT NOT NULL,
                description TEXT NOT NULL,
                type TEXT NOT NULL,
                efficacite TEXT DEFAULT 'Moyenne',
                responsable TEXT,
                date_creation TEXT NOT NULL
            )
        """)

        conn.commit()

        # Initialiser les utilisateurs par défaut (réutilise la même connexion)
        self.init_default_users(conn)

        # Initialiser les critères ISO 27001 (réutilise la même connexion)
        self.init_iso_criteria(conn)

        # Initialiser les paramètres par défaut (réutilise la même connexion)
        self.init_default_settings(conn)

        # Fermer la connexion ouverte pour l'initialisation
        self._close_conn(conn)
    
    def init_default_users(self, conn: sqlite3.Connection = None):
        """Initialise les utilisateurs par défaut

        Si une connexion est fournie, elle est réutilisée (utile pour
        init_database et les bases en mémoire). Si aucune connexion n'est
        fournie, la méthode ouvrira et fermera sa propre connexion.
        """
        own_conn = conn is None
        if own_conn:
            conn = self.get_connection()
        cursor = conn.cursor()
        
        default_users = [
            ("Sécurité360", "Admin@2025", "Admin"),
            ("audit01", "Audit@2025", "Auditeur"),
            ("user01", "User@2025", "Utilisateur")
        ]
        
        for username, password, role in default_users:
            cursor.execute("SELECT id FROM users WHERE username = ?", (username,))
            if not cursor.fetchone():
                password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
                cursor.execute("""
                    INSERT INTO users (username, password_hash, role, created_at)
                    VALUES (?, ?, ?, ?)
                """, (username, password_hash, role, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        # Toujours committer les insertions, pas seulement pour own_conn
        conn.commit()
        
        if own_conn:
            self._close_conn(conn)
    
    def init_iso_criteria(self, conn: sqlite3.Connection = None):
        """Initialise les critères ISO 27001 depuis l'Annexe A

        Même logique de réutilisation de connexion que pour
        `init_default_users`.
        """
        own_conn = conn is None
        if own_conn:
            conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT COUNT(*) FROM criteres")
        if cursor.fetchone()[0] > 0:
            if own_conn:
                self._close_conn(conn)
            return
        
        # Critères organisationnels
        criteres = [
            ("5.1", "Politiques de sécurité", "Une politique de sécurité de l'information doit être définie, approuvée, publiée et communiquée.", "Organisationnelle"),
            ("5.2", "Fonctions et responsabilités", "Les fonctions et responsabilités liées à la sécurité doivent être définies.", "Organisationnelle"),
            ("5.3", "Séparation des tâches", "Les tâches incompatibles doivent être séparées.", "Organisationnelle"),
            ("5.4", "Responsabilités de la direction", "La direction doit exiger l'application des mesures de sécurité.", "Organisationnelle"),
            ("5.5", "Contacts avec les autorités", "Établir et maintenir le contact avec les autorités appropriées.", "Organisationnelle"),
            ("5.6", "Contacts avec groupes d'intérêt", "Maintenir des contacts avec des groupes d'intérêt spécifiques.", "Organisationnelle"),
            ("5.7", "Renseignement sur les menaces", "Collecter et analyser les informations sur les menaces.", "Organisationnelle"),
            ("5.8", "Sécurité dans la gestion de projet", "Intégrer la sécurité à la gestion de projet.", "Organisationnelle"),
            ("5.9", "Inventaire des actifs", "Élaborer et tenir à jour un inventaire des actifs.", "Organisationnelle"),
            ("5.10", "Utilisation correcte des actifs", "Identifier et documenter les règles d'utilisation des actifs.", "Organisationnelle"),
            ("5.11", "Restitution des actifs", "Le personnel doit restituer tous les actifs lors du départ.", "Organisationnelle"),
            ("5.12", "Classification des informations", "Classifier les informations selon les besoins de sécurité.", "Organisationnelle"),
            ("5.13", "Marquage des informations", "Élaborer des procédures de marquage des informations.", "Organisationnelle"),
            ("5.14", "Transfert des informations", "Mettre en place des règles de transfert d'informations.", "Organisationnelle"),
            ("5.15", "Contrôle d'accès", "Définir et mettre en œuvre des règles de contrôle d'accès.", "Organisationnelle"),
            ("5.16", "Gestion des identités", "Gérer le cycle de vie complet des identités.", "Organisationnelle"),
            ("5.17", "Informations d'authentification", "Contrôler l'attribution et la gestion des informations d'authentification.", "Organisationnelle"),
            ("5.18", "Droits d'accès", "Gérer les droits d'accès selon la politique de contrôle d'accès.", "Organisationnelle"),
            ("5.19", "Sécurité avec les fournisseurs", "Gérer les risques associés aux fournisseurs.", "Organisationnelle"),
            ("5.20", "Accords avec les fournisseurs", "Établir des exigences de sécurité avec chaque fournisseur.", "Organisationnelle"),
            ("5.21", "Chaîne d'approvisionnement TIC", "Gérer les risques de la chaîne d'approvisionnement TIC.", "Organisationnelle"),
            ("5.22", "Surveillance des services fournisseurs", "Surveiller et gérer les pratiques de sécurité des fournisseurs.", "Organisationnelle"),
            ("5.23", "Services en nuage", "Établir des processus pour les services en nuage.", "Organisationnelle"),
            ("5.24", "Planification gestion des incidents", "Planifier et préparer la gestion des incidents.", "Organisationnelle"),
            ("5.25", "Évaluation des événements", "Évaluer les événements de sécurité.", "Organisationnelle"),
            ("5.26", "Réponse aux incidents", "Répondre aux incidents selon les procédures.", "Organisationnelle"),
            ("5.27", "Tirer des enseignements", "Utiliser les connaissances des incidents pour améliorer la sécurité.", "Organisationnelle"),
            ("5.28", "Collecte de preuves", "Établir des procédures de collecte de preuves.", "Organisationnelle"),
            ("5.29", "Sécurité pendant perturbation", "Maintenir la sécurité pendant une perturbation.", "Organisationnelle"),
            ("5.30", "Préparation TIC pour continuité", "Planifier la préparation des TIC pour la continuité.", "Organisationnelle"),
            ("5.31", "Exigences légales", "Identifier et respecter les exigences légales.", "Organisationnelle"),
            ("5.32", "Droits de propriété intellectuelle", "Protéger les droits de propriété intellectuelle.", "Organisationnelle"),
            ("5.33", "Protection des enregistrements", "Protéger les enregistrements de la perte et falsification.", "Organisationnelle"),
            ("5.34", "Protection vie privée et DCP", "Respecter les exigences relatives à la vie privée.", "Organisationnelle"),
            ("5.35", "Révision indépendante", "Réviser l'approche de sécurité de manière indépendante.", "Organisationnelle"),
            ("5.36", "Conformité aux politiques", "Vérifier la conformité aux politiques de sécurité.", "Organisationnelle"),
            ("5.37", "Procédures d'exploitation documentées", "Documenter les procédures d'exploitation.", "Organisationnelle"),
            
            # Mesures applicables aux personnes
            ("6.1", "Sélection des candidats", "Vérifier les références des candidats à l'embauche.", "Personnel"),
            ("6.2", "Termes du contrat de travail", "Indiquer les responsabilités de sécurité dans les contrats.", "Personnel"),
            ("6.3", "Sensibilisation et formation", "Former le personnel à la sécurité de l'information.", "Personnel"),
            ("6.4", "Processus disciplinaire", "Formaliser un processus disciplinaire pour violations.", "Personnel"),
            ("6.5", "Responsabilités après départ", "Définir les responsabilités après la fin d'emploi.", "Personnel"),
            ("6.6", "Accords de confidentialité", "Établir des accords de confidentialité.", "Personnel"),
            ("6.7", "Travail à distance", "Mettre en œuvre des mesures pour le travail à distance.", "Personnel"),
            ("6.8", "Déclaration des événements", "Fournir un mécanisme de déclaration des incidents.", "Personnel"),
            
            # Mesures physiques
            ("7.1", "Périmètres de sécurité physique", "Définir des périmètres de sécurité physique.", "Physique"),
            ("7.2", "Entrées physiques", "Protéger les zones sécurisées par des contrôles d'accès.", "Physique"),
            ("7.3", "Sécurisation des bureaux", "Concevoir des mesures de sécurité physique pour les bureaux.", "Physique"),
            ("7.4", "Surveillance sécurité physique", "Surveiller continuellement les locaux.", "Physique"),
            ("7.5", "Protection contre menaces physiques", "Protéger contre les menaces physiques et environnementales.", "Physique"),
            ("7.6", "Travail dans zones sécurisées", "Concevoir des mesures pour le travail en zones sécurisées.", "Physique"),
            ("7.7", "Bureau propre et écran vide", "Appliquer les règles du bureau propre et écran vide.", "Physique"),
            ("7.8", "Emplacement et protection du matériel", "Choisir un emplacement sécurisé pour le matériel.", "Physique"),
            ("7.9", "Sécurité des actifs hors site", "Protéger les actifs hors du site.", "Physique"),
            ("7.10", "Supports de stockage", "Gérer les supports de stockage sur leur cycle de vie.", "Physique"),
            ("7.11", "Services supports", "Protéger contre les coupures de courant et perturbations.", "Physique"),
            ("7.12", "Sécurité du câblage", "Protéger les câbles contre interceptions et dommages.", "Physique"),
            ("7.13", "Maintenance du matériel", "Entretenir correctement le matériel.", "Physique"),
            ("7.14", "Élimination sécurisée du matériel", "Supprimer les données avant élimination du matériel.", "Physique"),
            
            # Mesures technologiques
            ("8.1", "Terminaux finaux des utilisateurs", "Protéger les informations sur les terminaux.", "Technologique"),
            ("8.2", "Droits d'accès privilégiés", "Limiter et gérer les droits privilégiés.", "Technologique"),
            ("8.3", "Restriction d'accès aux informations", "Restreindre l'accès selon la politique.", "Technologique"),
            ("8.4", "Accès aux codes source", "Gérer l'accès au code source de manière appropriée.", "Technologique"),
            ("8.5", "Authentification sécurisée", "Mettre en œuvre l'authentification sécurisée.", "Technologique"),
            ("8.6", "Dimensionnement", "Surveiller et ajuster l'utilisation des ressources.", "Technologique"),
            ("8.7", "Protection contre les malwares", "Protéger contre les programmes malveillants.", "Technologique"),
            ("8.8", "Gestion des vulnérabilités techniques", "Obtenir et gérer les informations sur les vulnérabilités.", "Technologique"),
            ("8.9", "Gestion des configurations", "Définir et surveiller les configurations de sécurité.", "Technologique"),
            ("8.10", "Suppression des informations", "Supprimer les informations lorsqu'elles ne sont plus nécessaires.", "Technologique"),
            ("8.11", "Masquage des données", "Utiliser le masquage des données selon la politique.", "Technologique"),
            ("8.12", "Prévention de la fuite de données", "Appliquer des mesures de prévention de fuite de données.", "Technologique"),
            ("8.13", "Sauvegarde des informations", "Conserver et tester des copies de sauvegarde.", "Technologique"),
            ("8.14", "Redondance des moyens de traitement", "Mettre en œuvre la redondance pour la disponibilité.", "Technologique"),
            ("8.15", "Journalisation", "Générer, conserver et analyser des journaux.", "Technologique"),
            ("8.16", "Activités de surveillance", "Surveiller les systèmes pour détecter les comportements anormaux.", "Technologique"),
            ("8.17", "Synchronisation des horloges", "Synchroniser les horloges des systèmes.", "Technologique"),
            ("8.18", "Programmes utilitaires à privilèges", "Limiter l'utilisation des programmes utilitaires.", "Technologique"),
            ("8.19", "Installation de logiciels", "Gérer l'installation de logiciels de manière sécurisée.", "Technologique"),
            ("8.20", "Sécurité des réseaux", "Sécuriser, gérer et contrôler les réseaux.", "Technologique"),
            ("8.21", "Sécurité des services réseau", "Identifier et surveiller les services réseau.", "Technologique"),
            ("8.22", "Cloisonnement des réseaux", "Cloisonner les groupes de services dans les réseaux.", "Technologique"),
            ("8.23", "Filtrage web", "Gérer l'accès aux sites web externes.", "Technologique"),
            ("8.24", "Utilisation de la cryptographie", "Définir des règles pour l'utilisation de la cryptographie.", "Technologique"),
            ("8.25", "Cycle de vie de développement sécurisé", "Définir des règles pour le développement sécurisé.", "Technologique"),
            ("8.26", "Exigences de sécurité des applications", "Identifier les exigences lors du développement.", "Technologique"),
            ("8.27", "Principes d'ingénierie sécurisée", "Établir des principes d'ingénierie des systèmes sécurisés.", "Technologique"),
            ("8.28", "Codage sécurisé", "Appliquer des principes de codage sécurisé.", "Technologique"),
            ("8.29", "Tests de sécurité", "Définir des processus de tests de sécurité.", "Technologique"),
            ("8.30", "Développement externalisé", "Diriger et vérifier le développement externalisé.", "Technologique"),
            ("8.31", "Séparation des environnements", "Séparer les environnements de développement, test et production.", "Technologique"),
            ("8.32", "Gestion des changements", "Soumettre les changements à des procédures de gestion.", "Technologique"),
            ("8.33", "Informations de test", "Sélectionner et protéger les informations de test.", "Technologique"),
            ("8.34", "Protection pendant tests d'audit", "Planifier les tests d'audit des systèmes opérationnels.", "Technologique"),
        ]
        
        for code, titre, description, categorie in criteres:
            cursor.execute("""
                INSERT INTO criteres (code, titre, description, categorie, statut, derniere_maj)
                VALUES (?, ?, ?, ?, 'Non conforme', ?)
            """, (code, titre, description, categorie, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        
        # Toujours committer les insertions
        conn.commit()
        
        if own_conn:
            self._close_conn(conn)
    
    def init_default_settings(self, conn: sqlite3.Connection = None):
        """Initialise les paramètres par défaut du système

        Peut réutiliser une connexion existante si fournie.
        """
        own_conn = conn is None
        if own_conn:
            conn = self.get_connection()
        cursor = conn.cursor()
        
        default_settings = [
            ("theme_color", "#1e3a8a"),
            ("company_name", "Sécurité 360"),
            ("logo_path", ""),
        ]
        
        for cle, valeur in default_settings:
            cursor.execute("SELECT cle FROM settings WHERE cle = ?", (cle,))
            if not cursor.fetchone():
                cursor.execute("INSERT INTO settings (cle, valeur) VALUES (?, ?)", (cle, valeur))
        
        # Toujours committer les insertions
        conn.commit()
        
        if own_conn:
            self._close_conn(conn)
    
    # Méthodes pour les utilisateurs
    def verify_user(self, username: str, password: str) -> Optional[Dict]:
        """Vérifie les identifiants d'un utilisateur"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        user = cursor.fetchone()
        
        if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
            cursor.execute("""
                UPDATE users SET last_login = ? WHERE id = ?
            """, (datetime.now().strftime('%Y-%m-%d %H:%M:%S'), user['id']))
            conn.commit()
            self._close_conn(conn)
            return dict(user)
        
        conn.close()
        return None
    
    def get_all_users(self) -> List[Dict]:
        """Récupère tous les utilisateurs"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT id, username, role, created_at, last_login FROM users")
        users = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return users
    
    def add_user(self, username: str, password: str, role: str) -> bool:
        """Ajoute un nouvel utilisateur"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
            cursor.execute("""
                INSERT INTO users (username, password_hash, role, created_at)
                VALUES (?, ?, ?, ?)
            """, (username, password_hash, role, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
            conn.commit()
            self._close_conn(conn)
            return True
        except:
            return False
    
    def delete_user(self, user_id: int) -> bool:
        """Supprime un utilisateur"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM users WHERE id = ?", (user_id,))
            conn.commit()
            conn.close()
            return True
        except:
            return False
    
    def get_user_by_id(self, user_id: int) -> Optional[Dict]:
        """Récupère un utilisateur par son ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
            user = cursor.fetchone()
            conn.close()
            return dict(user) if user else None
        except:
            return None
    
    # Méthodes pour les critères ISO
    def get_all_criteres(self) -> List[Dict]:
        """Récupère tous les critères"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM criteres ORDER BY code")
        criteres = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return criteres
    
    def get_critere_by_id(self, critere_id: int) -> Optional[Dict]:
        """Récupère un critère par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM criteres WHERE id = ?", (critere_id,))
        critere = cursor.fetchone()
        conn.close()
        return dict(critere) if critere else None
    
    def update_critere(self, critere_id: int, statut: str, commentaire: str, preuve_path: str = None):
        """Met à jour un critère"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE criteres
            SET statut = ?, commentaire = ?, preuve_path = ?, derniere_maj = ?
            WHERE id = ?
        """, (statut, commentaire, preuve_path, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), critere_id))
        conn.commit()
        conn.close()
    
    def get_conformity_stats(self) -> Dict:
        """Calcule les statistiques de conformité"""
        conn = self.get_connection()
        cursor = conn.cursor()
        
        cursor.execute("SELECT statut, COUNT(*) as count FROM criteres GROUP BY statut")
        stats = {row['statut']: row['count'] for row in cursor.fetchall()}
        
        cursor.execute("SELECT COUNT(*) as total FROM criteres")
        total = cursor.fetchone()['total']
        
        conn.close()
        
        # Calculer le taux de conformité avec pondération
        conforme = stats.get('Conforme', 0)
        largement_conforme = stats.get('Largement conforme', 0)
        partiellement_conforme = stats.get('Partiellement conforme', 0)
        faiblement_conforme = stats.get('Faiblement conforme', 0)
        non_conforme = stats.get('Non conforme', 0)
        
        # Pondération: Conforme=100%, Largement=80%, Partiellement=50%, Faiblement=30%, Non=0%
        taux_pondere = (conforme * 100 + largement_conforme * 80 + partiellement_conforme * 50 + faiblement_conforme * 30) / total if total > 0 else 0
        
        return {
            'conforme': conforme,
            'largement_conforme': largement_conforme,
            'partiellement_conforme': partiellement_conforme,
            'faiblement_conforme': faiblement_conforme,
            'non_conforme': non_conforme,
            'total': total,
            'taux_conformite': round(taux_pondere, 2)
        }
    
    # Méthodes pour les audits
    def add_audit(self, titre: str, date_audit: str, auditeur: str, statut: str, score: float, commentaires: str) -> int:
        """Ajoute un nouvel audit"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO audits (titre, date_audit, auditeur, statut, score, commentaires, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, (titre, date_audit, auditeur, statut, score, commentaires, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        audit_id = cursor.lastrowid
        conn.commit()
        conn.close()
        return audit_id
    
    def get_all_audits(self) -> List[Dict]:
        """Récupère tous les audits"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audits ORDER BY date_audit DESC")
        audits = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return audits
    
    def get_audit_by_id(self, audit_id: int) -> Optional[Dict]:
        """Récupère un audit par son ID"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM audits WHERE id = ?", (audit_id,))
        audit = cursor.fetchone()
        conn.close()
        return dict(audit) if audit else None
    
    def delete_audit(self, audit_id: int) -> bool:
        """Supprime un audit par son ID"""
        try:
            conn = self.get_connection()
            cursor = conn.cursor()
            cursor.execute("DELETE FROM audits WHERE id = ?", (audit_id,))
            conn.commit()
            success = cursor.rowcount > 0
            conn.close()
            return success
        except Exception as e:
            print(f"Erreur lors de la suppression de l'audit: {e}")
            return False
    
    # Méthodes pour les documents
    def add_document(self, titre: str, categorie: str, version: str, contenu: str, auteur: str, fichier_path: str = None):
        """Ajoute un nouveau document"""
        conn = self.get_connection()
        cursor = conn.cursor()
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        cursor.execute("""
            INSERT INTO documents (titre, categorie, version, fichier_path, contenu, auteur, date_creation, derniere_modification)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (titre, categorie, version, fichier_path, contenu, auteur, now, now))
        conn.commit()
        conn.close()
    
    def get_documents_by_category(self, categorie: str) -> List[Dict]:
        """Récupère les documents d'une catégorie"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM documents WHERE categorie = ? ORDER BY date_creation DESC", (categorie,))
        docs = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return docs
    
    def update_document(self, doc_id: int, contenu: str, version: str):
        """Met à jour un document"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE documents
            SET contenu = ?, version = ?, derniere_modification = ?
            WHERE id = ?
        """, (contenu, version, datetime.now().strftime('%Y-%m-%d %H:%M:%S'), doc_id))
        conn.commit()
        conn.close()
    
    # Méthodes pour les directives
    def add_directive(self, titre: str, description: str, type_dir: str, efficacite: str, responsable: str):
        """Ajoute une nouvelle directive"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO directives (titre, description, type, efficacite, responsable, date_creation)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (titre, description, type_dir, efficacite, responsable, datetime.now().strftime('%Y-%m-%d %H:%M:%S')))
        conn.commit()
        conn.close()
    
    def get_all_directives(self) -> List[Dict]:
        """Récupère toutes les directives"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM directives ORDER BY date_creation DESC")
        directives = [dict(row) for row in cursor.fetchall()]
        conn.close()
        return directives
    
    def delete_directive(self, directive_id: int):
        """Supprime une directive"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM directives WHERE id = ?", (directive_id,))
        conn.commit()
        conn.close()
    
    # Méthodes pour les paramètres
    def get_setting(self, cle: str) -> Optional[str]:
        """Récupère un paramètre"""
        conn = self.get_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT valeur FROM settings WHERE cle = ?", (cle,))
        result = cursor.fetchone()
        conn.close()
        return result['valeur'] if result else None
    
    def update_setting(self, cle: str, valeur: str):
        """Met à jour un paramètre"""
        conn = self.get_connection()
        cursor = conn.cursor()
        # Utiliser INSERT OR REPLACE pour créer ou mettre à jour la clé
        cursor.execute("""
            INSERT OR REPLACE INTO settings (cle, valeur)
            VALUES (?, ?)
        """, (cle, valeur))
        conn.commit()
        conn.close()
