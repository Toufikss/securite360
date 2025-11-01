"""
Page des paramètres - Sécurité 360
Configuration du système (Admin uniquement)
"""

import streamlit as st
from utils.helpers import display_page_header
from utils.config import COLORS, APP_NAME, APP_VERSION

def show(auth, db):
    """Affiche la page des paramètres"""
    
    # Vérifier les permissions
    auth.require_role("Admin")
    
    # En-tête
    display_page_header(
        "Paramètres",
        "Configuration et personnalisation du système"
    )
    
    # Tabs
    tab1, tab2, tab3, tab4 = st.tabs(["🎨 Apparence", "🔧 Système", "💾 Sauvegarde", "ℹ️ À propos"])
    
    with tab1:
        st.markdown("###  Personnalisation de l'apparence")
        
        with st.form("apparence_form"):
            company_name = st.text_input(
                "Nom de l'organisation",
                value=db.get_setting("company_name") or "Sécurité 360",
                help="Nom affiché dans l'application"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                theme_color = st.color_picker(
                    "Couleur principale",
                    value=db.get_setting("theme_color") or COLORS['primary']
                )
            
            with col2:
                # Upload du logo
                logo_file = st.file_uploader(
                    "Logo de l'organisation",
                    type=['png', 'jpg', 'jpeg'],
                    help="Format recommandé: PNG, taille max 2MB"
                )
            
            if st.form_submit_button("💾 Enregistrer les modifications", use_container_width=True, type="primary"):
                db.update_setting("company_name", company_name)
                db.update_setting("theme_color", theme_color)
                
                if logo_file:
                    # Sauvegarder le logo (simulation)
                    logo_path = f"assets/{logo_file.name}"
                    db.update_setting("logo_path", logo_path)
                
                st.success("✅ Paramètres d'apparence enregistrés!")
                st.rerun()
        
        # Aperçu
        st.markdown("####  Aperçu")
        st.markdown(f"""
        <div style="background: linear-gradient(135deg, {theme_color}, {COLORS['secondary']}); padding: 2rem; border-radius: 12px; text-align: center;">
            <h2 style="color: white; margin: 0;">{company_name}</h2>
            <p style="color: rgba(255,255,255,0.8); margin: 0.5rem 0 0 0;">Système de gestion ISO 27001</p>
        </div>
        """, unsafe_allow_html=True)
    
    with tab2:
        st.markdown("### 🔧 Configuration du système")
        
        with st.form("system_form"):
            st.markdown("#### Paramètres de sécurité")
            
            col1, col2 = st.columns(2)
            
            with col1:
                session_timeout = st.number_input(
                    "Délai d'expiration de session (minutes)",
                    min_value=5,
                    max_value=480,
                    value=30,
                    help="Durée avant déconnexion automatique"
                )
            
            with col2:
                password_expiry = st.number_input(
                    "Expiration des mots de passe (jours)",
                    min_value=30,
                    max_value=365,
                    value=90,
                    help="Fréquence de renouvellement des mots de passe"
                )
            
            st.markdown("#### Notifications")
            
            col1, col2 = st.columns(2)
            
            with col1:
                email_notifications = st.checkbox(
                    "Activer les notifications par email",
                    value=False,
                    help="Alertes pour les non-conformités et audits"
                )
            
            with col2:
                admin_email = st.text_input(
                    "Email de l'administrateur",
                    placeholder="admin@exemple.com"
                )
            
            st.markdown("#### Rapports automatiques")
            
            auto_reports = st.checkbox(
                "Générer des rapports automatiques",
                value=False,
                help="Rapports de conformité mensuels"
            )
            
            if auto_reports:
                report_frequency = st.selectbox(
                    "Fréquence",
                    ["Hebdomadaire", "Mensuel", "Trimestriel"]
                )
            
            st.markdown("#### Journalisation")
            
            col1, col2 = st.columns(2)
            
            with col1:
                log_level = st.selectbox(
                    "Niveau de journalisation",
                    ["Info", "Warning", "Error", "Debug"]
                )
            
            with col2:
                log_retention = st.number_input(
                    "Rétention des logs (jours)",
                    min_value=30,
                    max_value=730,
                    value=365
                )
            
            if st.form_submit_button("💾 Enregistrer la configuration", use_container_width=True, type="primary"):
                st.success("✅ Configuration système enregistrée!")
                st.info("Note: Certains paramètres nécessitent un redémarrage pour prendre effet")
    
    with tab3:
        st.markdown("### 💾 Sauvegarde et restauration")
        
        st.markdown(f"""
        <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <h4 style="color: {COLORS['text']}; margin-top: 0;">Sauvegarde de la base de données</h4>
            <p style="color: {COLORS['text_secondary']};">
                Créez une sauvegarde complète de toutes les données de l'application.
                Incluant les utilisateurs, critères, audits et documents.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            if st.button("📥 Sauvegarder la base de données", use_container_width=True, type="primary"):
                import sqlite3
                import shutil
                from datetime import datetime
                
                try:
                    # Créer une copie de la base de données
                    backup_filename = f"backup_securite360_{datetime.now().strftime('%Y%m%d_%H%M%S')}.db"
                    shutil.copy2("securite360.db", backup_filename)
                    
                    with open(backup_filename, 'rb') as f:
                        st.download_button(
                            label="📥 Télécharger la sauvegarde",
                            data=f,
                            file_name=backup_filename,
                            mime="application/octet-stream",
                            use_container_width=True
                        )
                    
                    st.success(f"✅ Sauvegarde créée: {backup_filename}")
                except Exception as e:
                    st.error(f"❌ Erreur lors de la sauvegarde: {str(e)}")
        
        with col2:
            st.markdown("**Dernière sauvegarde:**")
            st.info("Aucune sauvegarde enregistrée")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
            <h4 style="color: {COLORS['text']}; margin-top: 0;">Restauration de la base de données</h4>
            <p style="color: {COLORS['text_secondary']};">
                Restaurez une sauvegarde précédente. <strong>Attention:</strong> Cette opération 
                remplacera toutes les données actuelles.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        uploaded_backup = st.file_uploader(
            "Sélectionner un fichier de sauvegarde",
            type=['db'],
            help="Fichier .db généré par l'outil de sauvegarde"
        )
        
        if uploaded_backup:
            st.warning("⚠️ La restauration écrasera toutes les données actuelles. Cette action est irréversible.")
            
            col1, col2 = st.columns([1, 3])
            with col1:
                if st.button("♻️ Restaurer", type="primary", use_container_width=True):
                    st.error("Fonction de restauration désactivée pour des raisons de sécurité dans cette démo")
        
        # Export CSV
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown(f"""
        <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px;">
            <h4 style="color: {COLORS['text']}; margin-top: 0;">Export des données</h4>
            <p style="color: {COLORS['text_secondary']};">
                Exportez les données au format CSV pour analyse externe.
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("📊 Exporter les critères", use_container_width=True):
                criteres = db.get_all_criteres()
                import pandas as pd
                df = pd.DataFrame(criteres)
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    "📥 Télécharger CSV",
                    csv,
                    "criteres_export.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        with col2:
            if st.button("📋 Exporter les audits", use_container_width=True):
                audits = db.get_all_audits()
                import pandas as pd
                df = pd.DataFrame(audits)
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    "📥 Télécharger CSV",
                    csv,
                    "audits_export.csv",
                    "text/csv",
                    use_container_width=True
                )
        
        with col3:
            if st.button("⚙️ Exporter les directives", use_container_width=True):
                directives = db.get_all_directives()
                import pandas as pd
                df = pd.DataFrame(directives)
                csv = df.to_csv(index=False, encoding='utf-8-sig')
                st.download_button(
                    "📥 Télécharger CSV",
                    csv,
                    "directives_export.csv",
                    "text/csv",
                    use_container_width=True
                )
    
    with tab4:
        st.markdown("### ℹ️ À propos de l'application")
        
        st.markdown(f"""
            <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px;">
                <h4 style="color: {COLORS['text']}; margin-top: 0;">📋 Informations</h4>
                <p style="color: {COLORS['text_secondary']}; margin: 0.5rem 0;">
                    <strong>Application:</strong> {APP_NAME}<br>
                    <strong>Version:</strong> {APP_VERSION}<br>
                    <strong>Date de sortie:</strong> Janvier 2025<br>
                    <strong>Licence:</strong> Propriétaire<br>
                    <strong>Norme:</strong> ISO/IEC 27001:2022
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown(f"""
            <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px;">
                <h4 style="color: {COLORS['text']}; margin-top: 0;">🛠️ Technologies</h4>
                <p style="color: {COLORS['text_secondary']}; margin: 0.5rem 0;">
                    <strong>Framework:</strong> Streamlit 1.31<br>
                    <strong>Base de données:</strong> SQLite3<br>
                    <strong>Graphiques:</strong> Plotly<br>
                    <strong>Rapports:</strong> ReportLab<br>
                    <strong>Sécurité:</strong> Bcrypt
                </p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px;">
            <h4 style="color: {COLORS['text']}; margin-top: 0;">📚 Description</h4>
            <p style="color: {COLORS['text']}; line-height: 1.8;">
                {APP_NAME} est une solution complète de gestion de la conformité ISO 27001. 
                L'application permet aux organisations de gérer efficacement leur Système de 
                Management de la Sécurité de l'Information (SMSI) en offrant:
            </p>
            <ul style="color: {COLORS['text']}; line-height: 1.8;">
                <li>Gestion complète des 93 critères de l'Annexe A</li>
                <li>Planification et suivi des audits internes</li>
                <li>Génération automatique de rapports PDF</li>
                <li>Tableaux de bord interactifs</li>
                <li>Gestion documentaire intégrée</li>
                <li>Contrôle d'accès basé sur les rôles</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        st.markdown(f"""
        <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px;">
            <h4 style="color: {COLORS['text']}; margin-top: 0;">📞 Support</h4>
            <p style="color: {COLORS['text_secondary']};">
                Pour toute question ou assistance technique, veuillez contacter:
            </p>
            <p style="color: {COLORS['text']};">
                <strong>Email:</strong> support@securite360.com<br>
                <strong>Documentation:</strong> https://docs.securite360.com<br>
                <strong>Hotline:</strong> 0559750403
            </p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # Informations système
        with st.expander("🔍 Informations système"):
            import platform
            import sys
            
            st.code(f"""
Système d'exploitation: {platform.system()} {platform.release()}
Architecture: {platform.machine()}
Python: {sys.version.split()[0]}
Streamlit: 1.31.0
Base de données: SQLite3
            """)
        
        # Copyright
        st.markdown(f"""
        <div style="text-align: center; color: {COLORS['text_secondary']}; padding: 2rem; margin-top: 2rem; border-top: 1px solid {COLORS['text_secondary']};">
            <p style="margin: 0;">© 2025 {APP_NAME}. Tous droits réservés.</p>
            <p style="margin: 0.5rem 0 0 0; font-size: 0.85rem;">
                Développé avec ❤️ pour la sécurité de l'information
            </p>
        </div>
        """, unsafe_allow_html=True)