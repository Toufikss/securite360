"""
Module de gestion des logos - Sécurité 360
Centralise la gestion et l'affichage des logos pour l'application
"""

import base64
import os
import streamlit as st
from typing import Optional, Dict, Tuple
from pathlib import Path

# Configuration des logos
LOGOS_CONFIG = {
    # Logo principal de l'application
    "main": {
        "file": "logo_securite360.png",
        "alt": "Logo Sécurité 360",
        "width": 200,
        "fallback": {
            "type": "css",
            "content": "S360",
            "background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)"
        }
    },
    
    # Logo pour la sidebar
    "sidebar": {
        "file": "logo_securite360.png",
        "alt": "Logo Sécurité 360 - Sidebar",
        "width": 150,
        "fallback": {
            "type": "css", 
            "content": "S360",
            "background": "linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%)"
        }
    },
    
    # Logo compact pour les headers
    "header": {
        "file": "logo_compact.png",
        "alt": "Logo Compact",
        "width": 100,
        "fallback": {
            "type": "text",
            "content": "🔐 S360"
        }
    },
    
    # Favicon
    "favicon": {
        "file": "icone.ico",
        "alt": "Favicon",
        "width": 32,
        "fallback": {
            "type": "emoji",
            "content": "🔐"
        }
    },
    
    # Logo pour rapports/exports
    "report": {
        "file": "logo_report.png", 
        "alt": "Logo Rapport",
        "width": 300,
        "fallback": {
            "type": "css",
            "content": "SÉCURITÉ 360",
            "background": "linear-gradient(135deg, #1f2937 0%, #374151 100%)"
        }
    }
}

# Chemins des dossiers de logos
LOGOS_PATHS = {
    "main": ".",  # Racine du projet
    "assets": "assets/logos",
    "icons": "assets/icons",
    "reports": "assets/reports"
}

# Styles CSS pour les logos
LOGO_STYLES = {
    "main": """
    .logo-main {
        display: flex;
        justify-content: center;
        align-items: center;
        width: 100%;
        margin: 1rem 0 2rem 0;
        padding: 1rem 0;
    }
    .logo-main img {
        transition: all 0.3s ease;
        filter: drop-shadow(0 4px 8px rgba(0,0,0,0.1));
    }
    .logo-main img:hover {
        transform: scale(1.05);
        filter: drop-shadow(0 6px 12px rgba(0,0,0,0.15));
    }
    """,
    
    "sidebar": """
    .logo-sidebar {
        text-align: center;
        margin: 0.5rem 0 1rem 0;
        padding: 0.5rem 0;
    }
    .logo-sidebar img {
        transition: opacity 0.3s ease;
    }
    .logo-sidebar img:hover {
        opacity: 0.8;
    }
    """,
    
    "header": """
    .logo-header {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
    }
    .logo-header img {
        vertical-align: middle;
    }
    """,
    
    "compact": """
    .logo-compact {
        display: inline-block;
        vertical-align: middle;
    }
    """
}

