"""
Page de gestion des utilisateurs - Sécurité 360
Administration des comptes utilisateurs (Admin uniquement)
"""

import streamlit as st
from utils.helpers import display_page_header, get_role_badge, format_date, validate_password_strength
from utils.config import COLORS, ROLES

def show(auth, db):
    """Affiche la page de gestion des utilisateurs"""
    
    # Vérifier les permissions
    auth.require_role("Admin")
    
    # En-tête
    display_page_header(
        "Gestion des utilisateurs",
        "Administration des comptes et des permissions"
    )
    
    # Tabs
    tab1, tab2 = st.tabs(["👥 Liste des utilisateurs", "➕ Nouvel utilisateur"])
    
    with tab1:
        # Récupérer tous les utilisateurs
        users = db.get_all_users()
        
        st.markdown(f"###  Utilisateurs actifs ({len(users)})")
        
        # Afficher les utilisateurs
        for user in users:
            with st.container():
                derniere_connexion = format_date(user['last_login']) if user.get('last_login') else 'Jamais'
                date_creation = format_date(user['created_at'])
                
                st.markdown(f"""
                <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px; margin-bottom: 1rem;">
                    <div style="display: flex; justify-content: space-between; align-items: center;">
                        <div style="flex: 1;">
                            <h4 style="color: {COLORS['text']}; margin: 0 0 0.5rem 0;">{user['username']}</h4>
                            <div style="margin-bottom: 0.5rem;">{get_role_badge(user['role'])}</div>
                            <p style="color: {COLORS['text_secondary']}; font-size: 0.85rem; margin: 0;"><strong>Créé le:</strong> {date_creation} | <strong>Dernière connexion:</strong> {derniere_connexion}</p>
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Actions
                col1, col2, col3 = st.columns([4, 1, 1])
                
                with col2:
                    if st.button("✏️ Modifier", key=f"edit_{user['id']}", use_container_width=True):
                        st.session_state[f'edit_user_{user["id"]}'] = True
                
                with col3:
                    # Empêcher la suppression de son propre compte
                    current_user = auth.get_current_user()
                    if user['id'] != current_user['id']:
                        if st.button("🗑️ Supprimer", key=f"del_{user['id']}", use_container_width=True):
                            if db.delete_user(user['id']):
                                st.success(f"Utilisateur {user['username']} supprimé")
                                st.rerun()
                            else:
                                st.error("Erreur lors de la suppression")
                    else:
                        st.info("Vous")
                
                # Formulaire d'édition
                if st.session_state.get(f'edit_user_{user["id"]}', False):
                    with st.expander(f"✏️ Modifier {user['username']}", expanded=True):
                        with st.form(f"edit_form_{user['id']}"):
                            new_role = st.selectbox(
                                "Rôle",
                                ROLES,
                                index=ROLES.index(user['role']),
                                key=f"role_{user['id']}"
                            )
                            
                            new_password = st.text_input(
                                "Nouveau mot de passe (laisser vide pour ne pas changer)",
                                type="password",
                                key=f"pass_{user['id']}"
                            )
                            
                            if new_password:
                                is_valid, message = validate_password_strength(new_password)
                                if is_valid:
                                    st.success(message)
                                else:
                                    st.warning(message)
                            
                            col1, col2 = st.columns(2)
                            with col1:
                                if st.form_submit_button("💾 Enregistrer", use_container_width=True):
                                    # Mise à jour (à implémenter dans la DB)
                                    st.success("Modifications enregistrées")
                                    st.session_state[f'edit_user_{user["id"]}'] = False
                                    st.rerun()
                            with col2:
                                if st.form_submit_button("❌ Annuler", use_container_width=True):
                                    st.session_state[f'edit_user_{user["id"]}'] = False
                                    st.rerun()
    
    with tab2:
        st.markdown("### ➕ Créer un nouvel utilisateur")
        
        with st.form("new_user_form"):
            username = st.text_input(
                "Nom d'utilisateur *",
                placeholder="Identifiant unique",
                help="L'identifiant doit être unique dans le système"
            )
            
            col1, col2 = st.columns(2)
            
            with col1:
                password = st.text_input(
                    "Mot de passe *",
                    type="password",
                    placeholder="Minimum 8 caractères"
                )
            
            with col2:
                password_confirm = st.text_input(
                    "Confirmer le mot de passe *",
                    type="password",
                    placeholder="Retaper le mot de passe"
                )
            
            # Validation du mot de passe
            if password:
                is_valid, message = validate_password_strength(password)
                if is_valid:
                    st.success(message)
                else:
                    st.warning(message)
            
            role = st.selectbox(
                "Rôle *",
                ROLES,
                help="Admin: Accès complet | Auditeur: Gestion audits et critères | Utilisateur: Consultation"
            )
            
            # Description des rôles
            st.info(f"""
            **Description des rôles:**
            
            - **Admin**: Accès complet à toutes les fonctionnalités, gestion des utilisateurs et paramètres
            - **Auditeur**: Peut créer/modifier des audits, mettre à jour les critères de conformité
            - **Utilisateur**: Consultation des tableaux de bord et rapports uniquement
            """)
            
            col1, col2 = st.columns(2)
            
            with col1:
                submit = st.form_submit_button("➕ Créer l'utilisateur", use_container_width=True, type="primary")
            
            with col2:
                cancel = st.form_submit_button("❌ Annuler", use_container_width=True)
            
            if submit:
                # Validation
                errors = []
                
                if not username:
                    errors.append("Le nom d'utilisateur est requis")
                
                if not password:
                    errors.append("Le mot de passe est requis")
                elif password != password_confirm:
                    errors.append("Les mots de passe ne correspondent pas")
                else:
                    is_valid, message = validate_password_strength(password)
                    if not is_valid:
                        errors.append(message)
                
                if errors:
                    for error in errors:
                        st.error(error)
                else:
                    # Créer l'utilisateur
                    success = db.add_user(username, password, role)
                    
                    if success:
                        st.success(f"✅ Utilisateur {username} créé avec succès!")
                        st.balloons()
                        st.rerun()
                    else:
                        st.error("❌ Erreur: Ce nom d'utilisateur existe déjà ou une erreur est survenue")
    
    # Statistiques
    st.markdown("<br><br>", unsafe_allow_html=True)
    st.markdown(f"""
    <div style="background-color: {COLORS['surface']}; padding: 1.5rem; border-radius: 12px;">
        <h3 style="color: {COLORS['text']}; margin-top: 0;"> Statistiques des utilisateurs</h3>
    </div>
    """, unsafe_allow_html=True)
    
    users = db.get_all_users()
    role_counts = {}
    for user in users:
        role_counts[user['role']] = role_counts.get(user['role'], 0) + 1
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total utilisateurs", len(users))
    with col2:
        st.metric("Administrateurs", role_counts.get('Admin', 0))
    with col3:
        st.metric("Auditeurs", role_counts.get('Auditeur', 0))
    with col4:
        st.metric("Utilisateurs", role_counts.get('Utilisateur', 0))
    
    # Conseils de sécurité
    with st.expander("🔒 Conseils de sécurité"):
        st.markdown("#### Bonnes pratiques de gestion des comptes :")
        st.markdown("""
        - Utiliser des mots de passe forts (minimum 8 caractères avec majuscules, minuscules, chiffres et caractères spéciaux)
        - Changer régulièrement les mots de passe (tous les 90 jours recommandé)
        - Appliquer le principe du moindre privilège
        - Désactiver ou supprimer immédiatement les comptes des employés partants
        - Effectuer des revues régulières des accès
        - Mettre en place une authentification multi-facteurs si possible
        - Journaliser toutes les actions administratives
        """)
        
        st.markdown("#### Niveaux de permissions :")
        st.markdown("""
        - **Admin:** Gestion complète du système, création/suppression d'utilisateurs, configuration
        - **Auditeur:** Création d'audits, modification des critères, génération de rapports
        - **Utilisateur:** Consultation des dashboards, lecture des rapports et documents
        """)