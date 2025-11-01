"""
Module de gestion des icônes - Sécurité 360
Centralise la gestion et l'affichage des icônes pour l'application
"""

import base64
import os
import streamlit as st
from typing import Optional, Dict, List
try:
    from .icon_sizes import get_icon_size
except ImportError:
    # Fallback si le fichier de config n'existe pas
    def get_icon_size(icon_key: str, icon_type: str = "kpi", custom_size: str = None) -> str:
        return custom_size or "64px"

# Configuration des icônes - Mise à jour avec toutes les icônes disponibles
ICONS_CONFIG = {
    # Indicateurs clés de performance (KPI) - Correspondance exacte avec le dossier
    "kpi": {
        "score_global": {
            "file": "score global.png",
            "alt": "Score Global ISO 27001",
            "description": "Indicateur principal de conformité ISO 27001",
            "fallback": "🎯",
            "category": "performance"
        },
        "criteres_evalues": {
            "file": "critères évalués.png", 
            "alt": "Critères Évalués",
            "description": "Nombre total de critères évalués sur le total",
            "fallback": "📋",
            "category": "evaluation"
        },
        "criteres_risque": {
            "file": "critères a risque.png",
            "alt": "Critères à Risque",
            "description": "Critères nécessitant une attention particulière",
            "fallback": "⚠️",
            "category": "risk"
        },
        "audits": {
            "file": "audits.png",
            "alt": "Audits",
            "description": "Nombre d'audits réalisés sur la période",
            "fallback": "🧮",
            "category": "audit"
        },
        "evolution_semestrielle": {
            "file": "évolution semestrielle.png",
            "alt": "Évolution Semestrielle", 
            "description": "Progression du score sur 6 mois",
            "fallback": "📈",
            "category": "trend"
        },
        "delai_moyen": {
            "file": "délai moyen.png",
            "alt": "Délai Moyen de Résolution",
            "description": "Temps moyen pour résoudre les non-conformités",
            "fallback": "⏱️",
            "category": "time"
        },
        "prochaine_echeance": {
            "file": "prochaine échéance.png",
            "alt": "Prochaine Échéance",
            "description": "Date du prochain audit ou contrôle prévu",
            "fallback": "📅",
            "category": "planning"
        },
        "maturite": {
            "file": "etoile.png",
            "alt": "Niveau de Maturité Sécurité",
            "description": "Évaluation globale de la maturité sécurité (1-5)",
            "fallback": "⭐",
            "category": "maturity"
        }
    },
    
    # Icônes système (si besoin)
    "system": {
        "success": {
            "file": "success.png",
            "alt": "Succès",
            "fallback": "✅"
        },
        "warning": {
            "file": "warning.png",
            "alt": "Attention",
            "fallback": "⚠️"
        },
        "error": {
            "file": "error.png",
            "alt": "Erreur",
            "fallback": "❌"
        },
        "info": {
            "file": "info.png",
            "alt": "Information",
            "fallback": "ℹ️"
        }
    },
    
    # Icônes de navigation (sidebar)
    "sidebar": {
        "dashboard": {
            "file": "tableau de bord.png",
            "alt": "Tableau de bord",
            "description": "Vue d'ensemble des indicateurs de sécurité",
            "fallback": "🏠",
            "category": "navigation"
        },
        "politique": {
            "file": "politique de sécurité.png", 
            "alt": "Politique de sécurité",
            "description": "Politiques et procédures de sécurité",
            "fallback": "📘",
            "category": "navigation"
        },
        "declaration": {
            "file": "declaration d'applicapilité.png",
            "alt": "Déclaration d'applicabilité", 
            "description": "Applicabilité des contrôles ISO 27001",
            "fallback": "🧾",
            "category": "navigation"
        },
        "directive": {
            "file": "directives et mesures.png",
            "alt": "Directives et mesures",
            "description": "Directives et mesures de sécurité",
            "fallback": "⚙️",
            "category": "navigation"
        },
        "audits": {
            "file": "audites interne.png",
            "alt": "Audits internes",
            "description": "Gestion des audits internes",
            "fallback": "🧮",
            "category": "navigation"
        },
        "rapports": {
            "file": "rapport.png",
            "alt": "Rapports",
            "description": "Génération et consultation des rapports",
            "fallback": "📊",
            "category": "navigation"
        },
        "users": {
            "file": "gestion utilisateurs.png",
            "alt": "Gestion utilisateurs",
            "description": "Administration des utilisateurs",
            "fallback": "👥",
            "category": "navigation"
        },
        "data_automation": {
            "file": "automatisation.png", 
            "alt": "Automatisation",
            "description": "Automatisation des processus",
            "fallback": "🤖",
            "category": "navigation"
        },
        "settings": {
            "file": "parametres.png",
            "alt": "Paramètres",
            "description": "Configuration du système",
            "fallback": "🔧",
            "category": "navigation"
        },
        "navigation": {
            "file": "navigation.png",
            "alt": "Navigation",
            "description": "Menu de navigation principal",
            "fallback": "📋",
            "category": "navigation"
        }
    }
}

