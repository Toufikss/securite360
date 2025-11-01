"""
Configuration globale pour Sécurité 360
Définit les constantes, couleurs et styles de l'application
"""

# Informations de l'application
APP_NAME = "Sécurité 360"
APP_VERSION = "1.0.0"
APP_DESCRIPTION = "Système de gestion de la conformité ISO 27001"

# Couleurs du thème (thème sombre professionnel)
COLORS = {
    'primary': '#1e3a8a',       # Bleu foncé
    'secondary': '#1e40af',     # Bleu intermédiaire
    'accent': '#10b981',        # Vert sécurité
    'background': '#0f172a',    # Fond très sombre
    'surface': '#1e293b',       # Surface légèrement plus claire
    'text': '#f8fafc',          # Texte blanc cassé
    'text_secondary': '#94a3b8', # Texte secondaire gris
    'success': '#10b981',       # Vert succès
    'warning': '#f59e0b',       # Orange alerte
    'danger': '#ef4444',        # Rouge danger
    'info': '#3b82f6',          # Bleu information
}

# Statuts de conformité
STATUTS_CONFORMITE = [
    'Conforme',
    'Largement conforme',
    'Partiellement conforme',
    'Faiblement conforme',
    'Non conforme'
]

# Catégories de critères ISO 27001
CATEGORIES_ISO = [
    'Organisationnelle',
    'Personnel',
    'Physique',
    'Technologique'
]

# Rôles utilisateur
ROLES = ['Admin', 'Auditeur', 'Utilisateur']

# Types de directives
TYPES_DIRECTIVES = [
    'Technique',
    'Organisationnelle',
    'Procédurale',
    'Politique'
]

# Niveaux d'efficacité
NIVEAUX_EFFICACITE = [
    'Élevée',
    'Moyenne',
    'Faible',
    'À améliorer'
]

