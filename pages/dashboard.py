"""
Page du tableau de bord - Sécurité 360
Affiche les indicateurs clés de conformité et statistiques
Dashboard modulaire et hiérarchisé
"""

import streamlit as st
from utils.helpers import display_page_header, display_stat_card, format_date
from utils.charts import create_conformity_gauge, create_conformity_pie_chart, create_category_bar_chart, create_radial_category_chart
from utils.config import COLORS
from utils.icons import get_kpi_icon, icon_manager
import plotly.graph_objects as go
from datetime import datetime, timedelta

def show(auth, db):
    """Affiche le tableau de bord modulaire"""
    
    # En-tête de la page avec filtres contextuels
    display_page_header(
        "Tableau de bord gestion ISO 27001",
        "Vue d'ensemble interactive de la conformité"
    )
    

    
    # Récupérer les données filtrées
    stats = db.get_conformity_stats()
    criteres = db.get_all_criteres()
    audits = db.get_all_audits()
    
    # === SECTION 2: INDICATEURS CLÉS GLOBAUX ===
    st.markdown(f"""
    <div style="
        background: linear-gradient(135deg, {COLORS['primary']}15 0%, {COLORS['surface']} 30%, {COLORS['info']}08 100%);
        padding: 0.8rem 1.2rem 0.6rem 1.2rem; 
        border-radius: 12px; 
        margin-bottom: 1.5rem;
        border: 1px solid {COLORS['primary']}20;
        box-shadow: 0 4px 16px rgba(0,0,0,0.06), 0 1px 8px rgba(0,0,0,0.03);
        position: relative;
        overflow: hidden;
    ">
        <div style="
            position: absolute; 
            top: 0; 
            left: 0; 
            right: 0; 
            height: 4px; 
            background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['info']} 50%, {COLORS['success']} 100%);
        "></div>
        <h3 style="
            color: {COLORS['text']}; 
            margin: 0 0 0.2rem 0; 
            font-size: 1.3rem; 
            font-weight: 600;
            display: flex; 
            align-items: center; 
            gap: 0.8rem;
            text-shadow: 0 1px 2px rgba(0,0,0,0.05);
        ">
            <span style="
                font-size: 1.2rem; 
                background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['info']} 100%); 
                -webkit-background-clip: text; 
                -webkit-text-fill-color: transparent; 
                background-clip: text;
                filter: drop-shadow(0 1px 2px rgba(0,0,0,0.1));
            "></span>
            <span>Indicateurs clés de performance</span>
            <span style="
                background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['info']} 100%);
                color: white;
                padding: 0.2rem 0.8rem;
                border-radius: 20px;
                font-size: 0.75rem;
                font-weight: 600;
                text-transform: uppercase;
                letter-spacing: 0.5px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.15);
                display: inline-block;
            ">KPI</span>
        </h3>
        <p style="
            color: {COLORS['text_secondary']}; 
            font-size: 0.75rem; 
            margin: 0;
            font-style: italic;
            opacity: 0.8;
        ">Métriques essentielles de conformité ISO 27001</p>
    </div>
    """, unsafe_allow_html=True)
    
    # KPI Cards - 4 colonnes
    kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
    
    with kpi_col1:
        display_stat_card(
            "Score global ISO 27001",
            f"{stats['taux_conformite']}%",
            get_kpi_icon("score_global"),
            COLORS['success'] if stats['taux_conformite'] >= 80 else 
            COLORS['warning'] if stats['taux_conformite'] >= 50 else COLORS['danger']
        )
    
    with kpi_col2:
        display_stat_card(
            "Critères évalués",
            f"{stats['conforme'] + stats['largement_conforme'] + stats['partiellement_conforme'] + stats['faiblement_conforme'] + stats['non_conforme']}/{stats['total']}",
            get_kpi_icon("criteres_evalues"),
            COLORS['info']
        )
    
    with kpi_col3:
        # Calculer les critères à risque (faiblement + non conformes)
        criteres_risque = stats['faiblement_conforme'] + stats['non_conforme']
        display_stat_card(
            "Critères à risque",
            str(criteres_risque),
            get_kpi_icon("criteres_risque"),
            COLORS['danger'] if criteres_risque > 10 else 
            COLORS['warning'] if criteres_risque > 5 else COLORS['success']
        )
    
    with kpi_col4:
        display_stat_card(
            "Audits cette période",
            str(len(audits)),
            get_kpi_icon("audits"),
            COLORS['primary']
        )
    
    # KPI Cards - 2ème ligne avec métriques avancées
    kpi_col5, kpi_col6, kpi_col7, kpi_col8 = st.columns(4)
    
    with kpi_col5:
        # Évolution (simulée pour l'exemple)
        evolution = "+5.2%"
        display_stat_card(
            "Évolution semestrielle",
            evolution,
            get_kpi_icon("evolution_semestrielle"),
            COLORS['success']
        )
    
    with kpi_col6:
        # Temps moyen de résolution
        display_stat_card(
            "Délai moyen résolution",
            "12 jours",
            get_kpi_icon("delai_moyen"),
            COLORS['info']
        )
    
    with kpi_col7:
        # Prochaine échéance
        display_stat_card(
            "Prochaine échéance",
            "Audit Q1 2025",
            get_kpi_icon("prochaine_echeance"),
            COLORS['warning']
        )
    
    with kpi_col8:
        # Score de maturité
        display_stat_card(
            "Maturité sécurité",
            "Niveau 3/5",
            get_kpi_icon("maturite"),
            COLORS['secondary']
        )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === SECTION 3: ANALYSE GLOBALE DE CONFORMITÉ ===
    st.markdown(f"""
    <div style="background-color: {COLORS['surface']}; padding: 0.8rem 1.2rem 0.6rem 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; height: 60px; display: flex; align-items: center;">
        <h3 style="color: {COLORS['text']}; margin: 0; font-size: 1.3rem; font-weight: 600;">Vue d'ensemble de la conformité</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Graphiques principaux - organisés logiquement
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        st.markdown(f"""
        <div style="background-color: {COLORS['background']}; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
            <h4 style="color: {COLORS['text']}; margin-top: 0; font-size: 1.1rem; font-weight: 500;">Évolution de la conformité</h4>
        """, unsafe_allow_html=True)
        
        fig_gauge = create_conformity_gauge(stats['taux_conformite'])
        st.plotly_chart(fig_gauge, use_container_width=True, config={'displayModeBar': False}, key="conformity_gauge_chart")
        
        # Ajouter contexte sous la jauge
        st.markdown(f"""
        <div style="text-align: center; margin-top: 1rem;">
            <p style="color: {COLORS['text_secondary']}; font-size: 0.9rem; margin: 0;">
                <strong>Objectif:</strong> ≥80% | <strong>Statut:</strong> 
                <span style="color: {'#22c55e' if stats['taux_conformite'] >= 80 else '#f59e0b' if stats['taux_conformite'] >= 50 else '#ef4444'};">
                    {'Conforme' if stats['taux_conformite'] >= 80 else 'En progression' if stats['taux_conformite'] >= 50 else 'Non conforme'}
                </span>
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with viz_col2:
        st.markdown(f"""
        <div style="background-color: {COLORS['background']}; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
            <h4 style="color: {COLORS['text']}; margin-top: 0; font-size: 1.1rem; font-weight: 500;">Distribution des statuts (5 niveaux)</h4>
        """, unsafe_allow_html=True)
        
        fig_pie = create_conformity_pie_chart(stats)
        st.plotly_chart(fig_pie, use_container_width=True, config={'displayModeBar': False}, key="status_distribution_pie")
        
        # Légende détaillée
        st.markdown(f"""
        <div style="margin-top: 1rem; display: grid; grid-template-columns: 1fr 1fr; gap: 0.5rem;">
            <div style="background: rgba(34, 197, 94, 0.1); padding: 0.5rem; border-radius: 6px; border-left: 3px solid #22c55e;">
                <span style="color: #22c55e; font-weight: bold;">{stats['conforme']}</span> Conforme
            </div>
            <div style="background: rgba(59, 130, 246, 0.1); padding: 0.5rem; border-radius: 6px; border-left: 3px solid #3b82f6;">
                <span style="color: #3b82f6; font-weight: bold;">{stats['largement_conforme']}</span> Largement
            </div>
            <div style="background: rgba(245, 158, 11, 0.1); padding: 0.5rem; border-radius: 6px; border-left: 3px solid #f59e0b;">
                <span style="color: #f59e0b; font-weight: bold;">{stats['partiellement_conforme']}</span> Partiellement
            </div>
            <div style="background: rgba(239, 68, 68, 0.1); padding: 0.5rem; border-radius: 6px; border-left: 3px solid #ef4444;">
                <span style="color: #ef4444; font-weight: bold;">{stats['faiblement_conforme']}</span> Faiblement
            </div>
        </div>
        <div style="background: rgba(107, 114, 128, 0.1); padding: 0.5rem; border-radius: 6px; border-left: 3px solid #6b7280; margin-top: 0.5rem;">
            <span style="color: #6b7280; font-weight: bold;">{stats['non_conforme']}</span> Non conforme
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === SECTION 4: ANALYSE PAR CATÉGORIE (fusionnée et optimisée) ===
    st.markdown(f"""
    <div style="background-color: {COLORS['surface']}; padding: 0.8rem 1.2rem 0.6rem 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; height: 60px; display: flex; align-items: center;">
        <h3 style="color: {COLORS['text']}; margin: 0; font-size: 1.3rem; font-weight: 600;">Analyse détaillée par catégorie ISO 27001</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Graphique combiné par catégorie
    category_col1, category_col2 = st.columns([2, 1])
    
    with category_col1:
        st.markdown(f"""
        <div style="background-color: {COLORS['background']}; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
            <h4 style="color: {COLORS['text']}; margin-top: 0; font-size: 1.1rem; font-weight: 500;">Performance par domaine de sécurité</h4>
        """, unsafe_allow_html=True)
        
        fig_bar = create_category_bar_chart(criteres)
        st.plotly_chart(fig_bar, use_container_width=True, config={'displayModeBar': False}, key="category_performance_bar")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with category_col2:
        st.markdown(f"""
        <div style="background-color: {COLORS['background']}; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
            <h4 style="color: {COLORS['text']}; margin-top: 0; font-size: 1.1rem; font-weight: 500;">Scores par catégorie</h4>
        """, unsafe_allow_html=True)
        
        # Calculer les stats par catégorie
        categories = ['Organisationnelle', 'Personnel', 'Physique', 'Technologique']
        
        for cat in categories:
            cat_criteres = [c for c in criteres if c['categorie'] == cat]
            total_cat = len(cat_criteres)
            conforme_cat = len([c for c in cat_criteres if c['statut'] in ['Conforme', 'Largement conforme']])
            percentage = round((conforme_cat / total_cat * 100) if total_cat > 0 else 0, 1)
            
            # Couleur basée sur le score
            color = COLORS['success'] if percentage >= 80 else COLORS['warning'] if percentage >= 50 else COLORS['danger']
            
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, {color}22 0%, {color}11 100%); 
                        padding: 1rem; border-radius: 8px; margin-bottom: 0.8rem;
                        border-left: 4px solid {color};">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <span style="color: {COLORS['text']}; font-weight: 600;">{cat}</span>
                    <span style="color: {color}; font-weight: bold; font-size: 1.1rem;">{percentage}%</span>
                </div>
                <div style="background-color: rgba(0,0,0,0.1); height: 6px; border-radius: 3px; margin-top: 0.5rem;">
                    <div style="background-color: {color}; height: 100%; width: {percentage}%; border-radius: 3px; transition: width 0.3s ease;"></div>
                </div>
                <p style="color: {COLORS['text_secondary']}; font-size: 0.8rem; margin: 0.3rem 0 0 0;">
                    {conforme_cat}/{total_cat} critères conformes
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === SECTION 5: SUIVI TEMPOREL ET TENDANCES ===
    st.markdown(f"""
    <div style="background-color: {COLORS['surface']}; padding: 0.8rem 1.2rem 0.6rem 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; height: 60px; display: flex; align-items: center;">
        <h3 style="color: {COLORS['text']}; margin: 0; font-size: 1.3rem; font-weight: 600;">Évolution et tendances</h3>
    </div>
    """, unsafe_allow_html=True)
    
    # Graphique temporel (simulé pour l'exemple)
    trend_col1, trend_col2 = st.columns(2)
    
    with trend_col1:
        st.markdown(f"""
        <div style="background-color: {COLORS['background']}; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
            <h4 style="color: {COLORS['text']}; margin-top: 0; font-size: 1.1rem; font-weight: 500;">Évolution du score de conformité</h4>
        """, unsafe_allow_html=True)
        
        # Créer un graphique de tendance simple
        import plotly.express as px
        import pandas as pd
        
        # Données simulées d'évolution
        trend_data = pd.DataFrame({
            'Mois': ['Jan', 'Fév', 'Mar', 'Avr', 'Mai', 'Jun'],
            'Score': [65, 68, 72, 75, 78, stats['taux_conformite']]
        })
        
        fig_trend = px.line(trend_data, x='Mois', y='Score', 
                           title="", 
                           line_shape='spline',
                           markers=True)
        fig_trend.update_traces(line_color=COLORS['primary'], marker_size=8)
        fig_trend.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font_color=COLORS['text'],
            showlegend=False,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        fig_trend.add_hline(y=80, line_dash="dash", line_color=COLORS['success'], 
                           annotation_text="Objectif ISO 27001")
        
        st.plotly_chart(fig_trend, use_container_width=True, config={'displayModeBar': False}, key="trend_evolution_chart")
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with trend_col2:
        st.markdown(f"""
            <div style="background-color: {COLORS['background']}; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
                <h4 style="color: {COLORS['text']}; margin-top: 0; font-size: 1.1rem; font-weight: 500;">Indicateurs de performance</h4>
        """, unsafe_allow_html=True)
        
        # Métriques de performance
        performance_metrics = [
            {"label": "Amélioration ce mois", "value": "+5.2%", "icon": "", "color": COLORS['success']},
            {"label": "Délai moyen correction", "value": "12 jours", "icon": "", "color": COLORS['info']},
            {"label": "Audits planifiés", "value": "3", "icon": "", "color": COLORS['warning']},
            {"label": "Actions en cours", "value": "8", "icon": "", "color": COLORS['primary']}
        ]
        
        for metric in performance_metrics:
                st.markdown(f"""
                <div style="background: linear-gradient(90deg, {metric['color']}15 0%, transparent 100%); 
                            padding: 0.8rem; border-radius: 8px; margin-bottom: 0.8rem;
                            border-left: 3px solid {metric['color']};">
                    <div style="display: flex; justify-content: between; align-items: center;">
                        <span style="font-size: 1.2rem; margin-right: 0.5rem;">{metric['icon']}</span>
                        <div style="flex: 1;">
                            <div style="color: {COLORS['text']}; font-size: 0.85rem;">{metric['label']}</div>
                            <div style="color: {metric['color']}; font-weight: bold; font-size: 1.1rem;">{metric['value']}</div>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # === SECTION 6: ACTIONS PRIORITAIRES ET SURVEILLANCE ===
    st.markdown(f"""
    <div style="background-color: {COLORS['surface']}; padding: 0.8rem 1.2rem 0.6rem 1.2rem; border-radius: 12px; margin-bottom: 1.5rem; height: 60px; display: flex; align-items: center;">
        <h3 style="color: {COLORS['text']}; margin: 0; font-size: 1.3rem; font-weight: 600;">Actions prioritaires et surveillance</h3>
    </div>
    """, unsafe_allow_html=True)
    
    action_col1, action_col2 = st.columns(2)
    
    with action_col1:
        st.markdown(f"""
        <div style="background-color: {COLORS['background']}; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
            <h4 style="color: {COLORS['text']}; margin-top: 0; font-size: 1.1rem; font-weight: 500;"> Points d'attention critiques</h4>
        """, unsafe_allow_html=True)
        
        # Analyser les critères critiques
        non_conformes = [c for c in criteres if c['statut'] == 'Non conforme']
        faiblement_conformes = [c for c in criteres if c['statut'] == 'Faiblement conforme']
        
        if non_conformes:
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, {COLORS['danger']}15 0%, transparent 100%); 
                        padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['danger']}; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">🔴</span>
                    <span style="color: {COLORS['danger']}; font-weight: bold;">
                        {len(non_conformes)} critère(s) non conforme(s)
                    </span>
                </div>
                <p style="color: {COLORS['text_secondary']}; font-size: 0.85rem; margin: 0;">
                    Action immédiate requise - Impact élevé sur la certification
                </p>
                <button style="background: {COLORS['danger']}; color: white; border: none; padding: 0.3rem 0.8rem; 
                               border-radius: 4px; font-size: 0.8rem; margin-top: 0.5rem; cursor: pointer;">
                    Voir détails →
                </button>
            </div>
            """, unsafe_allow_html=True)
        
        if faiblement_conformes:
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, {COLORS['warning']}15 0%, transparent 100%); 
                        padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['warning']}; margin-bottom: 1rem;">
                <div style="display: flex; align-items: center; margin-bottom: 0.5rem;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">🟡</span>
                    <span style="color: {COLORS['warning']}; font-weight: bold;">
                        {len(faiblement_conformes)} critère(s) faiblement conforme(s)
                    </span>
                </div>
                <p style="color: {COLORS['text_secondary']}; font-size: 0.85rem; margin: 0;">
                    Amélioration recommandée sous 30 jours
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        if not non_conformes and not faiblement_conformes:
            st.markdown(f"""
            <div style="background: linear-gradient(90deg, {COLORS['success']}15 0%, transparent 100%); 
                        padding: 1rem; border-radius: 8px; border-left: 4px solid {COLORS['success']};">
                <div style="display: flex; align-items: center;">
                    <span style="font-size: 1.2rem; margin-right: 0.5rem;">✅</span>
                    <span style="color: {COLORS['success']}; font-weight: bold;">
                        Aucun point critique détecté
                    </span>
                </div>
                <p style="color: {COLORS['text_secondary']}; font-size: 0.85rem; margin: 0.3rem 0 0 0;">
                    Excellente conformité - Maintenir les efforts
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    with action_col2:
        st.markdown(f"""
        <div style="background-color: {COLORS['background']}; padding: 1.5rem; border-radius: 12px; box-shadow: 0 4px 16px rgba(0,0,0,0.1);">
            <h4 style="color: {COLORS['text']}; margin-top: 0; font-size: 1.1rem; font-weight: 500;"> Dernières activités</h4>
        """, unsafe_allow_html=True)
        
        if audits:
            for i, audit in enumerate(audits[:3]):  # Afficher les 3 derniers audits
                score_color = COLORS['success'] if audit.get('score', 0) >= 80 else COLORS['warning'] if audit.get('score', 0) >= 50 else COLORS['danger']
                
                st.markdown(f"""
                <div style="background: linear-gradient(90deg, {score_color}10 0%, transparent 100%); 
                            padding: 1rem; border-radius: 8px; margin-bottom: 0.8rem; 
                            border-left: 3px solid {score_color};">
                    <div style="display: flex; justify-content: space-between; align-items: start;">
                        <div style="flex: 1;">
                            <p style="color: {COLORS['text']}; font-weight: 600; margin: 0 0 0.3rem 0; font-size: 0.9rem;">
                                {audit['titre']}
                            </p>
                            <p style="color: {COLORS['text_secondary']}; font-size: 0.75rem; margin: 0 0 0.3rem 0;">
                                {format_date(audit['date_audit'])} • {audit['auditeur']}
                            </p>
                        </div>
                        <div style="background: {score_color}; color: white; padding: 0.2rem 0.5rem; 
                                    border-radius: 12px; font-size: 0.75rem; font-weight: bold;">
                            {audit.get('score', 0)}%
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("Aucun audit enregistré pour le moment.")
        
        # Actions recommandées
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {COLORS['info']}15 0%, {COLORS['primary']}10 100%); 
                    padding: 1rem; border-radius: 8px; margin-top: 1rem;">
            <p style="color: {COLORS['info']}; font-weight: bold; margin: 0 0 0.8rem 0; display: flex; align-items: center;">
                <span style="font-size: 1.1rem; margin-right: 0.5rem;">💡</span>
                Recommandations stratégiques
            </p>
            <div style="color: {COLORS['text_secondary']}; font-size: 0.85rem;">
                <div style="margin-bottom: 0.4rem;">• Planifier audit Q1 2025</div>
                <div style="margin-bottom: 0.4rem;">• Réviser documentation technique</div>
                <div style="margin-bottom: 0.4rem;">• Formation équipes sécurité</div>
                <div>• Mise à jour analyses de risques</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("</div>", unsafe_allow_html=True)
    
    # === FOOTER AVEC MÉTADONNÉES ===
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background: linear-gradient(90deg, {COLORS['surface']} 0%, {COLORS['background']} 100%);
                padding: 1.5rem; border-radius: 12px; text-align: center;">
        <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(200px, 1fr)); gap: 1rem; margin-bottom: 1rem;">
            <div>
                <span style="color: {COLORS['text_secondary']}; font-size: 0.8rem;">Dernière mise à jour</span><br>
                <span style="color: {COLORS['text']}; font-weight: 600;">{format_date(st.session_state.get('last_update', '2025-01-15'))}</span>
            </div>
            <div>
                <span style="color: {COLORS['text_secondary']}; font-size: 0.8rem;">Prochaine évaluation</span><br>
                <span style="color: {COLORS['warning']}; font-weight: 600;">28 Novembre 2025</span>
            </div>
            <div>
                <span style="color: {COLORS['text_secondary']}; font-size: 0.8rem;">Certification ISO 27001</span><br>
                <span style="color: {COLORS['success']}; font-weight: 600;">En cours</span>
            </div>
        </div>
        <div style="color: {COLORS['text_secondary']}; font-size: 0.75rem; border-top: 1px solid {COLORS['text_secondary']}33; padding-top: 1rem;">
            Sécurité 360 - Système de gestion ISO 27001 | Tableau de bord intelligent v2.0
        </div>
    </div>
    """, unsafe_allow_html=True)