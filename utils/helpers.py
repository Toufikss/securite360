"""
Fonctions utilitaires pour Sécurité 360
Fournit des fonctions helper pour diverses opérations
"""

import streamlit as st
from datetime import datetime
from utils.config import COLORS, STATUTS_CONFORMITE
from typing import Dict, List, Optional

def format_date(date_str: str, format_type: str = 'short') -> str:
    """
    Formate une date selon le type spécifié
    
    Args:
        date_str: Date au format 'YYYY-MM-DD HH:MM:SS' ou 'YYYY-MM-DD'
        format_type: 'short' pour DD/MM/YYYY ou 'long' pour format complet
    
    Returns:
        Date formatée en français
    """
    if not date_str:
        return "N/A"
    
    try:
        if len(date_str) > 10:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        else:
            date_obj = datetime.strptime(date_str, '%Y-%m-%d')
        
        if format_type == 'short':
            return date_obj.strftime('%d/%m/%Y')
        else:
            mois_fr = ['janvier', 'février', 'mars', 'avril', 'mai', 'juin',
                      'juillet', 'août', 'septembre', 'octobre', 'novembre', 'décembre']
            return f"{date_obj.day} {mois_fr[date_obj.month-1]} {date_obj.year}"
    except:
        return date_str

def get_statut_badge(statut: str) -> str:
    """
    Génère un badge HTML pour un statut de conformité
    
    Args:
        statut: Statut de conformité
    
    Returns:
        Code HTML du badge
    """
    badge_colors = {
        'Conforme': COLORS['success'],
        'Largement conforme': '#16a34a',  # Vert foncé
        'Partiellement conforme': COLORS['warning'],
        'Faiblement conforme': '#dc2626',  # Rouge-orange
        'Non conforme': COLORS['danger']
    }
    
    color = badge_colors.get(statut, COLORS['info'])
    
    return f'<span style="background-color: {color}; color: white; padding: 0.3rem 0.8rem; border-radius: 20px; font-size: 0.85rem; font-weight: 600; display: inline-block;">{statut}</span>'

def get_role_badge(role: str) -> str:
    """
    Génère un badge HTML pour un rôle utilisateur
    
    Args:
        role: Rôle de l'utilisateur
    
    Returns:
        Code HTML du badge
    """
    role_colors = {
        'Admin': COLORS['danger'],
        'Auditeur': COLORS['info'],
        'Utilisateur': COLORS['success']
    }
    
    color = role_colors.get(role, COLORS['text_secondary'])
    
    return f'<span style="background-color: {color}; color: white; padding: 0.25rem 0.6rem; border-radius: 15px; font-size: 0.8rem; font-weight: 600;">{role}</span>'

