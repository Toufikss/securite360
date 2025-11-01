"""
Page de gestion des audits - Sécurité 360
Planification et suivi des audits internes
"""

import streamlit as st
from utils.helpers import display_page_header, format_date
from utils.config import COLORS
from utils.charts import create_audit_timeline
from datetime import datetime

def show(auth, db):
    """Affiche la page de gestion des audits"""
    
    # En-tête
    display_page_header(
        "Audits internes",
        "Planification et suivi des audits de conformité ISO 27001"
    )
    
    # Récupérer les audits
    audits = db.get_all_audits()
    
    # Tabs
    tab1, tab2, tab3 = st.tabs(["📋 Liste des audits", "📊 Chronologie", "➕ Nouvel audit"])
    
    with tab1:
        st.markdown(f"###  Audits réalisés ({len(audits)})")
        
        if audits:
            for audit in audits:
                score = audit.get('score', 0)
                score_color = COLORS['success'] if score >= 80 else COLORS['warning'] if score >= 50 else COLORS['danger']
                
                with st.container():
                    st.markdown(f"""
                    <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem; border-left: 4px solid {score_color};">
                        <div style="display: flex; justify-content: space-between; align-items: start;">
                            <div style="flex: 1;">
                                <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">{audit['titre']}</h4>
                                <p style="color: {COLORS['text_secondary']}; margin: 0 0 0.5rem 0;">
                                    <strong>Date:</strong> {format_date(audit['date_audit'])} | 
                                    <strong>Auditeur:</strong> {audit['auditeur']} | 
                                    <strong>Statut:</strong> {audit['statut']}
                                </p>
                                <div style="margin-top: 1rem;">
                                    <div style="display: inline-block; background-color: {score_color}; color: white; padding: 0.5rem 1rem; border-radius: 8px; font-weight: bold;">
                                        Score: {score}%
                                    </div>
                                </div>
                            </div>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    # Détails de l'audit
                    with st.expander(f" Détails de l'audit #{audit['id']}"):
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown(f"**Date de création:** {format_date(audit['created_at'])}")
                            st.markdown(f"**Statut:** {audit['statut']}")
                        
                        with col2:
                            st.markdown(f"**Score global:** {score}%")
                            st.markdown(f"**Auditeur:** {audit['auditeur']}")
                        
                        if audit.get('commentaires'):
                            st.markdown("**Commentaires:**")
                            st.info(audit['commentaires'])
                        
                        # Actions (si permissions)
                        if auth.has_role("Auditeur"):
                            col_action1, col_action2 = st.columns(2)
                            
                            with col_action1:
                                if st.button(" Exporter le rapport", key=f"export_{audit['id']}"):
                                    st.success("Export en cours... (fonctionnalité à implémenter)")
                            
                            with col_action2:
                                # Bouton de suppression avec confirmation
                                if st.button(" Supprimer l'audit", key=f"delete_{audit['id']}", type="secondary"):
                                    st.session_state[f"confirm_delete_{audit['id']}"] = True
                            
                            # Confirmation de suppression
                            if st.session_state.get(f"confirm_delete_{audit['id']}", False):
                                st.warning(f" Êtes-vous sûr de vouloir supprimer l'audit **{audit['titre']}** ?")
                                col_confirm1, col_confirm2 = st.columns(2)
                                
                                with col_confirm1:
                                    if st.button(" Oui, supprimer", key=f"confirm_yes_{audit['id']}", type="primary"):
                                        if db.delete_audit(audit['id']):
                                            st.success(f" Audit '{audit['titre']}' supprimé avec succès!")
                                            st.session_state[f"confirm_delete_{audit['id']}"] = False
                                            st.rerun()
                                        else:
                                            st.error(" Erreur lors de la suppression de l'audit")
                                
                                with col_confirm2:
                                    if st.button(" Annuler", key=f"confirm_no_{audit['id']}"):
                                        st.session_state[f"confirm_delete_{audit['id']}"] = False
                                        st.rerun()
        else:
            st.info("Aucun audit n'a été réalisé pour le moment")
    
    with tab2:
        st.markdown("###  Chronologie des audits")
        
        if audits:
            # Graphique de chronologie
            fig = create_audit_timeline(audits)
            st.plotly_chart(fig, use_container_width=True)
            
            # Statistiques
            scores = [a.get('score', 0) for a in audits if a.get('score')]
            if scores:
                avg_score = sum(scores) / len(scores)
                max_score = max(scores)
                min_score = min(scores)
                
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Score moyen", f"{avg_score:.1f}%")
                with col2:
                    st.metric("Score maximum", f"{max_score:.1f}%")
                with col3:
                    st.metric("Score minimum", f"{min_score:.1f}%")
                with col4:
                    st.metric("Nombre d'audits", len(audits))
                
                # Tendance
                st.markdown("<br>", unsafe_allow_html=True)
                if len(scores) >= 2:
                    tendance = scores[-1] - scores[-2]
                    tendance_text = "En hausse ↗" if tendance > 0 else "En baisse ↘" if tendance < 0 else "Stable →"
                    tendance_color = COLORS['success'] if tendance > 0 else COLORS['danger'] if tendance < 0 else COLORS['info']
                    
                    st.markdown(f"""
                    <div style="background-color: {COLORS['surface']}; padding: 1rem; border-radius: 8px; text-align: center;">
                        <p style="color: {COLORS['text_secondary']}; margin: 0; font-size: 0.9rem;">Tendance</p>
                        <p style="color: {tendance_color}; margin: 0.5rem 0 0 0; font-size: 1.5rem; font-weight: bold;">
                            {tendance_text} ({tendance:+.1f}%)
                        </p>
                    </div>
                    """, unsafe_allow_html=True)
        else:
            st.info("Aucune donnée disponible pour afficher la chronologie")
    
    with tab3:
        if auth.has_role("Auditeur"):
            st.markdown("###  Planifier un nouvel audit")
            
            user = auth.get_current_user()
            
            with st.form("nouvel_audit"):
                titre = st.text_input(
                    "Titre de l'audit *",
                    placeholder="Ex: Audit ISO 27001 Q1 2025"
                )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    date_audit = st.date_input(
                        "Date de l'audit *",
                        value=datetime.now()
                    )
                
                with col2:
                    auditeur = st.text_input(
                        "Auditeur *",
                        value=user['username']
                    )
                
                col1, col2 = st.columns(2)
                
                with col1:
                    statut = st.selectbox(
                        "Statut *",
                        ['Planifié', 'En cours', 'Terminé', 'Reporté']
                    )
                
                with col2:
                    score = st.slider(
                        "Score de conformité (%)",
                        0, 100, 0,
                        help="Peut être ajusté après l'audit"
                    )
                
                commentaires = st.text_area(
                    "Commentaires et observations",
                    height=150,
                    placeholder="Notes sur l'audit, points d'attention, recommandations..."
                )
                
                # Checklist d'audit
                st.markdown("####  Checklist d'audit (optionnel)")
                
                col1, col2 = st.columns(2)
                
                with col1:
                    check1 = st.checkbox("Documentation revue")
                    check2 = st.checkbox("Interviews réalisées")
                    check3 = st.checkbox("Tests techniques effectués")
                
                with col2:
                    check4 = st.checkbox("Conformité physique vérifiée")
                    check5 = st.checkbox("Politiques validées")
                    check6 = st.checkbox("Rapport préparé")
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button(" Enregistrer l'audit", use_container_width=True, type="primary")
                with col2:
                    cancel = st.form_submit_button(" Annuler", use_container_width=True)
                
                if submit:
                    if titre and date_audit and auditeur and statut:
                        audit_id = db.add_audit(
                            titre=titre,
                            date_audit=date_audit.strftime('%Y-%m-%d'),
                            auditeur=auditeur,
                            statut=statut,
                            score=score,
                            commentaires=commentaires
                        )
                        st.success(f"✅ Audit créé avec succès! (ID: {audit_id})")
                        st.rerun()
                    else:
                        st.error("Veuillez remplir tous les champs obligatoires (*)")
        else:
            st.warning(" Vous devez avoir les droits d'auditeur pour créer un audit")
    
    # Guide d'audit
    with st.expander(" Guide de réalisation d'un audit ISO 27001"):
        st.markdown("#### Phases d'un audit interne :")
        
        st.markdown("##### 1. Préparation")
        st.markdown("""
        - Définir le périmètre et les objectifs
        - Constituer l'équipe d'audit
        - Préparer les documents de référence
        - Élaborer le programme d'audit
        """)
        
        st.markdown("##### 2. Réalisation")
        st.markdown("""
        - Réunion d'ouverture
        - Collecte des preuves (documents, interviews, observations)
        - Vérification de la conformité aux critères
        - Documentation des constats
        """)
        
        st.markdown("##### 3. Clôture")
        st.markdown("""
        - Analyse des constats
        - Réunion de clôture
        - Rédaction du rapport d'audit
        - Définition des actions correctives
        """)
        
        st.markdown("##### 4. Suivi")
        st.markdown("""
        - Suivi des actions correctives
        - Vérification de l'efficacité des corrections
        - Planification de l'audit suivant
        """)
        
        st.markdown("#### Points clés à auditer :")
        st.markdown("""
        - Politique de sécurité de l'information
        - Organisation de la sécurité
        - Gestion des actifs
        - Contrôle d'accès
        - Cryptographie
        - Sécurité physique et environnementale
        - Sécurité des opérations
        - Sécurité des communications
        - Gestion des incidents
        - Conformité
        """)