# Chemins des dossiers d'icônes
ICONS_PATHS = {
    "kpi": "icone Indicateurs clés de performance",
    "system": "assets/icons/system",
    "custom": "assets/icons/custom",
    "sidebar": "icone sidebar"
}

class IconManager:
    """Gestionnaire des icônes pour l'application"""
    
    def __init__(self):
        self._icon_cache: Dict[str, str] = {}
    
    def _get_icon_path(self, category: str, filename: str) -> str:
        """Construit le chemin complet vers un fichier icône"""
        base_path = ICONS_PATHS.get(category, "assets/icons")
        return os.path.join(base_path, filename)
    
    def _load_icon_as_base64(self, icon_path: str) -> Optional[str]:
        """
        Charge une icône et la convertit en base64
        
        Args:
            icon_path: Chemin vers le fichier icône
            
        Returns:
            String base64 de l'icône ou None si erreur
        """
        cache_key = f"icon_{icon_path}"
        
        # Vérifier le cache
        if cache_key in self._icon_cache:
            return self._icon_cache[cache_key]
        
        try:
            if os.path.exists(icon_path):
                with open(icon_path, "rb") as f:
                    icon_data = base64.b64encode(f.read()).decode()
                    self._icon_cache[cache_key] = icon_data
                    return icon_data
        except Exception as e:
            st.error(f"Erreur lors du chargement de l'icône {icon_path}: {str(e)}")
        
        return None
    
    def get_icon_html(self, 
                      category: str, 
                      icon_key: str, 
                      size: str = "48px", 
                      css_class: str = "") -> str:
        """
        Génère le HTML pour afficher une icône
        
        Args:
            category: Catégorie de l'icône (kpi, system, etc.)
            icon_key: Clé de l'icône dans la configuration
            size: Taille de l'icône (ex: "48px", "2rem")
            css_class: Classes CSS additionnelles
            
        Returns:
            HTML de l'icône ou fallback emoji
        """
        try:
            # Récupérer la configuration de l'icône
            icon_config = ICONS_CONFIG.get(category, {}).get(icon_key)
            if not icon_config:
                return "📊"  # Icône par défaut
            
            # Construire le chemin du fichier
            icon_path = self._get_icon_path(category, icon_config["file"])
            
            # Charger l'icône
            icon_b64 = self._load_icon_as_base64(icon_path)
            
            if icon_b64:
                css_classes = f"icon {css_class}".strip()
                return f'''<img src="data:image/png;base64,{icon_b64}" 
                              alt="{icon_config['alt']}" 
                              class="{css_classes}"
                              style="width: {size}; height: {size}; object-fit: contain;">'''
            else:
                # Fallback vers l'emoji
                return icon_config["fallback"]
                
        except Exception as e:
            st.error(f"Erreur lors de la génération de l'icône {category}.{icon_key}: {str(e)}")
            return "📊"
    
    def get_kpi_icon(self, icon_key: str, size: str = None) -> str:
        """
        Raccourci pour obtenir une icône KPI
        
        Args:
            icon_key: Clé de l'icône KPI
            size: Taille de l'icône (si None, utilise la config)
            
        Returns:
            HTML de l'icône KPI
        """
        # Utiliser la taille configurée ou celle fournie
        final_size = get_icon_size(icon_key, "kpi", size)
        return self.get_icon_html("kpi", icon_key, final_size, "kpi-icon")
    
    def get_system_icon(self, icon_key: str, size: str = "24px") -> str:
        """
        Raccourci pour obtenir une icône système
        
        Args:
            icon_key: Clé de l'icône système
            size: Taille de l'icône
            
        Returns:
            HTML de l'icône système
        """
        return self.get_icon_html("system", icon_key, size, "system-icon")
    
    def get_sidebar_icon(self, icon_key: str, size: str = "20px") -> str:
        """
        Raccourci pour obtenir une icône de sidebar
        
        Args:
            icon_key: Clé de l'icône sidebar
            size: Taille de l'icône
            
        Returns:
            HTML de l'icône sidebar
        """
        return self.get_icon_html("sidebar", icon_key, size, "sidebar-icon")
    
    def list_available_icons(self, category: str = None) -> Dict:
        """
        Liste les icônes disponibles
        
        Args:
            category: Catégorie spécifique ou None pour toutes
            
        Returns:
            Dictionnaire des icônes disponibles
        """
        if category:
            return ICONS_CONFIG.get(category, {})
        return ICONS_CONFIG
    
    def add_custom_icon(self, 
                       category: str, 
                       icon_key: str, 
                       filename: str, 
                       alt_text: str, 
                       fallback: str = "📊"):
        """
        Ajoute une icône personnalisée à la configuration
        
        Args:
            category: Catégorie de l'icône
            icon_key: Clé unique pour l'icône
            filename: Nom du fichier icône
            alt_text: Texte alternatif
            fallback: Emoji de fallback
        """
        if category not in ICONS_CONFIG:
            ICONS_CONFIG[category] = {}
        
        ICONS_CONFIG[category][icon_key] = {
            "file": filename,
            "alt": alt_text,
            "fallback": fallback
        }
    
    def clear_cache(self):
        """Vide le cache des icônes"""
        self._icon_cache.clear()
    
    def preload_icons(self, category: str = None):
        """
        Précharge les icônes en mémoire
        
        Args:
            category: Catégorie à précharger ou None pour toutes
        """
        categories_to_load = [category] if category else ICONS_CONFIG.keys()
        
        for cat in categories_to_load:
            if cat in ICONS_CONFIG:
                for icon_key, config in ICONS_CONFIG[cat].items():
                    icon_path = self._get_icon_path(cat, config["file"])
                    self._load_icon_as_base64(icon_path)
    
    def check_icons_availability(self, category: str = None) -> Dict[str, Dict]:
        """
        Vérifie la disponibilité de toutes les icônes configurées
        
        Args:
            category: Catégorie à vérifier ou None pour toutes
            
        Returns:
            Dictionnaire avec le statut de chaque icône
        """
        result = {}
        categories_to_check = [category] if category else ICONS_CONFIG.keys()
        
        for cat in categories_to_check:
            if cat in ICONS_CONFIG:
                result[cat] = {}
                for icon_key, config in ICONS_CONFIG[cat].items():
                    icon_path = self._get_icon_path(cat, config["file"])
                    result[cat][icon_key] = {
                        "file": config["file"],
                        "path": icon_path,
                        "exists": os.path.exists(icon_path),
                        "alt": config.get("alt", ""),
                        "description": config.get("description", ""),
                        "fallback": config.get("fallback", "📊")
                    }
        
        return result
    
    def get_missing_icons(self, category: str = None) -> List[str]:
        """
        Retourne la liste des icônes manquantes
        
        Args:
            category: Catégorie à vérifier ou None pour toutes
            
        Returns:
            Liste des clés d'icônes manquantes
        """
        missing = []
        availability = self.check_icons_availability(category)
        
        for cat, icons in availability.items():
            for icon_key, info in icons.items():
                if not info["exists"]:
                    missing.append(f"{cat}.{icon_key}")
        
        return missing

