"""
Point d'entrée principal de l'application Sécurité 360
Système de gestion de la conformité ISO 27001
"""

import streamlit as st
from auth import Auth
from database import Database
from utils.config import APP_NAME, APP_VERSION, GLOBAL_CSS, COLORS
from utils.icons import get_sidebar_icon
from logo import logo_config

# Configuration de la page
st.set_page_config(
    page_title=f"{APP_NAME} - ISO 27001",
    page_icon="🔐",
    layout="wide",
    initial_sidebar_state="expanded"  # Sidebar toujours ouverte
)

# Appliquer le style CSS global
st.markdown(GLOBAL_CSS, unsafe_allow_html=True)

# CSS pour contrôler la sidebar de manière définitive
st.markdown("""
<style>
    /* Cacher le menu de navigation par défaut de Streamlit */
    [data-testid="stSidebarNav"] {
        display: none !important;
    }
    /* Cacher le lien "Deploy" dans le menu */
    [data-testid="stToolbar"] {
        display: none !important;
    }
    /* Cacher le bouton de réduction/expansion de la sidebar */
    [data-testid="collapsedControl"] {
        display: none !important;
    }
    button[kind="header"] {
        display: none !important;
    }
    /* Forcer la sidebar à toujours être visible et à la bonne largeur */
    section[data-testid="stSidebar"] {
        display: block !important;
        visibility: visible !important;
        width: 21rem !important;
        min-width: 21rem !important;
        max-width: 21rem !important;
        transform: none !important;
        transition: none !important;
    }
    section[data-testid="stSidebar"] > div {
        width: 21rem !important;
        visibility: visible !important;
    }
    /* Empêcher Streamlit de cacher la sidebar */
    section[data-testid="stSidebar"][aria-expanded="false"] {
        display: block !important;
        visibility: visible !important;
    }
    /* Ajuster la marge du contenu principal */
    .main .block-container {
        padding-left: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialisation des modules
auth = Auth()
db = Database()

# Initialisation automatique des données par défaut (pour Streamlit Cloud)
if 'data_initialized' not in st.session_state:
    with st.spinner("🔄 Initialisation de la base de données..."):
        try:
            # Vérifier si des données existent déjà
            conn = db.get_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT COUNT(*) FROM users")
            user_count = cursor.fetchone()[0]
            cursor.execute("SELECT COUNT(*) FROM criteres") 
            criteria_count = cursor.fetchone()[0]
            db._close_conn(conn)
            
            # Initialiser seulement si nécessaire
            if user_count == 0:
                db.init_default_users()
                st.success("✅ Utilisateurs par défaut créés")
            
            if criteria_count == 0:
                db.init_iso_criteria()
                st.success("✅ Critères ISO 27001 initialisés")
            
            st.session_state.data_initialized = True
            st.success("🎉 Base de données initialisée avec succès!")
            
        except Exception as e:
            st.error(f"❌ Erreur lors de l'initialisation: {str(e)}")
            st.session_state.data_initialized = False

def main():
    """Fonction principale de l'application"""
    
    # Vérifier l'authentification
    if not auth.is_authenticated():
        # Sur la page de connexion, masquer complètement la sidebar pour un affichage plein écran
        st.markdown("""
        <style>
            /* MASQUER COMPLÈTEMENT LA SIDEBAR SUR LA PAGE DE CONNEXION */
            section[data-testid="stSidebar"] {
                display: none !important;
                width: 0 !important;
                min-width: 0 !important;
                max-width: 0 !important;
                visibility: hidden !important;
                opacity: 0 !important;
                pointer-events: none !important;
                z-index: -9999 !important;
            }
            
            /* Étendre le contenu principal sur toute la largeur */
            .main .block-container {
                max-width: 100% !important;
                padding-left: 2rem !important;
                padding-right: 2rem !important;
                margin-left: 0 !important;
            }
            
            /* Forcer le conteneur principal à occuper toute la largeur */
            .main {
                margin-left: 0 !important;
                width: 100% !important;
            }
            
            /* Fond sombre pour la page de connexion */
            .stApp {
                background-color: #0f172a !important;
            }
            .main {
                background-color: #0f172a !important;
            }
            
            /* Cacher le header et toolbar */
            header {
                background-color: transparent !important;
                visibility: hidden !important;
            }
            [data-testid="stHeader"] {
                background-color: transparent !important;
                display: none !important;
            }
            .css-18ni7ap {
                display: none !important;
            }
            
            /* Supprimer le padding du haut pour utiliser tout l'espace */
            .block-container {
                padding-top: 1rem !important;
            }
            
            /* Masquer les conteneurs markdown vides ou indésirables */
            div[data-testid="stMarkdown"]:has(div.login-container:empty),
            div[data-testid="stMarkdown"]:empty,
            div[data-testid="stMarkdownContainer"]:has(div.login-container:empty),
            div[data-testid="stMarkdownContainer"]:empty {
                display: none !important;
                visibility: hidden !important;
                height: 0 !important;
                width: 0 !important;
                opacity: 0 !important;
                pointer-events: none !important;
            }
            
            /* Masquer spécifiquement les div login-container vides */
            div.login-container:empty {
                display: none !important;
            }
        </style>
        
        <script>
            // JavaScript pour supprimer complètement la sidebar et les éléments indésirables du DOM
            document.addEventListener('DOMContentLoaded', function() {
                function removeSidebar() {
                    const sidebar = document.querySelector('section[data-testid="stSidebar"]');
                    if (sidebar) {
                        sidebar.remove();
                    }
                }
                
                function removeUnwantedElements() {
                    // Supprimer l'élément spécifique avec la classe login-container vide
                    const unwantedContainers = document.querySelectorAll('div[data-testid="stMarkdown"] div[data-testid="stMarkdownContainer"] div.login-container');
                    unwantedContainers.forEach(function(container) {
                        // Vérifier si le conteneur est vide ou ne contient que des espaces
                        if (!container.innerHTML.trim() || container.innerHTML.trim() === '') {
                            const parentMarkdown = container.closest('div[data-testid="stMarkdown"]');
                            if (parentMarkdown) {
                                parentMarkdown.remove();
                            }
                        }
                    });
                    
                    // Alternative : supprimer tous les éléments stMarkdown vides
                    const emptyMarkdowns = document.querySelectorAll('div[data-testid="stMarkdown"]');
                    emptyMarkdowns.forEach(function(markdown) {
                        const content = markdown.textContent.trim();
                        if (!content || content === '') {
                            markdown.remove();
                        }
                    });
                }
                
                // Supprimer immédiatement
                removeSidebar();
                removeUnwantedElements();
                
                // Observer les changements et supprimer si des éléments réapparaissent
                const observer = new MutationObserver(function(mutations) {
                    mutations.forEach(function(mutation) {
                        mutation.addedNodes.forEach(function(node) {
                            if (node.nodeType === 1 && node.matches) {
                                // Supprimer sidebar si elle réapparaît
                                if (node.matches('section[data-testid="stSidebar"]')) {
                                    node.remove();
                                }
                                // Supprimer les conteneurs markdown vides
                                if (node.matches('div[data-testid="stMarkdown"]') && !node.textContent.trim()) {
                                    node.remove();
                                }
                            }
                        });
                    });
                    
                    // Nettoyer périodiquement
                    removeUnwantedElements();
                });
                
                observer.observe(document.body, { 
                    childList: true, 
                    subtree: true 
                });
                
                // Nettoyer toutes les 500ms pour s'assurer que les éléments indésirables sont supprimés
                setInterval(removeUnwantedElements, 500);
            });
            
            // Fonction de secours si DOMContentLoaded est déjà passé
            if (document.readyState !== 'loading') {
                const sidebar = document.querySelector('section[data-testid="stSidebar"]');
                if (sidebar) {
                    sidebar.remove();
                }
                
                // Supprimer les éléments indésirables
                const unwantedContainers = document.querySelectorAll('div[data-testid="stMarkdown"] div[data-testid="stMarkdownContainer"] div.login-container');
                unwantedContainers.forEach(function(container) {
                    if (!container.innerHTML.trim()) {
                        const parentMarkdown = container.closest('div[data-testid="stMarkdown"]');
                        if (parentMarkdown) {
                            parentMarkdown.remove();
                        }
                    }
                });
            }
        </script>
        """, unsafe_allow_html=True)
        auth.login_page()
        return
    
    # Récupérer l'utilisateur connecté
    user = auth.get_current_user()
    
    # Barre latérale avec logo PNG
    with st.sidebar:
        # CSS pour remonter le logo dans la sidebar
        st.markdown("""
        <style>
            /* Cibler spécifiquement la sidebar */
            section[data-testid="stSidebar"] .logo-container {
                margin-top: -2rem !important;
                margin-bottom: 0.5rem !important;
                padding-top: 0rem !important;
                padding-bottom: 0rem !important;
            }
            
            /* Alternative - cibler tous les éléments du logo dans la sidebar */
            section[data-testid="stSidebar"] .element-container:first-child {
                margin-top: -1rem !important;
            }
            
            /* Réduire l'espace général en haut de la sidebar */
            section[data-testid="stSidebar"] > div:first-child {
                padding-top: 0.5rem !important;
            }
        </style>
        """, unsafe_allow_html=True)
        
        # Affichage du même logo PNG que la page de connexion
        logo_config.display_logo()
        
        # Texte descriptif sous le logo
        st.markdown("""
        <div style="text-align: center; margin: 0.2rem 0 1.5rem 0;">
            <p style="
                color: #E5E7EB; 
                font-size: 1rem; 
                font-weight: 400; 
                margin: 0;
                text-shadow: 0 1px 2px rgba(0,0,0,0.1);
                letter-spacing: 0.5px;
            ">Système de gestion ISO 27001</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Informations utilisateur
        st.markdown(f"""
        <div style="background-color: {COLORS['surface']}; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
            <p style="color: {COLORS['text_secondary']}; font-size: 0.85rem; margin: 0;">Connecté en tant que</p>
            <p style="color: {COLORS['text']}; font-weight: bold; margin: 0.3rem 0;"><strong>{user['username']}</strong></p>
            <p style="color: {COLORS['accent']}; font-size: 0.9rem; margin: 0;">{user['role']}</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Menu de navigation
        # Menu de navigation
        nav_title_html = f"""
        <div style="display: flex; align-items: center; margin-bottom: 1rem;">
            {get_sidebar_icon("navigation", "24px")}
            <h3 style="margin-left: 0.5rem; margin-bottom: 0; color: {COLORS['text']};">Navigation</h3>
        </div>
        """
        st.markdown(nav_title_html, unsafe_allow_html=True)
        
        # Pages avec icônes - approche simplifiée
        if 'current_page' not in st.session_state:
            st.session_state.current_page = "dashboard"
        
        # Liste des pages principales
        main_pages = [
            ("dashboard", "Tableau de bord"),
            ("politique", "Politique de sécurité"),
            ("declaration", "Déclaration d'applicabilité"),
            ("directive", "Directives et mesures"),
            ("audits", "Audits internes"),
            ("rapports", "Rapports"),
        ]
        
        # Afficher les boutons de navigation principales
        for page_id, page_title in main_pages:
            col1, col2 = st.columns([1, 4])
            with col1:
                # Ajouter un padding vertical pour aligner l'icône avec le texte du bouton
                st.markdown(f"""
                <div style="display: flex; align-items: center; height: 40px; justify-content: center;">
                    {get_sidebar_icon(page_id, '20px')}
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button(page_title, key=f"nav-{page_id}", use_container_width=True):
                    st.session_state.current_page = page_id
                    st.rerun()
            
            # Ajouter de l'espace entre chaque fonctionnalité
            st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
        
        # Pages admin si applicable
        if auth.has_role("Admin"):
            st.markdown("---")
            st.markdown("**Administration**")
            
            admin_pages = [
                ("users", "Gestion utilisateurs"),
                ("data_automation", "Automatisation"),
                ("settings", "Paramètres")
            ]
            
            for page_id, page_title in admin_pages:
                col1, col2 = st.columns([1, 4])
                with col1:
                    # Ajouter un padding vertical pour aligner l'icône avec le texte du bouton
                    st.markdown(f"""
                    <div style="display: flex; align-items: center; height: 40px; justify-content: center;">
                        {get_sidebar_icon(page_id, '20px')}
                    </div>
                    """, unsafe_allow_html=True)
                with col2:
                    if st.button(page_title, key=f"nav-{page_id}", use_container_width=True):
                        st.session_state.current_page = page_id
                        st.rerun()
                
                # Ajouter de l'espace entre chaque fonctionnalité
                st.markdown("<div style='margin-bottom: 0.5rem;'></div>", unsafe_allow_html=True)
        
        selected_page_label = st.session_state.current_page
        
        st.markdown("---")
        
        # Bouton de déconnexion
        if st.button("🚪 Déconnexion", use_container_width=True, type="primary"):
            auth.logout()
    
    # Affichage de la page sélectionnée
    current_page = st.session_state.current_page
    
    if current_page == "dashboard":
        from pages import dashboard
        dashboard.show(auth, db)
    elif current_page == "politique":
        from pages import politique
        politique.show(auth, db)
    elif current_page == "declaration":
        from pages import declaration
        declaration.show(auth, db)
    elif current_page == "directive":
        from pages import directive
        directive.show(auth, db)
    elif current_page == "audits":
        from pages import audits
        audits.show(auth, db)
    elif current_page == "rapports":
        from pages import rapports
        rapports.show(auth, db)
    elif current_page == "users" and auth.has_role("Admin"):
        from pages import users
        users.show(auth, db)
    elif current_page == "data_automation" and auth.has_role("Admin"):
        from pages import data_automation
        data_automation.show(auth, db)
    elif current_page == "settings" and auth.has_role("Admin"):
        from pages import settings
        settings.show(auth, db)
    else:
        st.error("Page non trouvée")

if __name__ == "__main__":
    main()