def display_stat_card(title: str, value: str, icon: str = "📊", color: str = None):
    """
    Affiche une carte de statistique
    
    Args:
        title: Titre de la statistique
        value: Valeur à afficher
        icon: Icône à afficher
        color: Couleur personnalisée (optionnel)
    """
    accent_color = color if color else COLORS['accent']
    
    st.markdown(f"""
    <div class="stat-card" style="border-left-color: {accent_color};">
        <div style="display: flex; align-items: center; justify-content: space-between;">
            <div>
                <p class="stat-label">{title}</p>
                <p class="stat-value" style="color: {accent_color};">{value}</p>
            </div>
            <div style="font-size: 3rem; opacity: 0.5;">{icon}</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

def display_page_header(title: str, subtitle: str = ""):
    """
    Affiche un en-tête de page stylisé
    
    Args:
        title: Titre de la page
        subtitle: Sous-titre optionnel
    """
    subtitle_html = f'<p class="page-subtitle">{subtitle}</p>' if subtitle else ''
    
    st.markdown(f"""
    <div class="page-header fade-in">
        <h1 class="page-title">{title}</h1>
        {subtitle_html}
    </div>
    """, unsafe_allow_html=True)

def display_alert(message: str, alert_type: str = "info"):
    """
    Affiche une alerte personnalisée
    
    Args:
        message: Message à afficher
        alert_type: Type d'alerte (success, warning, danger, info)
    """
    alert_icons = {
        'success': '✅',
        'warning': '⚠️',
        'danger': '❌',
        'info': 'ℹ️'
    }
    
    icon = alert_icons.get(alert_type, 'ℹ️')
    
    st.markdown(f"""
    <div class="custom-alert alert-{alert_type}">
        <strong>{icon} {message}</strong>
    </div>
    """, unsafe_allow_html=True)

def calculate_conformity_percentage(stats: Dict) -> float:
    """
    Calcule le pourcentage de conformité
    
    Args:
        stats: Dictionnaire contenant les statistiques de conformité
    
    Returns:
        Pourcentage de conformité
    """
    total = stats.get('total', 0)
    if total == 0:
        return 0.0
    
    conforme = stats.get('conforme', 0)
    return round((conforme / total) * 100, 2)

def get_conformity_color(percentage: float) -> str:
    """
    Retourne une couleur selon le pourcentage de conformité
    
    Args:
        percentage: Pourcentage de conformité
    
    Returns:
        Code couleur hexadécimal
    """
    if percentage >= 80:
        return COLORS['success']
    elif percentage >= 50:
        return COLORS['warning']
    else:
        return COLORS['danger']

def format_file_size(size_bytes: int) -> str:
    """
    Formate une taille de fichier en unités lisibles
    
    Args:
        size_bytes: Taille en bytes
    
    Returns:
        Taille formatée (ex: "1.5 MB")
    """
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.1f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.1f} TB"

def filter_criteres(criteres: List[Dict], filters: Dict) -> List[Dict]:
    """
    Filtre une liste de critères selon des critères donnés
    
    Args:
        criteres: Liste des critères à filtrer
        filters: Dictionnaire de filtres (categorie, statut, recherche)
    
    Returns:
        Liste filtrée des critères
    """
    filtered = criteres.copy()
    
    # Filtre par catégorie
    if filters.get('categorie') and filters['categorie'] != 'Toutes':
        filtered = [c for c in filtered if c['categorie'] == filters['categorie']]
    
    # Filtre par statut
    if filters.get('statut') and filters['statut'] != 'Tous':
        filtered = [c for c in filtered if c['statut'] == filters['statut']]
    
    # Filtre par recherche textuelle
    if filters.get('recherche'):
        search_term = filters['recherche'].lower()
        filtered = [c for c in filtered if 
                   search_term in c['code'].lower() or 
                   search_term in c['titre'].lower() or 
                   search_term in c['description'].lower()]
    
    return filtered

def export_to_csv(data: List[Dict], filename: str) -> bytes:
    """
    Exporte des données en format CSV
    
    Args:
        data: Liste de dictionnaires à exporter
        filename: Nom du fichier
    
    Returns:
        Données CSV en bytes
    """
    import pandas as pd
    import io
    
    df = pd.DataFrame(data)
    csv_buffer = io.StringIO()
    df.to_csv(csv_buffer, index=False, encoding='utf-8-sig')
    return csv_buffer.getvalue().encode('utf-8-sig')

def validate_password_strength(password: str) -> tuple:
    """
    Valide la force d'un mot de passe
    
    Args:
        password: Mot de passe à valider
    
    Returns:
        Tuple (is_valid: bool, message: str)
    """
    if len(password) < 8:
        return False, "Le mot de passe doit contenir au moins 8 caractères"
    
    if not any(c.isupper() for c in password):
        return False, "Le mot de passe doit contenir au moins une majuscule"
    
    if not any(c.islower() for c in password):
        return False, "Le mot de passe doit contenir au moins une minuscule"
    
    if not any(c.isdigit() for c in password):
        return False, "Le mot de passe doit contenir au moins un chiffre"
    
    if not any(c in '!@#$%^&*()_+-=[]{}|;:,.<>?' for c in password):
        return False, "Le mot de passe doit contenir au moins un caractère spécial"
    
    return True, "Mot de passe valide"

def display_separator():
    """Affiche un séparateur stylisé"""
    st.markdown('<div class="separator"></div>', unsafe_allow_html=True)

def create_download_button(data: bytes, filename: str, label: str, mime_type: str = "application/octet-stream"):
    """
    Crée un bouton de téléchargement stylisé
    
    Args:
        data: Données à télécharger
        filename: Nom du fichier
        label: Libellé du bouton
        mime_type: Type MIME du fichier
    """
    st.download_button(
        label=label,
        data=data,
        file_name=filename,
        mime=mime_type,
        use_container_width=True
    )

def get_categorie_icon(categorie: str) -> str:
    """
    Retourne une icône pour une catégorie de critère
    
    Args:
        categorie: Catégorie du critère
    
    Returns:
        Icône emoji
    """
    icons = {
        'Organisationnelle': '🏢',
        'Personnel': '👥',
        'Physique': '🔒',
        'Technologique': '💻'
    }
    return icons.get(categorie, '📋')