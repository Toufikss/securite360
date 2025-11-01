"""
Démonstration du système de logos - Sécurité 360
Interface pour tester et gérer les logos de l'application
"""

import streamlit as st
from utils.logos import display_logo, get_main_logo, logo_manager
import os

def demo_logos():
    """Démonstration des logos disponibles"""
    
    st.title("🎨 Gestionnaire de logos - Sécurité 360")
    
    # Section 1: Logos disponibles
    st.header("📋 Logos configurés")
    
    available_logos = logo_manager.list_available_logos()
    
    for logo_key, config in available_logos.items():
        col1, col2, col3 = st.columns([1, 2, 2])
        
        with col1:
            st.markdown(f"### {logo_key}")
            # Afficher le logo
            try:
                display_logo(logo_key)
            except Exception as e:
                st.error(f"Erreur: {str(e)}")
        
        with col2:
            st.markdown("**Configuration:**")
            st.write(f"📁 Fichier: `{config['file']}`")
            st.write(f"📏 Largeur: {config['width']}px")
            st.write(f"🏷️ Alt: {config['alt']}")
            
            # Vérifier si le fichier existe
            exists = logo_manager.logo_exists(logo_key)
            status = "✅ Existe" if exists else "❌ Manquant"
            st.write(f"📍 Statut: {status}")
        
        with col3:
            st.markdown("**Fallback:**")
            fallback = config.get('fallback', {})
            st.write(f"Type: {fallback.get('type', 'N/A')}")
            st.write(f"Contenu: `{fallback.get('content', 'N/A')}`")
            
            # Code d'utilisation
            st.code(f'display_logo("{logo_key}")')
        
        st.divider()

def logo_tester():
    """Testeur de logos interactif"""
    
    st.header("🧪 Testeur de logos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Configuration")
        
        # Sélection du logo
        available_logos = list(logo_manager.list_available_logos().keys())
        selected_logo = st.selectbox("Logo à tester", available_logos)
        
        # Taille personnalisée
        use_custom_width = st.checkbox("Taille personnalisée")
        custom_width = None
        if use_custom_width:
            custom_width = st.slider("Largeur (px)", 50, 500, 200)
        
        # Classe CSS personnalisée
        custom_class = st.text_input("Classe CSS (optionnel)", "")
        
        # Styles inline
        custom_style = st.text_area("Styles CSS inline (optionnel)", "")
    
    with col2:
        st.subheader("Aperçu")
        
        # Affichage du logo avec paramètres personnalisés
        try:
            if custom_width or custom_class or custom_style:
                logo_html = logo_manager.get_logo_html(
                    selected_logo,
                    custom_width=custom_width,
                    css_class=custom_class,
                    style=custom_style
                )
                st.markdown(f'<div style="text-align: center; padding: 2rem;">{logo_html}</div>', 
                           unsafe_allow_html=True)
            else:
                display_logo(selected_logo)
            
            # Informations sur le logo
            info = logo_manager.get_logo_info(selected_logo)
            
            with st.expander("ℹ️ Informations détaillées"):
                st.json(info)
                
        except Exception as e:
            st.error(f"Erreur lors de l'affichage: {str(e)}")

def add_custom_logo():
    """Interface pour ajouter un logo personnalisé"""
    
    st.header("➕ Ajouter un logo personnalisé")
    
    with st.form("add_logo_form"):
        st.markdown("### Configuration du nouveau logo")
        
        col1, col2 = st.columns(2)
        
        with col1:
            logo_key = st.text_input("Clé du logo*", 
                                    placeholder="mon_logo", 
                                    help="Identifiant unique (sans espaces)")
            filename = st.text_input("Nom du fichier*", 
                                   placeholder="mon_logo.png",
                                   help="Nom du fichier dans le dossier")
            alt_text = st.text_input("Texte alternatif*", 
                                   placeholder="Mon Super Logo")
        
        with col2:
            width = st.number_input("Largeur par défaut (px)", 
                                  min_value=50, max_value=500, value=200)
            
            fallback_type = st.selectbox("Type de fallback", 
                                       ["text", "css", "emoji"])
            
            if fallback_type == "css":
                fallback_content = st.text_input("Contenu", "LOGO")
                fallback_bg = st.text_input("Background CSS", 
                                          "linear-gradient(135deg, #ff6b6b 0%, #feca57 100%)")
            else:
                fallback_content = st.text_input("Contenu fallback", "🎨" if fallback_type == "emoji" else "LOGO")
                fallback_bg = None
        
        # Aperçu du fallback
        st.markdown("**Aperçu du fallback:**")
        if fallback_type == "css" and fallback_bg:
            fallback_preview = f"""
            <div style="
                width: 60px; height: 60px; 
                background: {fallback_bg}; 
                border-radius: 50%; 
                display: flex; align-items: center; justify-content: center;
                color: white; font-weight: bold; font-size: 14px;
            ">{fallback_content}</div>
            """
            st.markdown(fallback_preview, unsafe_allow_html=True)
        else:
            st.write(fallback_content)
        
        submitted = st.form_submit_button("Ajouter le logo", type="primary")
        
        if submitted and all([logo_key, filename, alt_text]):
            try:
                # Construire la configuration fallback
                if fallback_type == "css":
                    fallback_config = {
                        "type": "css",
                        "content": fallback_content,
                        "background": fallback_bg
                    }
                else:
                    fallback_config = {
                        "type": fallback_type,
                        "content": fallback_content
                    }
                
                # Ajouter le logo
                logo_manager.add_custom_logo(
                    logo_key=logo_key,
                    filename=filename,
                    alt_text=alt_text,
                    width=width,
                    fallback_content=fallback_content
                )
                
                # Mettre à jour la config fallback manuellement
                from utils.logos import LOGOS_CONFIG
                LOGOS_CONFIG[logo_key]["fallback"] = fallback_config
                
                st.success(f"✅ Logo '{logo_key}' ajouté avec succès!")
                
                # Test du logo
                st.markdown("**Test du nouveau logo:**")
                display_logo(logo_key)
                
                # Code d'utilisation
                st.code(f'display_logo("{logo_key}")')
                
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