# Style CSS global
GLOBAL_CSS = f"""
<style>
    /* Configuration générale */
    .main {{
        background-color: {COLORS['background']};
        color: {COLORS['text']};
    }}
    
    /* En-têtes */
    h1, h2, h3 {{
        color: {COLORS['text']} !important;
        font-weight: 700;
    }}
    
    /* Cartes de statistiques */
    .stat-card {{
        background: linear-gradient(135deg, {COLORS['surface']} 0%, {COLORS['primary']} 100%);
        padding: 1.5rem;
        border-radius: 12px;
        box-shadow: 0 4px 16px rgba(0, 0, 0, 0.3);
        border-left: 4px solid {COLORS['accent']};
        margin-bottom: 1rem;
        transition: transform 0.2s ease;
    }}
    
    .stat-card:hover {{
        transform: translateY(-2px);
    }}
    
    .stat-value {{
        font-size: 2.5rem;
        font-weight: bold;
        color: {COLORS['accent']};
        margin: 0;
    }}
    
    .stat-label {{
        font-size: 0.9rem;
        color: {COLORS['text_secondary']};
        text-transform: uppercase;
        letter-spacing: 1px;
    }}
    
    /* Badges de statut */
    .badge {{
        padding: 0.3rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        font-weight: 600;
        display: inline-block;
    }}
    
    .badge-success {{
        background-color: {COLORS['success']};
        color: white;
    }}
    
    .badge-warning {{
        background-color: {COLORS['warning']};
        color: white;
    }}
    
    .badge-danger {{
        background-color: {COLORS['danger']};
        color: white;
    }}
    
    .badge-info {{
        background-color: {COLORS['info']};
        color: white;
    }}
    
    /* Tableaux */
    .dataframe {{
        background-color: {COLORS['surface']} !important;
        color: {COLORS['text']} !important;
        border-radius: 8px;
        overflow: hidden;
    }}
    
    /* Boutons */
    .stButton > button {{
        background: linear-gradient(135deg, {COLORS['primary']} 0%, {COLORS['secondary']} 100%);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-weight: 600;
        transition: all 0.3s ease;
    }}
    
    .stButton > button:hover {{
        box-shadow: 0 4px 12px rgba(30, 58, 138, 0.4);
        transform: translateY(-1px);
    }}
    
    /* Barre latérale */
    .css-1d391kg {{
        background-color: {COLORS['surface']};
    }}
    
    /* Expander */
    .streamlit-expanderHeader {{
        background-color: {COLORS['surface']};
        color: {COLORS['text']};
        border-radius: 8px;
    }}
    
    /* Séparateur */
    .separator {{
        height: 2px;
        background: linear-gradient(90deg, {COLORS['primary']} 0%, {COLORS['accent']} 100%);
        margin: 2rem 0;
        border-radius: 2px;
    }}
    
    /* En-tête de page */
    .page-header {{
        padding: 2rem;
        margin-bottom: 2rem;
    }}
    
    .page-title {{
        color: {COLORS['text']};
        font-size: 2rem;
        font-weight: bold;
        margin: 0;
    }}
    
    .page-subtitle {{
        color: {COLORS['text_secondary']};
        font-size: 1rem;
        margin-top: 0.5rem;
    }}
    
    /* Cartes de critères */
    .critere-card {{
        background-color: {COLORS['surface']};
        padding: 1.5rem;
        border-radius: 12px;
        margin-bottom: 1rem;
        border-left: 4px solid {COLORS['info']};
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.2);
    }}
    
    .critere-code {{
        color: {COLORS['accent']};
        font-weight: bold;
        font-size: 1.1rem;
    }}
    
    .critere-titre {{
        color: {COLORS['text']};
        font-size: 1rem;
        font-weight: 600;
        margin-top: 0.5rem;
    }}
    
    .critere-description {{
        color: {COLORS['text_secondary']};
        font-size: 0.9rem;
        margin-top: 0.5rem;
    }}
    
    /* Alertes personnalisées */
    .custom-alert {{
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
    }}
    
    .alert-success {{
        background-color: rgba(16, 185, 129, 0.1);
        border-left: 4px solid {COLORS['success']};
        color: {COLORS['success']};
    }}
    
    .alert-warning {{
        background-color: rgba(245, 158, 11, 0.1);
        border-left: 4px solid {COLORS['warning']};
        color: {COLORS['warning']};
    }}
    
    .alert-danger {{
        background-color: rgba(239, 68, 68, 0.1);
        border-left: 4px solid {COLORS['danger']};
        color: {COLORS['danger']};
    }}
    
    /* Animations */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    .fade-in {{
        animation: fadeIn 0.5s ease-out;
    }}
    
    /* Masquer les éléments Streamlit par défaut */
    #MainMenu {{visibility: hidden;}}
    footer {{visibility: hidden;}}
    
    /* Responsive */
    @media (max-width: 768px) {{
        .stat-card {{
            margin-bottom: 1rem;
        }}
        .page-header {{
            padding: 1rem;
        }}
        .page-title {{
            font-size: 1.5rem;
        }}
    }}
</style>
"""

# Configuration des graphiques Plotly
PLOTLY_CONFIG = {
    'displayModeBar': False,
    'staticPlot': False,
    'responsive': True
}

PLOTLY_LAYOUT = {
    'paper_bgcolor': COLORS['surface'],
    'plot_bgcolor': COLORS['surface'],
    'font': {
        'color': COLORS['text'],
        'family': 'Arial, sans-serif'
    },
    'margin': {'l': 40, 'r': 40, 't': 40, 'b': 40},
    'xaxis': {
        'gridcolor': 'rgba(148, 163, 184, 0.1)',
        'zerolinecolor': 'rgba(148, 163, 184, 0.1)'
    },
    'yaxis': {
        'gridcolor': 'rgba(148, 163, 184, 0.1)',
        'zerolinecolor': 'rgba(148, 163, 184, 0.1)'
    }
}

# Messages système
MESSAGES = {
    'success_save': '✅ Enregistrement réussi',
    'success_update': '✅ Mise à jour effectuée',
    'success_delete': '✅ Suppression effectuée',
    'error_generic': '❌ Une erreur est survenue',
    'error_permission': '🚫 Vous n\'avez pas les permissions nécessaires',
    'warning_empty': '⚠️ Aucune donnée disponible',
    'info_loading': '⏳ Chargement en cours...'
}

# Format de date
DATE_FORMAT = '%Y-%m-%d'
DATETIME_FORMAT = '%Y-%m-%d %H:%M:%S'