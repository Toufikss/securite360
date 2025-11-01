"""
Configuration du logo pour l'application Sécurité 360
Modifiez ce fichier pour changer facilement le logo
"""

import streamlit as st
import os
from pathlib import Path

class LogoConfig:
    def __init__(self):
        """Configuration du logo"""
        # Nom du fichier logo (à placer dans le même dossier que ce fichier)
        self.LOGO_FILENAME = "logo_securite360.png"
        
        # Taille d'affichage du logo (en pixels) - Réduite pour un meilleur affichage
        self.LOGO_WIDTH = 200

        # Styles CSS simplifiés (plus de boîte/ombre)
        self.LOGO_STYLES = """
        /* Styles de base pour le logo - sans ombre ni bordure */
        .logo-container {
            text-align: center;
            margin: 1rem 0 2rem 0;
            padding: 1rem 0;
        }
        """
    
    def get_logo_path(self):
        """Retourne le chemin vers le fichier logo"""
        current_dir = Path(__file__).parent
        logo_path = current_dir / self.LOGO_FILENAME
        return str(logo_path)
    
    def logo_exists(self):
        """Vérifie si le fichier logo existe"""
        return os.path.exists(self.get_logo_path())
    
    def display_logo(self):
        """Affiche le logo dans l'interface"""
        if self.logo_exists():
            # CSS pour le logo
            st.markdown(f"<style>{self.LOGO_STYLES}</style>", unsafe_allow_html=True)
            
            # Affichage du logo parfaitement centré avec HTML
            import base64
            with open(self.get_logo_path(), "rb") as f:
                logo_data = base64.b64encode(f.read()).decode()
            
            centered_logo_html = f"""
            <div style="
                display: flex;
                justify-content: center;
                align-items: center;
                width: 100%;
                margin: 1rem 0 2rem 0;
                padding: 1rem 0;
            ">
                <img src="data:image/png;base64,{logo_data}" 
                     style="
                         width: {self.LOGO_WIDTH}px;
                         transition: all 0.3s ease;
                     "
                     onmouseover="this.style.transform='scale(1.05)';"
                     onmouseout="this.style.transform='scale(1)';"
                />
            </div>
            """
            st.markdown(centered_logo_html, unsafe_allow_html=True)
        else:
            # Message si le logo n'est pas trouvé
            st.warning(f"⚠️ Logo non trouvé: {self.LOGO_FILENAME}")
            st.info("""
            **Pour ajouter votre logo :**
            1. Placez votre fichier PNG dans le dossier de l'application
            2. Renommez-le : `logo_securite360.png`
            3. Ou modifiez le nom dans le fichier `logo.py`
            """)
    
    def get_fallback_logo(self):
        """Retourne un logo de secours (CSS) si le PNG n'existe pas"""
        return """
        <div class="fallback-logo">
            <div style="
                width: 80px;
                height: 80px;
                background: linear-gradient(135deg, #3b82f6 0%, #1d4ed8 100%);
                border-radius: 50%;
                margin: 0 auto 1rem auto;
                display: flex;
                align-items: center;
                justify-content: center;
                box-shadow: 0 4px 15px rgba(59, 130, 246, 0.3);
            ">
                <span style="color: white; font-size: 24px; font-weight: bold;">S360</span>
            </div>
        </div>
        """

# Instance globale pour faciliter l'utilisation
logo_config = LogoConfig()

# Instructions pour changer le logo
INSTRUCTIONS_LOGO = """
## 📝 Comment changer le logo :

### Méthode 1 : Remplacer le fichier
1. Placez votre nouveau logo PNG dans le dossier de l'application
2. Renommez-le exactement : `logo_securite360.png`
3. Redémarrez l'application

### Méthode 2 : Modifier la configuration
1. Ouvrez le fichier `logo.py`
2. Changez la ligne : `self.LOGO_FILENAME = "votre_nouveau_logo.png"`
3. Ajustez la taille si nécessaire : `self.LOGO_WIDTH = 250`
4. Redémarrez l'application

### Formats supportés :
- PNG (recommandé)
- JPG/JPEG
- SVG
- GIF

### Taille recommandée :
- Largeur : 200-400 pixels
- Format : Carré ou rectangulaire
- Fond transparent (PNG) pour un meilleur rendu
"""