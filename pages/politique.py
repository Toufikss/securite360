"""
Page de politique de sécurité - Sécurité 360
Gestion de la politique de sécurité de l'information
"""

import streamlit as st
from utils.helpers import display_page_header, format_date
from utils.config import COLORS
from datetime import datetime

def show(auth, db):
    """Affiche la page de politique de sécurité"""
    
    # En-tête
    display_page_header(
        "Politique de sécurité",
        "Gestion de la politique de sécurité de l'information"
    )
    
    # Récupérer les documents de politique
    documents = db.get_documents_by_category('Politique')
    
    # Tabs pour organiser le contenu
    tab1, tab2, tab3 = st.tabs(["📄 Document actuel", "📚 Historique", "➕ Nouvelle version"])
    
    with tab1:
        if documents:
            doc_actuel = documents[0]  # Document le plus récent
            
            st.markdown(f"""
            <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                <h3 style="color: {COLORS['text']}; margin-top: 0;">{doc_actuel['titre']}</h3>
                <p style="color: {COLORS['text_secondary']}; margin: 0.5rem 0;">
                    <strong>Version:</strong> {doc_actuel['version']} |
                    <strong>Auteur:</strong> {doc_actuel['auteur']} |
                    <strong>Date:</strong> {format_date(doc_actuel['date_creation'])}
                </p>
            </div>
            """, unsafe_allow_html=True)
            
            # Contenu du document
            if doc_actuel.get('contenu'):
                st.markdown(f"""
                <div style="background-color: {COLORS['background']}; padding: 2rem; border-radius: 8px; border-left: 4px solid {COLORS['accent']};">
                    <div style="color: {COLORS['text']}; line-height: 1.8;">
                        {doc_actuel['contenu'].replace(chr(10), '<br>')}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            
            # Actions (si permissions)
            if auth.has_role("Admin"):
                st.markdown("<br>", unsafe_allow_html=True)
                col1, col2 = st.columns([1, 1])
                
                with col1:
                    if st.button("✏️ Modifier", use_container_width=True):
                        st.session_state['edit_politique'] = True
                        st.rerun()
                
                with col2:
                    # Bouton d'export PDF (placeholder)
                    st.download_button(
                        label="📥 Exporter en PDF",
                        data="Contenu PDF à implémenter",
                        file_name=f"politique_securite_v{doc_actuel['version']}.pdf",
                        mime="application/pdf",
                        use_container_width=True
                    )
        else:
            st.info("Aucune politique de sécurité n'a été créée. Utilisez l'onglet 'Nouvelle version' pour en créer une.")
    
    with tab2:
        st.markdown("### 📚 Historique des versions")
        
        if documents:
            for idx, doc in enumerate(documents):
                with st.expander(f"Version {doc['version']} - {format_date(doc['date_creation'])}"):
                    st.markdown(f"**Auteur:** {doc['auteur']}")
                    st.markdown(f"**Dernière modification:** {format_date(doc['derniere_modification'])}")
                    st.markdown("---")
                    st.markdown(doc.get('contenu', 'Aucun contenu'))
        else:
            st.info("Aucun historique disponible")
    
    with tab3:
        if auth.has_role("Admin"):
            st.markdown("### ➕ Créer une nouvelle version")
            
            user = auth.get_current_user()
            
            with st.form("nouvelle_politique"):
                titre = st.text_input(
                    "Titre du document",
                    value="Politique de sécurité de l'information"
                )
                
                version = st.text_input(
                    "Numéro de version",
                    value="1.0",
                    placeholder="Ex: 1.0, 2.0, 2.1..."
                )
                
                contenu = st.text_area(
                    "Contenu de la politique",
                    height=400,
                    value="""1. INTRODUCTION

La présente politique de sécurité de l'information définit les principes et les règles que [Nom de l'organisation] s'engage à respecter pour protéger ses informations et ses actifs informationnels.

2. OBJECTIFS

Les objectifs de cette politique sont de :
- Protéger la confidentialité, l'intégrité et la disponibilité des informations
- Établir un cadre de gestion de la sécurité de l'information
- Définir les responsabilités en matière de sécurité
- Assurer la conformité aux exigences légales et réglementaires

