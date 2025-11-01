"""
Module d'authentification pour Sécurité 360
Gère la connexion, déconnexion et vérification des rôles
"""

import streamlit as st
from database import Database
from logo import logo_config
import hashlib
import time
import json
import os
from datetime import datetime, timedelta

class Auth:
    def __init__(self):
        """Initialise le système d'authentification"""
        self.db = Database()
        self.session_key = "securite360_session"
        self.session_duration = 24  # Durée de session en heures
        
        # Initialiser la session persistante
        self._init_persistent_session()
        
        # Initialiser les variables de session
        if 'authenticated' not in st.session_state:
            st.session_state.authenticated = False
        if 'user' not in st.session_state:
            st.session_state.user = None
    
    def _init_persistent_session(self):
        """Initialise la session persistante simple"""
        # Utiliser un fichier de session global pour cette application
        self.session_file = os.path.join(os.path.dirname(__file__), '.session_data.json')
        
        # Vérifier et restaurer une session existante
        if 'session_initialized' not in st.session_state:
            st.session_state.session_initialized = True
            self._restore_session()
    
    def _restore_session(self):
        """Restaure une session sauvegardée si elle existe et est valide"""
        try:
            if os.path.exists(self.session_file):
                with open(self.session_file, 'r', encoding='utf-8') as f:
                    session_data = json.load(f)
                
                # Vérifier si la session n'a pas expiré
                created_time = datetime.fromisoformat(session_data.get('created_at', ''))
                if datetime.now() - created_time < timedelta(hours=self.session_duration):
                    # Vérifier que l'utilisateur existe toujours en base
                    user_id = session_data.get('user_id')
                    if user_id:
                        db_user = self.db.get_user_by_id(user_id)
                        if db_user:
                            st.session_state.authenticated = True
                            st.session_state.user = db_user
                            return True
                
                # Session expirée ou utilisateur inexistant, supprimer le fichier
                os.remove(self.session_file)
        except Exception as e:
            # En cas d'erreur, supprimer le fichier de session corrompu
            if os.path.exists(self.session_file):
                try:
                    os.remove(self.session_file)
                except:
                    pass
        
        return False
    
    def _save_session(self, user_data):
        """Sauvegarde la session utilisateur dans un fichier"""
        session_data = {
            'user_id': user_data.get('id'),
            'created_at': datetime.now().isoformat(),
            'expires_at': (datetime.now() + timedelta(hours=self.session_duration)).isoformat()
        }
        
        try:
            with open(self.session_file, 'w', encoding='utf-8') as f:
                json.dump(session_data, f, ensure_ascii=False, indent=2)
        except Exception as e:
            # Silencieusement ignorer les erreurs de sauvegarde
            pass
    
    def _clear_session(self):
        """Efface la session persistante"""
        try:
            if os.path.exists(self.session_file):
                os.remove(self.session_file)
        except Exception as e:
            # Silencieusement ignorer les erreurs
            pass
    
    def login_page(self):
        """Affiche la page de connexion en plein écran"""
        st.markdown("""
            <style>
            /* Container de connexion centré avec effet plein écran */
            .login-container {
                max-width: 500px;
                margin: 0 auto;
                padding: 3rem;
                background: linear-gradient(135deg, #1e3a8a 0%, #1e40af 100%);
                border-radius: 20px;
                box-shadow: 0 20px 60px rgba(0, 0, 0, 0.4);
                margin-top: 8vh;
                margin-bottom: 2rem;
            }
            

            
            /* Champs de saisie stylisés */
            .stTextInput > div > div > input {
                background-color: rgba(255, 255, 255, 0.1);
                color: white;
                border: 1px solid rgba(255, 255, 255, 0.2);
                border-radius: 10px;
                padding: 0.8rem;
                font-size: 1rem;
                backdrop-filter: blur(5px);
            }
            
            .stTextInput > div > div > input:focus {
                border: 2px solid #60a5fa;
                box-shadow: 0 0 20px rgba(96, 165, 250, 0.3);
            }
            
            .stTextInput > label {
                color: white !important;
                font-weight: 600;
                font-size: 1.1rem;
            }
            
            /* Bouton de connexion stylisé */
            .stButton > button {
                background: linear-gradient(135deg, #059669 0%, #10b981 100%);
                color: white;
                border: none;
                border-radius: 10px;
                padding: 0.8rem 2rem;
                font-size: 1.1rem;
                font-weight: 600;
                box-shadow: 0 4px 15px rgba(5, 150, 105, 0.3);
                transition: all 0.3s ease;
            }
            
            .stButton > button:hover {
                transform: translateY(-2px);
                box-shadow: 0 6px 20px rgba(5, 150, 105, 0.4);
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown('<div class="login-container">', unsafe_allow_html=True)
        
        # Affichage du logo PNG
        logo_config.display_logo()
        
        # Texte descriptif sous le logo
        st.markdown("""
        <div style="text-align: center; margin: 0.2rem 0 0.5rem 0;">
            <p style="
                color: #E5E7EB; 
                font-size: 1.2rem; 
                font-weight: 100; 
                margin: 0;
                text-shadow: 0 1px 2px rgba(0,0,0,0.1);
                letter-spacing: 0.5px;
            ">Système de gestion ISO 27001</p>
        </div>
        """, unsafe_allow_html=True)
        
        with st.form("login_form"):
            username = st.text_input("Identifiant", placeholder="Entrez votre identifiant")
            password = st.text_input("Mot de passe", type="password", placeholder="Entrez votre mot de passe")
            
            col1, col2, col3 = st.columns([1, 2, 1])
            with col2:
                submit = st.form_submit_button("Se connecter", use_container_width=True)
            
            if submit:
                if username and password:
                    user = self.db.verify_user(username, password)
                    if user:
                        st.session_state.authenticated = True
                        st.session_state.user = user
                        
                        # Sauvegarder la session de façon persistante
                        self._save_session(user)
                        
                        st.success("Connexion réussie!")
                        st.rerun()
                    else:
                        st.error("Identifiant ou mot de passe incorrect")
                else:
                    st.warning("Veuillez remplir tous les champs")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Informations de test
        with st.expander("ℹ️ Identifiants de test"):
            st.markdown("""
            **Administrateur:**
            - Identifiant: `toufiksalah`
            - Mot de passe: `Admin@2025`
            
            **Auditeur:**
            - Identifiant: `audit01`
            - Mot de passe: `Audit@2025`
            
            **Utilisateur:**
            - Identifiant: `user01`
            - Mot de passe: `User@2025`
            """)
    
    def logout(self):
        """Déconnecte l'utilisateur"""
        # Effacer la session persistante
        self._clear_session()
        
        # Effacer la session Streamlit
        st.session_state.authenticated = False
        st.session_state.user = None
        st.session_state.session_checked = False
        
        st.success("Déconnexion réussie!")
        st.rerun()
    
    def is_authenticated(self) -> bool:
        """Vérifie si l'utilisateur est authentifié"""
        return st.session_state.get('authenticated', False)
    
    def get_current_user(self):
        """Récupère l'utilisateur actuel"""
        return st.session_state.get('user', None)
    
    def has_role(self, required_role: str) -> bool:
        """Vérifie si l'utilisateur a le rôle requis"""
        user = self.get_current_user()
        if not user:
            return False
        
        role_hierarchy = {
            'Admin': 3,
            'Auditeur': 2,
            'Utilisateur': 1
        }
        
        user_level = role_hierarchy.get(user['role'], 0)
        required_level = role_hierarchy.get(required_role, 0)
        
        return user_level >= required_level
    
    def require_auth(self):
        """Décorateur pour exiger l'authentification"""
        if not self.is_authenticated():
            st.warning("Vous devez être connecté pour accéder à cette page")
            st.stop()
    
    def require_role(self, role: str):
        """Décorateur pour exiger un rôle spécifique"""
        self.require_auth()
        if not self.has_role(role):
            st.error(f"Vous n'avez pas les permissions nécessaires (rôle {role} requis)")
            st.stop()