"""
Exemple d'utilisation du système d'icônes - Sécurité 360
Ce fichier montre comment utiliser et personnaliser le gestionnaire d'icônes
"""

import streamlit as st
from utils.icons import get_kpi_icon, get_system_icon, icon_manager

def demo_icons():
    """Démonstration du système d'icônes"""
    
    st.title("🎨 Démonstration du système d'icônes")
    
    # Section 1: Icônes KPI existantes
    st.header("📊 Icônes KPI disponibles")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown("**Score Global**")
        st.markdown(get_kpi_icon("score_global"), unsafe_allow_html=True)
        st.code('get_kpi_icon("score_global")')
    
    with col2:
        st.markdown("**Critères Évalués**")
        st.markdown(get_kpi_icon("criteres_evalues"), unsafe_allow_html=True)
        st.code('get_kpi_icon("criteres_evalues")')
    
    with col3:
        st.markdown("**Critères à Risque**")
        st.markdown(get_kpi_icon("criteres_risque"), unsafe_allow_html=True)
        st.code('get_kpi_icon("criteres_risque")')
    
    with col4:
        st.markdown("**Audits**")
        st.markdown(get_kpi_icon("audits"), unsafe_allow_html=True)
        st.code('get_kpi_icon("audits")')
    
    # Section 2: Différentes tailles
    st.header("📏 Différentes tailles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("**Petite (32px)**")
        st.markdown(get_kpi_icon("maturite", "32px"), unsafe_allow_html=True)
    
    with col2:
        st.markdown("**Normale (48px)**")
        st.markdown(get_kpi_icon("maturite", "48px"), unsafe_allow_html=True)
    
    with col3:
        st.markdown("**Grande (64px)**")
        st.markdown(get_kpi_icon("maturite", "64px"), unsafe_allow_html=True)
    
    # Section 3: Liste des icônes disponibles
    st.header("📋 Configuration actuelle")
    
    available_icons = icon_manager.list_available_icons()
    
    for category, icons in available_icons.items():
        st.subheader(f"Catégorie: {category}")
        
        for icon_key, config in icons.items():
            col1, col2, col3 = st.columns([1, 2, 2])
            
            with col1:
                if category == "kpi":
                    st.markdown(get_kpi_icon(icon_key, "32px"), unsafe_allow_html=True)
                else:
                    st.markdown("🔧")  # Placeholder pour autres catégories
            
            with col2:
                st.markdown(f"**{icon_key}**")
                st.markdown(f"Fichier: `{config['file']}`")
            
            with col3:
                st.markdown(f"Alt: {config['alt']}")
                st.markdown(f"Fallback: {config['fallback']}")

def add_custom_icon_demo():
    """Démonstration d'ajout d'icône personnalisée"""
    
    st.header("➕ Ajouter une icône personnalisée")
    
    with st.form("add_icon_form"):
        st.markdown("### Formulaire d'ajout d'icône")
        
        category = st.selectbox("Catégorie", ["kpi", "system", "custom"])
        icon_key = st.text_input("Clé de l'icône", placeholder="ma_nouvelle_icone")
        filename = st.text_input("Nom du fichier", placeholder="mon_fichier.png")
        alt_text = st.text_input("Texte alternatif", placeholder="Description de l'icône")
        fallback = st.text_input("Emoji de fallback", placeholder="📊")
        
        submitted = st.form_submit_button("Ajouter l'icône")
        
        if submitted and all([icon_key, filename, alt_text, fallback]):
            try:
                icon_manager.add_custom_icon(
                    category=category,
                    icon_key=icon_key,
                    filename=filename,
                    alt_text=alt_text,
                    fallback=fallback
                )
                st.success(f"✅ Icône '{icon_key}' ajoutée avec succès!")
                
                # Test de l'icône
                if category == "kpi":
                    test_html = get_kpi_icon(icon_key)
                    st.markdown(f"**Aperçu:** {test_html}", unsafe_allow_html=True)
                    st.code(f'get_kpi_icon("{icon_key}")')
                
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")

def performance_tools():
    """Outils de performance et maintenance"""
    
    st.header("⚡ Outils de performance")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🗂️ Précharger toutes les icônes"):
            with st.spinner("Préchargement en cours..."):
                icon_manager.preload_icons()
            st.success("✅ Icônes préchargées!")
        
        if st.button("🧹 Vider le cache"):
            icon_manager.clear_cache()
            st.success("✅ Cache vidé!")
    
    with col2:
        st.markdown("### 📊 Statistiques")
        cache_size = len(icon_manager._icon_cache)
        st.metric("Icônes en cache", cache_size)
        
        total_icons = sum(len(icons) for icons in icon_manager.list_available_icons().values())
        st.metric("Total icônes configurées", total_icons)

# Code d'exemple pour l'utilisation dans un dashboard
EXAMPLE_DASHBOARD_CODE = '''
# Dans votre fichier dashboard.py
from utils.icons import get_kpi_icon

# Utilisation dans une carte KPI
display_stat_card(
    "Score global ISO 27001",
    f"{stats['taux_conformite']}%",
    get_kpi_icon("score_global"),  # ← Remplace l'emoji
    color
)

# Avec taille personnalisée
display_stat_card(
    "Critères évalués",
    f"{total}/{max_total}",
    get_kpi_icon("criteres_evalues", "52px"),  # ← Taille custom
    COLORS['info']
)

# Icône dans du HTML personnalisé
st.markdown(f"""
<div class="custom-card">
    {get_kpi_icon("audits", "40px")}
    <h3>Mes Audits</h3>
</div>
""", unsafe_allow_html=True)
'''

def code_examples():
    """Exemples de code"""
    
    st.header("💻 Exemples de code")
    
    st.subheader("Utilisation dans un dashboard")
    st.code(EXAMPLE_DASHBOARD_CODE, language="python")
    
    st.subheader("Ajout d'icône personnalisée")
    st.code('''
# Ajouter une nouvelle icône KPI
icon_manager.add_custom_icon(
    category="kpi",
    icon_key="nouveau_kpi",
    filename="mon_kpi.png",
    alt_text="Mon nouveau KPI",
    fallback="📈"
)

# L'utiliser immédiatement
mon_icone = get_kpi_icon("nouveau_kpi", "48px")
''', language="python")

if __name__ == "__main__":
    # Interface de démonstration
    st.set_page_config(
        page_title="Système d'icônes - Sécurité 360",
        page_icon="🎨",
        layout="wide"
    )
    
    tab1, tab2, tab3, tab4 = st.tabs([
        "📊 Démonstration", 
        "➕ Ajouter icône", 
        "⚡ Performance", 
        "💻 Exemples"
    ])
    
    with tab1:
        demo_icons()
    
    with tab2:
        add_custom_icon_demo()
    
    with tab3:
        performance_tools()
    
    with tab4:
        code_examples()