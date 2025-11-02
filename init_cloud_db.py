"""
Script d'initialisation de la base de données pour Streamlit Cloud
Initialise automatiquement les utilisateurs et critères ISO 27001
"""

import streamlit as st
from database import Database

def init_cloud_database():
    """Initialise la base de données sur Streamlit Cloud au premier lancement"""
    
    if 'database_initialized' not in st.session_state:
        st.info("🔄 Initialisation de la base de données pour Streamlit Cloud...")
        
        try:
            db = Database()
            
            # Vérifier si des données existent
            conn = db.get_connection()
            cursor = conn.cursor()
            
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            
            cursor.execute("SELECT COUNT(*) FROM criteres")
            criteria_count = cursor.fetchone()[0]
            
            db._close_conn(conn)
            
            # Messages d'initialisation
            init_messages = []
            
            # Initialiser les utilisateurs si nécessaire
            if user_count == 0:
                db.init_default_users()
                init_messages.append("✅ Utilisateurs par défaut créés")
                st.success("✅ Utilisateurs par défaut créés")
            
            # Initialiser les critères ISO si nécessaire
            if criteria_count == 0:
                db.init_iso_criteria()
                init_messages.append("✅ Critères ISO 27001 initialisés")
                st.success("✅ Critères ISO 27001 initialisés")
            
            # Marquer comme initialisé
            st.session_state.database_initialized = True
            
            if init_messages:
                st.success("🎉 Base de données initialisée avec succès sur Streamlit Cloud!")
                st.info("**Comptes par défaut créés :**\n- **Admin :** Sécurité360 / Admin@2025\n- **Auditeur :** audit01 / Audit@2025\n- **Utilisateur :** user01 / User@2025")
            else:
                st.success("✅ Base de données déjà initialisée")
                
        except Exception as e:
            st.error(f"❌ Erreur lors de l'initialisation : {e}")
            st.session_state.database_initialized = False

def check_and_init_if_needed():
    """Vérifie et initialise la base de données si nécessaire"""
    init_cloud_database()
    return st.session_state.get('database_initialized', False)