class LogoManager:
    """Gestionnaire des logos pour l'application"""
    
    def __init__(self):
        self._logo_cache: Dict[str, str] = {}
    
    def _get_logo_path(self, logo_key: str) -> str:
        """Construit le chemin complet vers un fichier logo"""
        logo_config = LOGOS_CONFIG.get(logo_key)
        if not logo_config:
            return ""
        
        # Déterminer le dossier de base
        if logo_config["file"].endswith(".ico"):
            base_path = LOGOS_PATHS.get("icons", ".")
        elif "report" in logo_key:
            base_path = LOGOS_PATHS.get("reports", ".")
        else:
            base_path = LOGOS_PATHS.get("main", ".")
        
        return os.path.join(base_path, logo_config["file"])
    
    def _load_logo_as_base64(self, logo_path: str) -> Optional[str]:
        """
        Charge un logo et le convertit en base64
        
        Args:
            logo_path: Chemin vers le fichier logo
            
        Returns:
            String base64 du logo ou None si erreur
        """
        cache_key = f"logo_{logo_path}"
        
        # Vérifier le cache
        if cache_key in self._logo_cache:
            return self._logo_cache[cache_key]
        
        try:
            if os.path.exists(logo_path):
                with open(logo_path, "rb") as f:
                    logo_data = base64.b64encode(f.read()).decode()
                    self._logo_cache[cache_key] = logo_data
                    return logo_data
        except Exception as e:
            st.error(f"Erreur lors du chargement du logo {logo_path}: {str(e)}")
        
        return None
    
    def _get_fallback_logo(self, logo_key: str) -> str:
        """
        Génère un logo de fallback
        
        Args:
            logo_key: Clé du logo
            
        Returns:
            HTML du logo de fallback
        """
        logo_config = LOGOS_CONFIG.get(logo_key, {})
        fallback = logo_config.get("fallback", {})
        width = logo_config.get("width", 200)
        
        fallback_type = fallback.get("type", "text")
        content = fallback.get("content", "LOGO")
        
        if fallback_type == "css":
            background = fallback.get("background", "#3b82f6")
            size = min(width, 80)  # Taille max pour les logos CSS
            
            return f"""
            <div class="fallback-logo-css" style="
                width: {size}px;
                height: {size}px;
                background: {background};
                border-radius: 50%;
                margin: 0 auto;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 15px rgba(0,0,0,0.2);
                color: white;
                font-size: {size//4}px;
                font-weight: bold;
                font-family: 'Inter', sans-serif;
            ">
                {content}
            </div>
            """
        elif fallback_type == "emoji":
            return f'<span style="font-size: {width//8}px;">{content}</span>'
        else:  # text
            return f'<span style="font-weight: bold; color: #3b82f6;">{content}</span>'
    
    def get_logo_html(self, 
                      logo_key: str, 
                      width: Optional[int] = None,
                      css_class: str = "",
                      style: str = "") -> str:
        """
        Génère le HTML pour afficher un logo
        
        Args:
            logo_key: Clé du logo dans la configuration
            width: Largeur personnalisée (optionnel)
            css_class: Classes CSS additionnelles
            style: Styles CSS inline additionnels
            
        Returns:
            HTML du logo ou fallback
        """
        try:
            # Récupérer la configuration du logo
            logo_config = LOGOS_CONFIG.get(logo_key)
            if not logo_config:
                return self._get_fallback_logo("main")  # Logo par défaut
            
            # Construire le chemin du fichier
            logo_path = self._get_logo_path(logo_key)
            
            # Charger le logo
            logo_b64 = self._load_logo_as_base64(logo_path)
            
            if logo_b64:
                logo_width = width or logo_config["width"]
                css_classes = f"logo-{logo_key} {css_class}".strip()
                
                # Déterminer le type MIME
                file_ext = Path(logo_path).suffix.lower()
                if file_ext == ".png":
                    mime_type = "image/png"
                elif file_ext in [".jpg", ".jpeg"]:
                    mime_type = "image/jpeg"
                elif file_ext == ".svg":
                    mime_type = "image/svg+xml"
                elif file_ext == ".gif":
                    mime_type = "image/gif"
                else:
                    mime_type = "image/png"  # Par défaut
                
                return f'''<img src="data:{mime_type};base64,{logo_b64}" 
                              alt="{logo_config['alt']}" 
                              class="{css_classes}"
                              style="width: {logo_width}px; {style}">'''
            else:
                # Fallback
                return self._get_fallback_logo(logo_key)
                
        except Exception as e:
            st.error(f"Erreur lors de la génération du logo {logo_key}: {str(e)}")
            return self._get_fallback_logo("main")
    
    def display_logo(self, 
                     logo_key: str = "main", 
                     width: Optional[int] = None,
                     container_class: str = "") -> None:
        """
        Affiche un logo avec ses styles CSS
        
        Args:
            logo_key: Clé du logo à afficher
            width: Largeur personnalisée (renommé de custom_width)
            container_class: Classe CSS du conteneur
        """
        # Injecter les styles CSS
        style_key = logo_key if logo_key in LOGO_STYLES else "main"
        st.markdown(f"<style>{LOGO_STYLES[style_key]}</style>", unsafe_allow_html=True)
        
        # Générer le HTML du logo
        logo_html = self.get_logo_html(logo_key, width)
        
        # Conteneur avec classe appropriée
        container_css = f"logo-{style_key} {container_class}".strip()
        
        st.markdown(f'''
        <div class="{container_css}">
            {logo_html}
        </div>
        ''', unsafe_allow_html=True)
    
    def get_main_logo(self, width: Optional[int] = None) -> str:
        """Raccourci pour obtenir le logo principal"""
        return self.get_logo_html("main", width, "main-logo")
    
    def get_sidebar_logo(self, width: Optional[int] = None) -> str:
        """Raccourci pour obtenir le logo sidebar"""
        return self.get_logo_html("sidebar", width, "sidebar-logo")
    
    def get_header_logo(self, width: Optional[int] = None) -> str:
        """Raccourci pour obtenir le logo header"""
        return self.get_logo_html("header", width, "header-logo")
    
    def list_available_logos(self) -> Dict:
        """Liste les logos disponibles"""
        return LOGOS_CONFIG
    
    def add_custom_logo(self, 
                       logo_key: str, 
                       filename: str, 
                       alt_text: str, 
                       width: int = 200,
                       fallback_content: str = "LOGO"):
        """
        Ajoute un logo personnalisé à la configuration
        
        Args:
            logo_key: Clé unique pour le logo
            filename: Nom du fichier logo
            alt_text: Texte alternatif
            width: Largeur par défaut
            fallback_content: Contenu de fallback
        """
        LOGOS_CONFIG[logo_key] = {
            "file": filename,
            "alt": alt_text,
            "width": width,
            "fallback": {
                "type": "text",
                "content": fallback_content
            }
        }
    
    def clear_cache(self):
        """Vide le cache des logos"""
        self._logo_cache.clear()
    
    def preload_logos(self):
        """Précharge tous les logos en mémoire"""
        for logo_key in LOGOS_CONFIG.keys():
            logo_path = self._get_logo_path(logo_key)
            self._load_logo_as_base64(logo_path)
    
    def logo_exists(self, logo_key: str) -> bool:
        """Vérifie si un logo existe"""
        logo_path = self._get_logo_path(logo_key)
        return os.path.exists(logo_path)
    
    def get_logo_info(self, logo_key: str) -> Dict:
        """Obtient les informations d'un logo"""
        config = LOGOS_CONFIG.get(logo_key, {})
        logo_path = self._get_logo_path(logo_key)
        
        return {
            "key": logo_key,
            "file": config.get("file", ""),
            "path": logo_path,
            "exists": os.path.exists(logo_path),
            "alt": config.get("alt", ""),
            "width": config.get("width", 200),
            "fallback": config.get("fallback", {})
        }