3. CHAMP D'APPLICATION

Cette politique s'applique à :
- Tous les employés, sous-traitants et partenaires
- Tous les systèmes d'information et actifs de l'organisation
- Toutes les informations, quel que soit leur support

4. PRINCIPES DIRECTEURS

4.1 Confidentialité
Les informations doivent être accessibles uniquement aux personnes autorisées.

4.2 Intégrité
Les informations doivent être exactes, complètes et protégées contre toute modification non autorisée.

4.3 Disponibilité
Les informations doivent être accessibles aux utilisateurs autorisés quand ils en ont besoin.

5. RESPONSABILITÉS

5.1 Direction
La direction est responsable de l'approbation et du soutien de cette politique.

5.2 Responsable de la sécurité de l'information (RSSI)
Le RSSI est responsable de la mise en œuvre et du suivi de cette politique.

5.3 Employés
Tous les employés sont responsables de respecter cette politique et les procédures associées.

6. GESTION DES RISQUES

L'organisation s'engage à :
- Identifier et évaluer régulièrement les risques de sécurité
- Mettre en place des mesures de traitement appropriées
- Surveiller et réviser les risques de manière continue

7. CONTRÔLE D'ACCÈS

- Les accès aux systèmes doivent être accordés selon le principe du moindre privilège
- Les mots de passe doivent respecter les exigences de complexité
- Les accès doivent être révoqués immédiatement en cas de départ

8. SÉCURITÉ PHYSIQUE

- Les locaux doivent être protégés contre les accès non autorisés
- Les équipements critiques doivent être sécurisés
- Une politique de bureau propre doit être appliquée

9. INCIDENTS DE SÉCURITÉ

- Tout incident de sécurité doit être signalé immédiatement
- Une procédure de gestion des incidents est en place
- Des analyses post-incident doivent être réalisées

10. CONTINUITÉ D'ACTIVITÉ

- Des plans de continuité et de reprise d'activité sont établis
- Des tests réguliers doivent être effectués
- Les sauvegardes doivent être réalisées conformément aux procédures

11. CONFORMITÉ

- Cette politique doit être respectée par tous
- Des audits réguliers seront réalisés
- Les violations peuvent entraîner des sanctions disciplinaires

12. RÉVISION

Cette politique sera révisée au minimum une fois par an ou en cas de changement significatif.

Approuvé par : [Direction]
Date : [Date d'approbation]"""
                )
                
                fichier_joint = st.file_uploader(
                    "Fichier joint (optionnel)",
                    type=['pdf', 'docx'],
                    help="Vous pouvez joindre une version PDF ou Word du document"
                )
                
                col1, col2 = st.columns(2)
                with col1:
                    submit = st.form_submit_button("💾 Enregistrer", use_container_width=True, type="primary")
                with col2:
                    cancel = st.form_submit_button("❌ Annuler", use_container_width=True)
                
                if submit:
                    if titre and version and contenu:
                        fichier_path = None
                        if fichier_joint:
                            fichier_path = f"documents/{fichier_joint.name}"
                        
                        db.add_document(
                            titre=titre,
                            categorie='Politique',
                            version=version,
                            contenu=contenu,
                            auteur=user['username'],
                            fichier_path=fichier_path
                        )
                        
                        st.success("✅ Politique enregistrée avec succès!")
                        st.rerun()
                    else:
                        st.error("Veuillez remplir tous les champs obligatoires")
        else:
            st.warning("🚫 Vous devez avoir les droits d'administrateur pour créer une nouvelle politique")
    
    # Section d'aide
    with st.expander("ℹ️ Aide et recommandations"):
        st.markdown(f"""
        <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 8px; color: {COLORS['text']};">
            <h4 style="color: {COLORS['accent']}; margin-top: 0;">Bonnes pratiques pour la politique de sécurité :</h4>
            <ul style="line-height: 1.8;">
                <li>La politique doit être claire, concise et compréhensible par tous</li>
                <li>Elle doit être approuvée par la direction générale</li>
                <li>Elle doit être communiquée à tout le personnel</li>
                <li>Elle doit être revue au moins une fois par an</li>
                <li>Elle doit être alignée avec les objectifs business</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)
                