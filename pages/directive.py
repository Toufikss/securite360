"""
Page des directives et mesures - Sécurité 360
Gestion des mesures techniques et organisationnelles
"""

import streamlit as st
from utils.helpers import display_page_header
from utils.config import COLORS, TYPES_DIRECTIVES, NIVEAUX_EFFICACITE
from utils.charts import create_directive_effectiveness_chart

def show(auth, db):
    """Affiche la page des directives et mesures"""
    
    # En-tête
    display_page_header(
        "Directives et mesures",
        "Gestion des mesures techniques et organisationnelles"
    )
    
    # Récupérer les directives
    directives = db.get_all_directives()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Liste des directives", "📊 Analyse", "➕ Nouvelle directive"])
    
    with tab1:
        st.markdown(f"###  Directives actives ({len(directives)})")
        
        # Filtres
        col1, col2 = st.columns(2)
        with col1:
            filtre_type = st.selectbox("Type", ['Tous'] + TYPES_DIRECTIVES)
        with col2:
            filtre_efficacite = st.selectbox("Efficacité", ['Tous'] + NIVEAUX_EFFICACITE)
        
        # Appliquer les filtres
        directives_filtrees = directives
        if filtre_type != 'Tous':
            directives_filtrees = [d for d in directives_filtrees if d['type'] == filtre_type]
        if filtre_efficacite != 'Tous':
            directives_filtrees = [d for d in directives_filtrees if d['efficacite'] == filtre_efficacite]
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        if directives_filtrees:
            for directive in directives_filtrees:
                # Couleur selon l'efficacité
                efficacite_colors = {
                    'Élevée': COLORS['success'],
                    'Moyenne': COLORS['info'],
                    'Faible': COLORS['warning'],
                    'À améliorer': COLORS['danger']
                }
                color = efficacite_colors.get(directive['efficacite'], COLORS['info'])
                
                with st.container():
                    st.markdown(f"""
                    <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid {color};">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 1;">
                                <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">{directive['titre']}</h4>
                                <p style="color: {COLORS['text_secondary']}; margin: 0 0 1rem 0;">{directive['description']}</p>
                                <div>
                                    <span style="background-color: {COLORS['primary']}; color: white; padding: 0.3rem 0.7rem; border-radius: 15px; font-size: 0.8rem; margin-right: 0.5rem;">
                                        {directive['type']}
                                    </span>
                                    <span style="background-color: {color}; color: white; padding: 0.3rem 0.7rem; border-radius: 15px; font-size: 0.8rem; margin-right: 0.5rem;">
                                        Efficacité: {directive['efficacite']}
                                    </span>
                                    {f'<span style="color: {COLORS["text_secondary"]}; font-size: 0.85rem;">Responsable: {directive["responsable"]}</span>' if directive.get('responsable') else ''}
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Actions pour Admin
                    if auth.has_role("Admin"):
                        col1, col2 = st.columns([5, 1])
                        with col2:
                            if st.button("🗑️ Supprimer", key=f"del_{directive['id']}", use_container_width=True):
                                db.delete_directive(directive['id'])
                                st.success("Directive supprimée")
                                st.rerun()
        else:
            st.info("Aucune directive trouvée avec ces filtres")
    
    with tab2:
        st.markdown("###  Analyse des directives")
        
        if directives:
            # Graphique d'efficacité
            fig = create_directive_effectiveness_chart(directives)
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistiques
            col1, col2, col3, col4 = st.columns(4)
            
            types_count = {}
            for d in directives:
                t = d['type']
                types_count[t] = types_count.get(t, 0) + 1
            
            with col1:
                st.metric("Total directives", len(directives))
            with col2:
                efficaces = len([d for d in directives if d['efficacite'] == 'Élevée'])
                st.metric("Efficacité élevée", efficaces)
            with col3:
                techniques = types_count.get('Technique', 0)
                st.metric("Mesures techniques", techniques)
            with col4:
                org = types_count.get('Organisationnelle', 0)
                st.metric("Mesures organisationnelles", org)
            
            # Répartition par type
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("#### Répartition par type")
            
            for type_dir, count in types_count.items():
                percentage = (count / len(directives)) * 100
                st.markdown(f"""
                <div style="margin-bottom: 0.5rem;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 0.3rem;">
                        <span style="color: {COLORS['text']};">{type_dir}</span>
                        <span style="color: {COLORS['text_secondary']};">{count} ({percentage:.1f}%)</span>
                    </div>
                    <div style="background-color: {COLORS['background']}; border-radius: 10px; height: 10px; overflow: hidden;">
                        <div style="background-color: {COLORS['accent']}; height: 100%; width: {percentage}%;"></div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aucune donnée disponible pour l'analyse")
    
    with tab3:
        if auth.has_role("Admin"):
            st.markdown("### ➕ Créer une nouvelle directive")
            
            user = auth.get_current_user()
            
            with st.form("nouvelle_directive"):
                titre = st.text_input(
                    "Titre de la directive *",
                    placeholder="Ex: Politique de gestion des mots de passe"
                )
                
                description = st.text_area(
                    "Description *",
                    height=150,
                    placeholder="Décrivez la directive en détail..."
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    type_directive = st.selectbox(
                        "Type de directive *",
                        TYPES_DIRECTIVES
                    )
                
                with col2:
                    efficacite = st.selectbox(
                        "Niveau d'efficacité *",
                        NIVEAUX_EFFICACITE
                    )
                
                responsable = st.text_input(
                    "Responsable",
                    placeholder="Nom du responsable de la mise en œuvre"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("💾 Enregistrer", use_container_width=True, type="primary")
                with col2:
                    cancel = st.form_submit_button("❌ Annuler", use_container_width=True)
                
                if submit:
                    if titre and description and type_directive and efficacite:
                        db.add_directive(
                            titre=titre,
                            description=description,
                            type_dir=type_directive,
                            efficacite=efficacite,
                            responsable=responsable if responsable else "Non assigné"
                        )
                        st.success("✅ Directive créée avec succès!")
                        st.rerun()
                    else:
                        st.error("Veuillez remplir tous les champs obligatoires (*)")
        else:
            st.warning("🚫 Vous devez avoir les droits d'administrateur pour créer une directive")
    
    # Section exemples
    with st.expander("💡 Exemples de directives"):
        st.markdown("#### Exemples de directives techniques :")
        st.markdown("""
        - Mise en place d'un pare-feu périmétrique
        - Chiffrement des données sensibles au repos et en transit
        - Authentification multi-facteurs pour les accès critiques
        - Journalisation et surveillance des événements de sécurité
        - Gestion des correctifs de sécurité
        """)
        
        st.markdown("#### Exemples de directives organisationnelles :")
        st.markdown("""
        - Processus de classification des données
        - Politique de bureau propre et écran vide
        - Procédure de gestion des incidents de sécurité
        - Programme de sensibilisation à la sécurité
        - Gestion des accès et des habilitations
        """)
        
        st.markdown("#### Exemples de directives procédurales :")
        st.markdown("""
        - Procédure de sauvegarde et de restauration
        - Procédure de gestion des changements
        - Procédure de départ d'employé
        - Procédure d'audit interne
        - Procédure de revue de conformité
        """)