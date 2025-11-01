"""
Page de déclaration d'applicabilité - Sécurité 360
Gestion des critères ISO 27001 Annexe A
"""

import streamlit as st
from utils.helpers import display_page_header, get_statut_badge, get_categorie_icon, filter_criteres
from utils.config import COLORS, CATEGORIES_ISO, STATUTS_CONFORMITE
from utils.iso_commentaires import get_commentaire
import pandas as pd

def show(auth, db):
    """Affiche la page de déclaration d'applicabilité"""
    
    # En-tête
    display_page_header(
        "Déclaration d'applicabilité",
        "Gestion des critères ISO 27001 - Annexe A"
    )
    
    # Récupérer tous les critères
    criteres = db.get_all_criteres()
    
    # Filtres
    st.markdown(f"""
    <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1.5rem;">
        <h3 style="color: {COLORS['text']}; margin-top: 0;"> Filtres</h3>
    </div>
    """, unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        filtre_categorie = st.selectbox(
            "Catégorie",
            ['Toutes'] + CATEGORIES_ISO,
            key="filtre_cat"
        )
    
    with col2:
        filtre_statut = st.selectbox(
            "Statut",
            ['Tous'] + STATUTS_CONFORMITE,
            key="filtre_statut"
        )
    
    with col3:
        recherche = st.text_input(
            "Rechercher",
            placeholder="Code, titre ou description...",
            key="recherche"
        )
    
    # Appliquer les filtres
    filters = {
        'categorie': filtre_categorie,
        'statut': filtre_statut,
        'recherche': recherche
    }
    criteres_filtres = filter_criteres(criteres, filters)
    
    # Statistiques des critères filtrés
    st.markdown(f"""
    <div style="background-color: {COLORS['surface']}; padding: 1rem; border-radius: 8px; margin-bottom: 1rem;">
        <p style="color: {COLORS['text_secondary']}; margin: 0;">
            <strong style="color: {COLORS['text']};">{len(criteres_filtres)}</strong> critère(s) trouvé(s) sur <strong style="color: {COLORS['text']};">{len(criteres)}</strong>
        </p>
    </div>
    """, unsafe_allow_html=True)
    
    # Options d'affichage
    col1, col2 = st.columns([3, 1])
    with col1:
        st.markdown(f"### 📋 Liste des critères")
    with col2:
        vue_mode = st.radio("Vue", ["Cartes", "Tableau"], horizontal=True, label_visibility="collapsed")
    
    # Affichage selon le mode
    if vue_mode == "Cartes":
        # Affichage en cartes
        for critere in criteres_filtres:
            with st.container():
                # Afficher la date de mise à jour
                derniere_maj = critere.get('derniere_maj', 'N/A')
                if derniere_maj and derniere_maj != 'N/A':
                    derniere_maj = derniere_maj[:19]  # Format: YYYY-MM-DD HH:MM:SS
                
                # Carte principale du critère
                st.markdown(f"""
                <div class="critere-card" style="border-left-color: {COLORS['info']};">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <p class="critere-code">{get_categorie_icon(critere['categorie'])} {critere['code']}</p>
                            <p class="critere-titre">{critere['titre']}</p>
                            <p class="critere-description">{critere['description']}</p>
                            <div style="margin-top: 1rem;">
                                <span style="background-color: {COLORS['primary']}; color: white; padding: 0.25rem 0.6rem; border-radius: 12px; font-size: 0.75rem; margin-right: 0.5rem;">{critere['categorie']}</span>
                                {get_statut_badge(critere['statut'])}
                                <span style="color: {COLORS['text_secondary']}; font-size: 0.75rem; margin-left: 0.5rem;">🕒 MAJ: {derniere_maj}</span>
                            </div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Récupérer et afficher le commentaire ISO 27001
                commentaire_iso = get_commentaire(critere['code'])
                if commentaire_iso:
                    st.markdown(f"""
                    <div style="margin-top: 0.75rem; padding: 1rem; background-color: {COLORS['surface']}; border-radius: 8px; border-left: 3px solid {COLORS['info']};">
                        <p style="color: {COLORS['info']}; font-size: 0.75rem; margin: 0; font-weight: 600; margin-bottom: 0.5rem;">
                            � Exigence ISO 27001:2022 - Annexe A
                        </p>
                        <p style="color: {COLORS['text']}; font-size: 0.9rem; margin: 0; line-height: 1.6;">
                            {commentaire_iso}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Afficher le commentaire utilisateur si présent
                commentaire_user = critere.get('commentaire', '')
                if commentaire_user:
                    st.markdown(f"""
                    <div style="margin-top: 0.75rem; padding: 0.75rem; background-color: {COLORS['background']}; border-radius: 8px; border-left: 3px solid {COLORS['accent']};">
                        <p style="color: {COLORS['accent']}; font-size: 0.75rem; margin: 0; font-weight: 600; margin-bottom: 0.5rem;">
                            💬 Commentaire de l'organisation
                        </p>
                        <p style="color: {COLORS['text']}; font-size: 0.85rem; margin: 0; line-height: 1.5;">
                            {commentaire_user}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Afficher la preuve si présente
                preuve = critere.get('preuve_path', '')
                if preuve:
                    st.markdown(f"""
                    <div style="margin-top: 0.5rem; padding: 0.5rem; background-color: {COLORS['surface']}; border-radius: 6px;">
                        <p style="color: {COLORS['text_secondary']}; font-size: 0.75rem; margin: 0;">
                            � <span style="color: {COLORS['accent']}; font-weight: 600;">Preuve jointe:</span> {preuve}
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # Options d'édition (si permissions)
                if auth.has_role("Auditeur"):
                    with st.expander(f" Modifier le critère {critere['code']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            nouveau_statut = st.selectbox(
                                "Statut",
                                STATUTS_CONFORMITE,
                                index=STATUTS_CONFORMITE.index(critere['statut']),
                                key=f"statut_{critere['id']}"
                            )
                        
                        with col2:
                            fichier_preuve = st.file_uploader(
                                "Preuve (optionnel)",
                                type=['pdf', 'docx', 'jpg', 'png'],
                                key=f"preuve_{critere['id']}"
                            )
                        
                        commentaire = st.text_area(
                            "Commentaire",
                            value=critere.get('commentaire', ''),
                            key=f"comment_{critere['id']}",
                            height=100
                        )
                        
                        if st.button(" Enregistrer", key=f"save_{critere['id']}"):
                            preuve_path = None
                            if fichier_preuve:
                                # Sauvegarder le fichier (simulation)
                                preuve_path = f"preuves/{fichier_preuve.name}"
                            
                            db.update_critere(
                                critere['id'],
                                nouveau_statut,
                                commentaire,
                                preuve_path
                            )
                            st.success("✅ Critère mis à jour avec succès!")
                            st.rerun()
                
                st.markdown("<br>", unsafe_allow_html=True)
    
    else:
        # Affichage en tableau
        df_data = []
        for critere in criteres_filtres:
            df_data.append({
                'Code': critere['code'],
                'Titre': critere['titre'],
                'Catégorie': critere['categorie'],
                'Statut': critere['statut'],
                'Dernière MAJ': critere.get('derniere_maj', 'N/A')[:10]
            })
        
        if df_data:
            df = pd.DataFrame(df_data)
            
            # Style du DataFrame
            st.dataframe(
                df,
                use_container_width=True,
                height=600,
                hide_index=True
            )
            
            # Export CSV
            csv = df.to_csv(index=False, encoding='utf-8-sig')
            st.download_button(
                label="📥 Exporter en CSV",
                data=csv,
                file_name="declaration_applicabilite.csv",
                mime="text/csv"
            )
        else:
            st.info("Aucun critère à afficher")
    
    # Statistiques en bas de page
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px;">
        <h3 style="color: {COLORS['text']}; margin-top: 0;"> Statistiques globales</h3>
    </div>
    """, unsafe_allow_html=True)
    
    stats = db.get_conformity_stats()
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total critères", stats['total'])
    
    with col2:
        st.metric("Conformes", stats['conforme'], delta=None)
    
    with col3:
        st.metric("Partiellement conformes", stats['partiellement_conforme'])
    
    with col4:
        st.metric("Non conformes", stats['non_conforme'])