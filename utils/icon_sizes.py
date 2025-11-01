"""
Configuration des tailles d'icônes pour Sécurité 360
Fichier de configuration centralisé pour ajuster facilement les tailles
"""

# Tailles prédéfinies
ICON_SIZES = {
    "tiny": "16px",      # Très petite - listes, inline
    "small": "24px",     # Petite - boutons, menus  
    "medium": "32px",    # Moyenne - cartes secondaires
    "normal": "48px",    # Normale - usage standard
    "large": "64px",     # Grande - KPI principaux
    "xl": "80px",        # Très grande - éléments importants
    "xxl": "96px"        # Énorme - headers, logos
}

# Configuration spécifique par type d'icône
KPI_ICON_SIZES = {
    # Toutes les icônes KPI à 80px (taille xl)
    "score_global": "xl",           # 90px
    "audits": "xl",                 # 80px
    "criteres_evalues": "xl",       # 80px
    "criteres_risque": "90px",      # 90px
    "evolution_semestrielle": "xl", # 80px
    "delai_moyen": "xl",            # 80px
    "prochaine_echeance": "xl",     # 80px
    "maturite": "xl",               # 80px
    
    # Nouvelles icônes aussi à 80px
    "documents": "xl",              # 80px
    "formations": "xl",             # 80px
    "incidents": "xl",              # 80px
    "risques": "xl",                # 80px
    "actions_correctives": "xl",    # 80px
    "non_conformites": "xl"         # 80px
}

# Configuration pour les icônes système
SYSTEM_ICON_SIZES = {
    "success": "small",    # 24px
    "warning": "small",    # 24px
    "error": "small",      # 24px
    "info": "small"        # 24px
}

def get_icon_size(icon_key: str, icon_type: str = "kpi", custom_size: str = None) -> str:
    """
    Récupère la taille configurée pour une icône
    
    Args:
        icon_key: Clé de l'icône
        icon_type: Type d'icône (kpi, system)
        custom_size: Taille personnalisée qui override la config
        
    Returns:
        Taille en pixels (ex: "64px")
    """
    if custom_size:
        # Si une taille personnalisée est fournie
        if custom_size in ICON_SIZES:
            return ICON_SIZES[custom_size]  # Nom de taille
        else:
            return custom_size  # Taille directe (ex: "50px")
    
    # Utiliser la configuration par type
    if icon_type == "kpi":
        size_name = KPI_ICON_SIZES.get(icon_key, "large")  # Défaut: large
    elif icon_type == "system":
        size_name = SYSTEM_ICON_SIZES.get(icon_key, "small")  # Défaut: small
    else:
        size_name = "normal"  # Défaut général
    
    # Si size_name est déjà une taille en pixels (ex: "90px"), la retourner directement
    if size_name.endswith("px"):
        return size_name
    
    # Sinon, chercher dans le dictionnaire des tailles nommées
    return ICON_SIZES.get(size_name, "48px")

def list_available_sizes():
    """Retourne la liste des tailles disponibles"""
    return list(ICON_SIZES.keys())

def get_all_kpi_sizes():
    """Retourne un dictionnaire avec toutes les tailles KPI configurées"""
    return {
        icon_key: get_icon_size(icon_key, "kpi") 
        for icon_key in KPI_ICON_SIZES.keys()
    }

# Fonctions pour modifier dynamiquement les tailles
def update_kpi_size(icon_key: str, size: str):
    """Met à jour la taille d'une icône KPI"""
    if size in ICON_SIZES:
        KPI_ICON_SIZES[icon_key] = size
    else:
        # Créer une nouvelle taille personnalisée
        ICON_SIZES[f"custom_{icon_key}"] = size
        KPI_ICON_SIZES[icon_key] = f"custom_{icon_key}"

def reset_kpi_size(icon_key: str):
    """Remet la taille par défaut pour une icône KPI"""
    if icon_key in KPI_ICON_SIZES:
        KPI_ICON_SIZES[icon_key] = "large"  # Taille par défaut

# Configuration rapide pour tout changer d'un coup
def set_all_kpi_size(size: str):
    """Change la taille de toutes les icônes KPI"""
    for icon_key in KPI_ICON_SIZES.keys():
        KPI_ICON_SIZES[icon_key] = size

# Exemples d'utilisation :
# get_icon_size("score_global") → "80px"
# get_icon_size("documents", "kpi") → "32px" 
# get_icon_size("audits", "kpi", "xxl") → "96px"
# set_all_kpi_size("xl")  # Toutes les icônes en 80px