# Instance globale du gestionnaire d'icônes
icon_manager = IconManager()

# Fonctions helper pour la compatibilité
def get_kpi_icon(icon_key: str, size: str = None) -> str:
    """Fonction helper pour obtenir une icône KPI avec taille configurée"""
    return icon_manager.get_kpi_icon(icon_key, size)

def get_system_icon(icon_key: str, size: str = "24px") -> str:
    """Fonction helper pour obtenir une icône système"""
    return icon_manager.get_system_icon(icon_key, size)

def get_sidebar_icon(icon_key: str, size: str = "20px") -> str:
    """Fonction helper pour obtenir une icône de sidebar"""
    return icon_manager.get_sidebar_icon(icon_key, size)

# Mapping des anciennes fonctions vers les nouvelles clés
KPI_ICON_MAPPING = {
    "score global": "score_global",
    "critères évalués": "criteres_evalues",
    "critères a risque": "criteres_risque",
    "audits": "audits",
    "évolution semestrielle": "evolution_semestrielle",
    "délai moyen": "delai_moyen",
    "prochaine échéance": "prochaine_echeance",
    "etoile": "maturite"
}

def get_icon_html_legacy(icon_name: str, size: str = "48px") -> str:
    """
    Fonction de compatibilité avec l'ancien système
    
    Args:
        icon_name: Nom de l'icône (ancien format)
        size: Taille de l'icône
        
    Returns:
        HTML de l'icône
    """
    # Mapper l'ancien nom vers la nouvelle clé
    icon_key = KPI_ICON_MAPPING.get(icon_name, icon_name)
    return get_kpi_icon(icon_key, size)