"""
Exemple d'utilisation des tailles d'icônes personnalisées
Script pour tester et démontrer les différentes tailles disponibles
"""

import streamlit as st
from utils.icons import get_kpi_icon, icon_manager
from utils.icon_sizes import (
    ICON_SIZES, 
    KPI_ICON_SIZES, 
    get_icon_size,
    set_all_kpi_size,
    update_kpi_size,
    get_all_kpi_sizes
)

def demo_tailles_icones():
    """Démonstration des différentes tailles d'icônes"""
    
    st.title("🎨 Configuration des Tailles d'Icônes")
    
    # Section 1: Tailles disponibles
    st.header("📏 Tailles Disponibles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.subheader("Tailles Prédéfinies")
        for size_name, size_value in ICON_SIZES.items():
            st.write(f"**{size_name}**: {size_value}")
    
    with col2:
        st.subheader("Exemple Visuel")
        test_icon = "score_global"
        
        for size_name, size_value in list(ICON_SIZES.items())[:6]:  # Premier 6 pour l'affichage
            st.write(f"**{size_name}** ({size_value}):")
            st.markdown(get_kpi_icon(test_icon, size_value), unsafe_allow_html=True)
            st.write("---")
    
    with col3:
        st.subheader("Configuration Actuelle KPI")
        current_config = get_all_kpi_sizes()
        for icon_key, size in current_config.items():
            st.write(f"**{icon_key}**: {size}")
    
    # Section 2: Modifier les tailles
    st.header("⚙️ Modifier les Tailles")
    
    tab1, tab2, tab3 = st.tabs(["Modifier Une Icône", "Modifier Toutes", "Aperçu"])
    
    with tab1:
        st.subheader("Modifier une icône spécifique")
        
        # Sélectionner l'icône
        available_icons = list(KPI_ICON_SIZES.keys())
        selected_icon = st.selectbox(
            "Choisir l'icône à modifier:",
            available_icons,
            key="single_icon_select"
        )
        
        # Sélectionner la nouvelle taille
        size_options = list(ICON_SIZES.keys()) + ["Taille personnalisée"]
        selected_size = st.selectbox(
            "Choisir la nouvelle taille:",
            size_options,
            key="single_size_select"
        )
        
        if selected_size == "Taille personnalisée":
            custom_size = st.text_input(
                "Saisir la taille (ex: 72px):",
                placeholder="72px",
                key="custom_size_input"
            )
        else:
            custom_size = None
        
        if st.button("Appliquer la modification", key="apply_single"):
            try:
                if selected_size == "Taille personnalisée" and custom_size:
                    update_kpi_size(selected_icon, custom_size)
                    st.success(f"✅ Icône '{selected_icon}' mise à jour avec la taille {custom_size}")
                else:
                    update_kpi_size(selected_icon, selected_size)
                    actual_size = ICON_SIZES.get(selected_size, selected_size)
                    st.success(f"✅ Icône '{selected_icon}' mise à jour avec la taille {actual_size}")
                
                st.experimental_rerun()
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")
    
    with tab2:
        st.subheader("Modifier toutes les icônes KPI")
        
        # Options de taille globale
        global_size = st.selectbox(
            "Choisir la taille pour toutes les icônes KPI:",
            list(ICON_SIZES.keys()),
            index=4,  # Par défaut sur "large"
            key="global_size_select"
        )
        
        st.write(f"Nouvelle taille: **{ICON_SIZES[global_size]}**")
        
        if st.button("Appliquer à toutes les icônes", key="apply_all"):
            try:
                set_all_kpi_size(global_size)
                st.success(f"✅ Toutes les icônes KPI mises à jour avec la taille {ICON_SIZES[global_size]}")
                st.experimental_rerun()
            except Exception as e:
                st.error(f"❌ Erreur: {str(e)}")
        
        st.warning("⚠️ Cette action modifiera toutes les icônes KPI en même temps.")
    
    with tab3:
        st.subheader("Aperçu des Tailles Actuelles")
        
        st.write("**Toutes les icônes KPI avec leurs tailles actuelles:**")
        
        # Afficher toutes les icônes en grille
        cols = st.columns(4)
        
        for idx, icon_key in enumerate(available_icons):
            with cols[idx % 4]:
                current_size = get_icon_size(icon_key, "kpi")
                
                st.write(f"**{icon_key}**")
                st.write(f"Taille: {current_size}")
                
                try:
                    icon_html = get_kpi_icon(icon_key)
                    st.markdown(icon_html, unsafe_allow_html=True)
                except:
                    st.write("🔧 (Icône non disponible)")
                
                st.write("---")

def code_examples_tailles():
    """Exemples de code pour les tailles"""
    
    st.header("💻 Exemples de Code")
    
    st.subheader("1. Utilisation Basique (avec configuration automatique)")
    st.code('''
# Les tailles sont automatiquement appliquées selon la configuration
from utils.icons import get_kpi_icon

# Utilise la taille configurée pour score_global (80px par défaut)
icone_score = get_kpi_icon("score_global")

# Utilise la taille configurée pour audits (64px par défaut)  
icone_audits = get_kpi_icon("audits")
    ''', language="python")
    
    st.subheader("2. Forcer une Taille Spécifique")
    st.code('''
# Forcer une taille particulière
icone_grande = get_kpi_icon("score_global", "96px")  # Très grande
icone_petite = get_kpi_icon("documents", "24px")     # Petite

# Utiliser les tailles nommées
icone_xl = get_kpi_icon("audits", "xl")        # 80px
icone_medium = get_kpi_icon("risques", "medium") # 32px
    ''', language="python")
    
    st.subheader("3. Modifier la Configuration")
    st.code('''
from utils.icon_sizes import update_kpi_size, set_all_kpi_size

# Modifier une icône spécifique
update_kpi_size("score_global", "xxl")  # 96px

# Changer toutes les icônes KPI
set_all_kpi_size("large")  # Toutes en 64px

# Ensuite, get_kpi_icon() utilisera automatiquement les nouvelles tailles
    ''', language="python")
    
    st.subheader("4. Dans le Dashboard")
    st.code('''
# Dans pages/dashboard.py
from utils.icons import get_kpi_icon

# Les icônes utilisent automatiquement leurs tailles configurées
display_stat_card(
    "Score global ISO 27001",
    f"{stats['taux_conformite']}%",
    get_kpi_icon("score_global"),  # 80px automatique
    color
)

# Pour forcer une taille spéciale dans un cas particulier
display_stat_card(
    "Critères évalués",
    f"{total}/{max_total}",
    get_kpi_icon("criteres_evalues", "xxl"),  # Force 96px
    COLORS['info']
)
    ''', language="python")

def config_rapide():
    """Configuration rapide des tailles"""
    
    st.header("⚡ Configuration Rapide")
    
    st.write("Choisissez un profil de tailles prédéfini:")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("📱 Compact\n(Toutes petites)", key="compact"):
            set_all_kpi_size("small")
            st.success("✅ Profil Compact appliqué (24px)")
            st.experimental_rerun()
    
    with col2:
        if st.button("💼 Standard\n(Tailles moyennes)", key="standard"):
            set_all_kpi_size("large")
            st.success("✅ Profil Standard appliqué (64px)")
            st.experimental_rerun()
    
    with col3:
        if st.button("🎯 Impact\n(Grandes icônes)", key="impact"):
            set_all_kpi_size("xl")
            st.success("✅ Profil Impact appliqué (80px)")
            st.experimental_rerun()
    
    st.write("---")
    
    st.subheader("Configuration Personnalisée par Importance")
    
    if st.button("🎨 Configuration par Importance", key="custom_importance"):
        # Score global = le plus important
        update_kpi_size("score_global", "xxl")  # 96px
        
        # KPI principaux = grands
        for kpi in ["audits", "criteres_evalues", "criteres_risque"]:
            update_kpi_size(kpi, "xl")  # 80px
        
        # KPI secondaires = moyens
        for kpi in ["evolution_semestrielle", "delai_moyen", "prochaine_echeance", "maturite"]:
            update_kpi_size(kpi, "large")  # 64px
        
        # Autres = petits
        for kpi in ["documents", "formations", "incidents", "risques", "actions_correctives", "non_conformites"]:
            update_kpi_size(kpi, "medium")  # 32px
        
        st.success("✅ Configuration par importance appliquée!")
        st.experimental_rerun()

if __name__ == "__main__":
    st.set_page_config(
        page_title="Configuration Tailles Icônes",
        page_icon="🎨",
        layout="wide"
    )
    
    tab1, tab2, tab3 = st.tabs(["🎨 Démo Tailles", "💻 Exemples Code", "⚡ Config Rapide"])
    
    with tab1:
        demo_tailles_icones()
    
    with tab2:
        code_examples_tailles()
    
    with tab3:
        config_rapide()