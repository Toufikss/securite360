"""
Page de génération de rapports - Sécurité 360
Export et historique des rapports de conformité
"""

import streamlit as st
from utils.helpers import display_page_header, format_date
from utils.config import COLORS
from utils.pdf_generator import PDFGenerator
from datetime import datetime

def show(auth, db):
    """Affiche la page de génération de rapports"""
    
    # Masquer tous les éléments de debug
    st.markdown("""
    <style>
        /* Masquer les affichages JSON/debug de Streamlit */
        .react-json-view,
        .pretty-json-container,
        .object-key-val,
        .variable-row,
        .object-container,
        .pushed-content,
        .copy-to-clipboard-container,
        .object-content,
        .brace-row {
            display: none !important;
            visibility: hidden !important;
            opacity: 0 !important;
            height: 0 !important;
            width: 0 !important;
            overflow: hidden !important;
        }
        
        /* Masquer les éléments avec classes de debug */
        [class*="debug"],
        [class*="json-viewer"],
        [data-testid*="debug"] {
            display: none !important;
        }
        
        /* Masquer spécifiquement les éléments contenant "Debug" */
        div:has([class*="stMarkdownContainer"]) {
            display: contents;
        }
        
        div[data-testid="stMarkdownContainer"]:has-text("Debug") {
            display: none !important;
        }
    </style>
    
    <script>
        // Supprimer tout élément JSON viewer et debug
        function removeDebugElements() {
            // Cibler spécifiquement les viewers JSON
            const jsonViewers = document.querySelectorAll('.react-json-view, .pretty-json-container, .object-key-val, .variable-row');
            jsonViewers.forEach(el => {
                el.style.display = 'none';
                el.style.visibility = 'hidden';
                el.style.opacity = '0';
                el.style.height = '0';
                el.style.width = '0';
                el.style.overflow = 'hidden';
                // Supprimer aussi les parents
                if (el.parentElement) {
                    el.parentElement.style.display = 'none';
                }
            });
            
            // Chercher les éléments contenant les données de statistiques
            const allElements = document.querySelectorAll('*');
            allElements.forEach(el => {
                if (el.textContent && (
                    el.textContent.includes('conforme') ||
                    el.textContent.includes('largement_conforme') ||
                    el.textContent.includes('taux_conformite')
                )) {
                    // Vérifier si c'est un viewer JSON et non pas nos métriques
                    if (el.classList.contains('react-json-view') || 
                        el.classList.contains('object-key') ||
                        el.closest('.react-json-view') ||
                        el.closest('.object-key-val')) {
                        el.style.display = 'none';
                        if (el.parentElement) {
                            el.parentElement.style.display = 'none';
                        }
                    }
                }
                
                if (el.textContent && el.textContent.includes('Debug - Statistiques')) {
                    el.style.display = 'none';
                    if (el.parentElement) {
                        el.parentElement.style.display = 'none';
                    }
                }
            });
        }
        
        // Exécuter immédiatement et avec un observer
        setTimeout(removeDebugElements, 100);
        setInterval(removeDebugElements, 500);
        
        // Observer pour les nouveaux éléments
        const observer = new MutationObserver(removeDebugElements);
        observer.observe(document.body, { 
            childList: true, 
            subtree: true,
            characterData: true
        });
    </script>
    </style>
    """, unsafe_allow_html=True)
    
    # En-tête
    display_page_header(
        "Rapports",
        "Génération et export des rapports de conformité"
    )
    
    # Tabs
    tab1, tab2 = st.tabs(["📊 Générer un rapport", "📚 Historique"])
    
    with tab1:
        st.markdown("###  Générer un nouveau rapport")
        
        # Sélection du type de rapport
        col1, col2 = st.columns(2)
        
        with col1:
            type_rapport = st.selectbox(
                "Type de rapport",
                [
                    "Rapport de conformité global",
                    "Rapport d'audit",
                    "Rapport par catégorie",
                    "Rapport des non-conformités"
                ]
            )
        
        with col2:
            format_export = st.selectbox(
                "Format d'export",
                ["PDF", "CSV", "Excel (à venir)"]
            )
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Aperçu et génération selon le type
        if type_rapport == "Rapport de conformité global":
            st.markdown(f"""
            <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                <h4 style="color: {COLORS['text']}; margin-top: 0;">📄 Rapport de conformité global</h4>
                <p style="color: {COLORS['text_secondary']};">
                    Ce rapport inclut :
                </p>
                <ul style="color: {COLORS['text_secondary']};">
                    <li>Vue d'ensemble de la conformité</li>
                    <li>Statistiques par catégorie</li>
                    <li>Liste des critères non conformes</li>
                    <li>Recommandations d'amélioration</li>
                    <li>Graphiques et indicateurs clés</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
            # Récupérer les données
            stats = db.get_conformity_stats()
            criteres = db.get_all_criteres()
            
            # Éviter tout affichage automatique de debug
            _ = None  # Ligne pour éviter l'affichage automatique
            
            # Forcer la suppression de tout affichage JSON automatique
            st.markdown("""
            <script>
                // Supprimer immédiatement tous les viewers JSON et debug
                function removeAllDebugElements() {
                    // Supprimer les viewers JSON
                    const jsonElements = document.querySelectorAll('.react-json-view, .pretty-json-container, .object-key-val');
                    jsonElements.forEach(el => {
                        el.remove();
                        if (el.parentElement) el.parentElement.remove();
                    });
                    
                    // Supprimer spécifiquement le texte de debug
                    const allElements = document.querySelectorAll('*');
                    allElements.forEach(el => {
                        if (el.textContent && (
                            el.textContent.includes('🔍 Debug - Statistiques récupérées') ||
                            el.textContent.includes('Debug - Statistiques récupérées') ||
                            (el.textContent.includes('conforme') && el.textContent.includes('largement_conforme') && el.textContent.includes('taux_conformite'))
                        )) {
                            // Vérifier si c'est bien un élément de debug et pas nos métriques
                            if (!el.closest('[data-testid="metric-container"]') && 
                                !el.closest('.metric') &&
                                (el.classList.contains('react-json-view') || 
                                 el.textContent.includes('Debug') ||
                                 el.textContent.includes('🔍'))) {
                                el.remove();
                                if (el.parentElement) el.parentElement.remove();
                            }
                        }
                    });
                }
                
                // Exécuter immédiatement et répéter
                setTimeout(removeAllDebugElements, 10);
                setTimeout(removeAllDebugElements, 50);
                setTimeout(removeAllDebugElements, 100);
                setTimeout(removeAllDebugElements, 500);
            </script>
            """, unsafe_allow_html=True)
            
            # Aperçu des statistiques - Taux global
            col1, col2 = st.columns(2)
            
            with col1:
                st.metric("Taux de conformité pondéré", f"{stats['taux_conformite']}%")
            with col2:
                st.metric("Total des critères", stats['total'])
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Répartition des 5 statuts de conformité - Design professionnel
            st.markdown("### Répartition par statut de conformité")
            
            # CSS pour styliser les métriques
            st.markdown("""
            <style>
                .status-metrics {
                    background: none !important;
                }
                
                /* Styliser les conteneurs de métriques */
                [data-testid="metric-container"] {
                    background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
                    border: 1px solid #cbd5e1;
                    padding: 1rem;
                    border-radius: 8px;
                    box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
                    transition: transform 0.2s ease;
                }
                
                [data-testid="metric-container"]:hover {
                    transform: translateY(-2px);
                    box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
                }
                
                /* Couleurs spécifiques par statut */
                [data-testid="metric-container"]:nth-child(1) {
                    background: linear-gradient(135deg, #dbeafe 0%, #bfdbfe 100%);
                    border-color: #3b82f6;
                }
                
                [data-testid="metric-container"]:nth-child(2) {
                    background: linear-gradient(135deg, #dcfce7 0%, #bbf7d0 100%);
                    border-color: #059669;
                }
                
                [data-testid="metric-container"]:nth-child(3) {
                    background: linear-gradient(135deg, #fed7aa 0%, #fdba74 100%);
                    border-color: #d97706;
                }
                
                [data-testid="metric-container"]:nth-child(4) {
                    background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
                    border-color: #ea580c;
                }
                
                [data-testid="metric-container"]:nth-child(5) {
                    background: linear-gradient(135deg, #fecaca 0%, #f87171 100%);
                    border-color: #dc2626;
                }
                
                /* Style des valeurs et labels */
                [data-testid="metric-container"] [data-testid="stMetricValue"] {
                    font-size: 2.5rem !important;
                    font-weight: 700 !important;
                }
                
                [data-testid="metric-container"] [data-testid="stMetricLabel"] {
                    font-size: 1rem !important;
                    font-weight: 600 !important;
                    text-transform: uppercase;
                    letter-spacing: 0.5px;
                }
            </style>
            """, unsafe_allow_html=True)
            
            # Affichage des 5 métriques avec design professionnel
            col1, col2, col3, col4, col5 = st.columns(5)
            
            with col1:
                st.metric("CONFORME", stats['conforme'], help="Niveau 5 • 100% - Pleinement satisfaisant")
            with col2:
                st.metric("LARGEMENT CONFORME", stats['largement_conforme'], help="Niveau 4 • 80% - Très satisfaisant")
            with col3:
                st.metric("PARTIELLEMENT CONFORME", stats['partiellement_conforme'], help="Niveau 3 • 50% - Améliorations nécessaires")
            with col4:
                st.metric("FAIBLEMENT CONFORME", stats['faiblement_conforme'], help="Niveau 2 • 30% - Efforts importants requis")
            with col5:
                st.metric("NON CONFORME", stats['non_conforme'], help="Niveau 1 • 0% - Action immédiate requise")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            # Bouton de génération
            if st.button("📥 Générer le rapport PDF", type="primary", use_container_width=True):
                with st.spinner("Génération du rapport en cours..."):
                    try:
                        pdf_generator = PDFGenerator()
                        pdf_data = pdf_generator.generate_conformity_report(stats, criteres)
                        
                        filename = f"rapport_conformite_{datetime.now().strftime('%Y%m%d_%H%M%S')}.pdf"
                        
                        st.download_button(
                            label="📥 Télécharger le rapport PDF",
                            data=pdf_data,
                            file_name=filename,
                            mime="application/pdf",
                            use_container_width=True
                        )
                        
                        st.success("✅ Rapport généré avec succès!")
                    except Exception as e:
                        st.error(f"❌ Erreur lors de la génération du rapport: {str(e)}")
        
        elif type_rapport == "Rapport d'audit":
            st.markdown(f"""
            <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                <h4 style="color: {COLORS['text']}; margin-top: 0;">📄 Rapport d'audit</h4>
                <p style="color: {COLORS['text_secondary']};">
                    Sélectionnez un audit pour générer son rapport détaillé.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            audits = db.get_all_audits()
            
            if audits:
                audit_options = {f"{a['titre']} - {format_date(a['date_audit'])}": a['id'] for a in audits}
                selected_audit = st.selectbox("Sélectionner un audit", list(audit_options.keys()))
                
                if selected_audit:
                    audit_id = audit_options[selected_audit]
                    audit = db.get_audit_by_id(audit_id)
                    
                    if audit:
                        st.markdown(f"""
                        <div style="background-color: {COLORS['background']}; padding: 1rem; border-radius: 8px; margin: 1rem 0;">
                            <p style="color: {COLORS['text']}; margin: 0;"><strong>Titre:</strong> {audit['titre']}</p>
                            <p style="color: {COLORS['text']}; margin: 0.3rem 0;"><strong>Date:</strong> {format_date(audit['date_audit'])}</p>
                            <p style="color: {COLORS['text']}; margin: 0.3rem 0;"><strong>Auditeur:</strong> {audit['auditeur']}</p>
                            <p style="color: {COLORS['text']}; margin: 0.3rem 0;"><strong>Score:</strong> {audit.get('score', 0)}%</p>
                        </div>
                        """, unsafe_allow_html=True)
                        
                        if st.button("📥 Générer le rapport d'audit PDF", type="primary", use_container_width=True):
                            with st.spinner("Génération du rapport en cours..."):
                                try:
                                    pdf_generator = PDFGenerator()
                                    criteres = db.get_all_criteres()
                                    pdf_data = pdf_generator.generate_audit_report(audit, criteres)
                                    
                                    filename = f"rapport_audit_{audit_id}_{datetime.now().strftime('%Y%m%d')}.pdf"
                                    
                                    st.download_button(
                                        label="📥 Télécharger le rapport d'audit PDF",
                                        data=pdf_data,
                                        file_name=filename,
                                        mime="application/pdf",
                                        use_container_width=True
                                    )
                                    
                                    st.success("✅ Rapport d'audit généré avec succès!")
                                except Exception as e:
                                    st.error(f"❌ Erreur lors de la génération: {str(e)}")
            else:
                st.info("Aucun audit disponible pour générer un rapport")
        
        elif type_rapport == "Rapport par catégorie":
            st.markdown(f"""
            <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                <h4 style="color: {COLORS['text']}; margin-top: 0;">📄 Rapport par catégorie</h4>
                <p style="color: {COLORS['text_secondary']};">
                    Analyse détaillée de la conformité par catégorie ISO 27001.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            categories = ['Organisationnelle', 'Personnel', 'Physique', 'Technologique']
            selected_cat = st.selectbox("Sélectionner une catégorie", categories)
            
            criteres = db.get_all_criteres()
            criteres_cat = [c for c in criteres if c['categorie'] == selected_cat]
            
            # Statistiques de la catégorie
            total_cat = len(criteres_cat)
            conforme_cat = len([c for c in criteres_cat if c['statut'] == 'Conforme'])
            partiel_cat = len([c for c in criteres_cat if c['statut'] == 'Partiellement conforme'])
            non_conforme_cat = len([c for c in criteres_cat if c['statut'] == 'Non conforme'])
            taux_cat = round((conforme_cat / total_cat * 100) if total_cat > 0 else 0, 2)
            
            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("Total", total_cat)
            with col2:
                st.metric("Conformes", conforme_cat)
            with col3:
                st.metric("Partiels", partiel_cat)
            with col4:
                st.metric("Non conformes", non_conforme_cat)
            
            st.markdown("<br>", unsafe_allow_html=True)
            st.info(f"Taux de conformité pour {selected_cat}: {taux_cat}%")
            
            if st.button("📥 Générer le rapport par catégorie", type="primary", use_container_width=True):
                st.info("Génération de rapport par catégorie (fonctionnalité à implémenter)")
        
        else:  # Rapport des non-conformités
            st.markdown(f"""
            <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                <h4 style="color: {COLORS['text']}; margin-top: 0;">📄 Rapport des non-conformités</h4>
                <p style="color: {COLORS['text_secondary']};">
                    Liste détaillée des critères nécessitant une action corrective.
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            criteres = db.get_all_criteres()
            non_conformes = [c for c in criteres if c['statut'] == 'Non conforme']
            partiels = [c for c in criteres if c['statut'] == 'Partiellement conforme']
            
            col1, col2 = st.columns(2)
            with col1:
                st.metric("Critères non conformes", len(non_conformes))
            with col2:
                st.metric("Critères partiellement conformes", len(partiels))
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if non_conformes or partiels:
                # Afficher un aperçu
                with st.expander("👁️ Aperçu des non-conformités"):
                    for nc in non_conformes[:5]:
                        st.markdown(f"- **{nc['code']}**: {nc['titre']}")
                
                if st.button("📥 Générer le rapport des non-conformités", type="primary", use_container_width=True):
                    st.info("Génération de rapport des non-conformités (fonctionnalité à implémenter)")
            else:
                st.success("✅ Aucune non-conformité à signaler!")
    
    with tab2:
        st.markdown("### 📚 Historique des rapports")
        
        st.info("L'historique des rapports générés sera affiché ici (fonctionnalité à implémenter)")
        
        # Exemple d'historique (simulation)
        rapports_exemple = [
            {
                "titre": "Rapport de conformité global",
                "date": "2025-01-15",
                "type": "PDF",
                "auteur": "admin",
                "taille": "245 KB"
            },
            {
                "titre": "Rapport d'audit Q4 2024",
                "date": "2024-12-20",
                "type": "PDF",
                "auteur": "audit01",
                "taille": "189 KB"
            },
            {
                "titre": "Rapport par catégorie - Technologique",
                "date": "2024-12-15",
                "type": "PDF",
                "auteur": "admin",
                "taille": "156 KB"
            }
        ]
        
        for rapport in rapports_exemple:
            st.markdown(f"""
            <div style="background-color: {COLORS['surface']}; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <div style="display: flex; justify-content: space-between; align-items: center;">
                    <div>
                        <p style="color: {COLORS['text']}; font-weight: bold; margin: 0;">{rapport['titre']}</p>
                        <p style="color: {COLORS['text_secondary']}; font-size: 0.85rem; margin: 0.3rem 0 0 0;">
                            {format_date(rapport['date'])} | Par: {rapport['auteur']} | {rapport['taille']}
                        </p>
                    </div>
                    <div>
                        <span style="background-color: {COLORS['primary']}; color: white; padding: 0.3rem 0.6rem; border-radius: 12px; font-size: 0.8rem;">
                            {rapport['type']}
                        </span>
                    </div>
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Aide
    with st.expander("ℹ️ Aide sur les rapports"):
        st.markdown("#### Types de rapports disponibles :")
        
        st.markdown("##### Rapport de conformité global")
        st.markdown("""
        Document complet incluant toutes les statistiques de conformité, l'analyse par catégorie,
        et les recommandations. Idéal pour les revues de direction.
        """)
        
        st.markdown("##### Rapport d'audit")
        st.markdown("""
        Rapport détaillé d'un audit spécifique avec les constats, observations et plan d'action.
        Utilisé pour documenter les audits internes.
        """)
        
        st.markdown("##### Rapport par catégorie")
        st.markdown("""
        Analyse approfondie d'une catégorie spécifique (Organisationnelle, Personnel, Physique, Technologique).
        Utile pour les responsables de domaine.
        """)
        
        st.markdown("##### Rapport des non-conformités")
        st.markdown("""
        Liste exhaustive des points nécessitant une action corrective. Sert de base pour les plans d'action.
        """)
        
        st.markdown("#### Bonnes pratiques :")
        st.markdown("""
        - Générer des rapports régulièrement (mensuel/trimestriel)
        - Conserver l'historique des rapports
        - Partager les rapports avec les parties prenantes
        - Suivre l'évolution des indicateurs dans le temps
        """)