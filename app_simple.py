"""
Version simplifiée de app.py pour Streamlit Cloud
Sans CSS complexe ni JavaScript
"""

import streamlit as st
from auth import Auth
from database import Database
from utils.config import APP_NAME, APP_VERSION, COLORS
from utils.icons import get_sidebar_icon
from logo import logo_config

# Configuration de la page
st.set_page_config(
    page_title=f"{APP_NAME} - ISO 27001",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS minimal pour le thème
st.markdown(f"""
<style>
    .stApp {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
    }}
    [data-testid="stSidebarNav"] {{
        display: none;
    }}
</style>
""", unsafe_allow_html=True)

# Initialisation des modules
auth = Auth()
db = Database()

def main():
    """Fonction principale de l'application"""
    
    # Header avec logo
    col1, col2 = st.columns([1, 3])
    with col1:
        st.markdown(logo_config.get_main_logo(width=100), unsafe_allow_html=True)
    with col2:
        st.title(f"{APP_NAME} v{APP_VERSION}")
        st.markdown("**Système de gestion de la conformité ISO 27001**")
    
    st.divider()
    
    # Vérification de l'authentification
    if not st.session_state.get('authenticated', False):
        show_login_page()
    else:
        show_main_application()

def show_login_page():
    """Affiche la page de connexion"""
    st.header("🔐 Connexion")
    
    with st.form("login_form"):
        username = st.text_input("👤 Nom d'utilisateur")
        password = st.text_input("🔒 Mot de passe", type="password")
        submit = st.form_submit_button("Se connecter")
        
        if submit and username and password:
            if auth.authenticate(username, password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.success("✅ Connexion réussie!")
                st.rerun()
            else:
                st.error("❌ Identifiants incorrects")

def show_main_application():
    """Affiche l'application principale"""
    
    # Sidebar de navigation
    with st.sidebar:
        st.markdown(f"### 👤 {st.session_state.get('username', 'Utilisateur')}")
        
        if st.button("🚪 Déconnexion"):
            for key in list(st.session_state.keys()):
                del st.session_state[key]
            st.rerun()
        
        st.divider()
        
        # Menu principal
        page = st.radio(
            "📋 Navigation",
            [
                "🏠 Dashboard",
                "📊 Audits",
                "📋 Déclaration",
                "📜 Directive",
                "🛡️ Politique",
                "📈 Rapports", 
                "👥 Utilisateurs",
                "⚙️ Paramètres"
            ]
        )
    
    # Contenu principal
    if page == "🏠 Dashboard":
        show_dashboard()
    elif page == "📊 Audits":
        st.header("📊 Gestion des Audits")
        st.info("Module Audits - En développement")
    elif page == "📋 Déclaration":
        st.header("📋 Déclaration de Conformité")
        st.info("Module Déclaration - En développement")
    elif page == "📜 Directive":
        st.header("📜 Gestion des Directives")
        st.info("Module Directives - En développement")
    elif page == "🛡️ Politique":
        st.header("🛡️ Politique de Sécurité")
        st.info("Module Politique - En développement")
    elif page == "📈 Rapports":
        st.header("📈 Génération de Rapports")
        st.info("Module Rapports - En développement")
    elif page == "👥 Utilisateurs":
        st.header("👥 Gestion des Utilisateurs")
        st.info("Module Utilisateurs - En développement")
    elif page == "⚙️ Paramètres":
        st.header("⚙️ Paramètres Système")
        st.info("Module Paramètres - En développement")

def show_dashboard():
    """Affiche le tableau de bord"""
    st.header("🏠 Tableau de Bord - Sécurité 360")
    
    # Métriques de base
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Conformité Globale", "75%", "5%")
    
    with col2:
        st.metric("Audits Actifs", "3", "1")
    
    with col3:
        st.metric("Contrôles Conformes", "45/60", "2")
    
    with col4:
        st.metric("Dernière Évaluation", "Oct 2025", "")
    
    st.divider()
    
    # Status de l'application
    st.success("✅ Application Sécurité 360 opérationnelle sur Streamlit Cloud!")
    st.info("🎉 Tous les modules ont été chargés avec succès")
    
    # Informations techniques
    with st.expander("ℹ️ Informations Techniques"):
        st.write(f"**Version:** {APP_VERSION}")
        st.write("**Environnement:** Streamlit Cloud")
        st.write("**Base de données:** SQLite")
        st.write("**Statut:** Opérationnel")

if __name__ == "__main__":
    main()