# Instance globale du gestionnaire de logos
logo_manager = LogoManager()

# Fonctions helper pour la compatibilité
def display_logo(logo_key: str = "main", width: Optional[int] = None):
    """Fonction helper pour afficher un logo"""
    logo_manager.display_logo(logo_key, width)

def get_main_logo(width: Optional[int] = None) -> str:
    """Fonction helper pour obtenir le logo principal"""
    return logo_manager.get_main_logo(width)

def get_sidebar_logo(width: Optional[int] = None) -> str:
    """Fonction helper pour obtenir le logo sidebar"""
    return logo_manager.get_sidebar_logo(width)

# Classe de compatibilité avec l'ancien système
class LogoConfig:
    """Classe de compatibilité avec l'ancien système logo.py"""
    
    def __init__(self):
        self.LOGO_FILENAME = "logo_securite360.png"
        self.LOGO_WIDTH = 200
        self.LOGO_STYLES = LOGO_STYLES["main"]
    
    def get_logo_path(self):
        return logo_manager._get_logo_path("main")
    
    def logo_exists(self):
        return logo_manager.logo_exists("main")
    
    def display_logo(self):
        logo_manager.display_logo("main")
    
    def get_fallback_logo(self):
        return logo_manager._get_fallback_logo("main")

# Instance de compatibilité
logo_config = LogoConfig()