def logo_management():
    """Outils de gestion des logos"""
    
    st.header("🔧 Gestion des logos")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Actions")
        
        if st.button("🗂️ Précharger tous les logos"):
            with st.spinner("Préchargement..."):
                logo_manager.preload_logos()
            st.success("✅ Logos préchargés en cache!")
        
        if st.button("🧹 Vider le cache"):
            logo_manager.clear_cache()
            st.success("✅ Cache vidé!")
        
        if st.button("🔍 Analyser les fichiers manquants"):
            missing = []
            for logo_key in logo_manager.list_available_logos():
                if not logo_manager.logo_exists(logo_key):
                    missing.append(logo_key)
            
            if missing:
                st.warning(f"Logos manquants: {', '.join(missing)}")
            else:
                st.success("✅ Tous les logos sont présents!")
    
    with col2:
        st.subheader("Statistiques")
        
        # Statistiques générales
        total_logos = len(logo_manager.list_available_logos())
        cache_size = len(logo_manager._logo_cache)
        
        st.metric("Logos configurés", total_logos)
        st.metric("Logos en cache", cache_size)
        
        # Liste des logos existants
        existing_logos = [key for key in logo_manager.list_available_logos() 
                         if logo_manager.logo_exists(key)]
        st.metric("Logos disponibles", len(existing_logos))
    
    # Détail par logo
    st.subheader("📊 Détail par logo")
    
    for logo_key in logo_manager.list_available_logos():
        info = logo_manager.get_logo_info(logo_key)
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.write(f"**{logo_key}**")
        
        with col2:
            status = "✅" if info['exists'] else "❌"
            st.write(f"{status} {info['file']}")
        
        with col3:
            st.write(f"{info['width']}px")
        
        with col4:
            fallback_type = info['fallback'].get('type', 'N/A')
            st.write(f"🔄 {fallback_type}")

def code_examples():
    """Exemples de code pour les logos"""
    
    st.header("💻 Exemples de code")
    
    # Utilisation basique
    st.subheader("Utilisation basique")
    st.code('''
from utils.logos import display_logo, get_main_logo

# Affichage simple
display_logo()                    # Logo principal
display_logo("sidebar")           # Logo sidebar
display_logo("header")            # Logo header

# Avec taille personnalisée  
display_logo("main", width=250)   # Logo plus grand
display_logo("sidebar", width=100) # Logo plus petit
''', language="python")
    
    # Intégration HTML
    st.subheader("Intégration HTML personnalisée")
    st.code('''
from utils.logos import get_main_logo, logo_manager

# Obtenir le HTML du logo
logo_html = get_main_logo(180)

# Intégration dans du HTML custom
st.markdown(f"""
<div class="header-custom">
    {logo_html}
    <h1>Mon Application</h1>
</div>
""", unsafe_allow_html=True)

# Méthode complète avec options
logo_html = logo_manager.get_logo_html(
    "main", 
    custom_width=200,
    css_class="my-logo", 
    style="border-radius: 10px;"
)
''', language="python")
    
    # Migration depuis l'ancien système
    st.subheader("Migration depuis logo.py")
    st.code('''
# Ancien code (logo.py)
from logo import logo_config
logo_config.display_logo()

# Nouveau code - Option 1 (compatible)
from utils.logos import logo_config  # Classe de compatibilité
logo_config.display_logo()

# Nouveau code - Option 2 (recommandé)
from utils.logos import display_logo
display_logo("main")
''', language="python")

if __name__ == "__main__":
    # Interface principale
    st.set_page_config(
        page_title="Gestionnaire de logos - Sécurité 360",
        page_icon="🎨",
        layout="wide"
    )
    
    # CSS personnalisé pour la démo
    st.markdown("""
    <style>
    .demo-container {
        border: 1px solid #e0e0e0;
        border-radius: 10px;
        padding: 1rem;
        margin: 1rem 0;
        background: #f9f9f9;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Onglets principaux
    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "📋 Logos", 
        "🧪 Testeur", 
        "➕ Ajouter", 
        "🔧 Gestion",
        "💻 Code"
    ])
    
    with tab1:
        demo_logos()
    
    with tab2:
        logo_tester()
    
    with tab3:
        add_custom_logo()
    
    with tab4:
        logo_management()
    
    with tab5:
        code_examples()