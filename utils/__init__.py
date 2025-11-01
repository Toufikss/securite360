"""
Package utils pour Sécurité 360
Contient les utilitaires et configurations de l'application
"""

# Import des modules principaux pour faciliter l'accès
from .config import APP_NAME, APP_VERSION, GLOBAL_CSS, COLORS
from .icons import get_sidebar_icon
from .logos import get_main_logo, get_sidebar_logo

__all__ = [
    'APP_NAME',
    'APP_VERSION', 
    'GLOBAL_CSS',
    'COLORS',
    'get_sidebar_icon',
    'get_main_logo',
    'get_sidebar_logo'
]