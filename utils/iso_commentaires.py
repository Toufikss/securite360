"""
Module pour charger les commentaires ISO 27001 depuis le fichier JSON
"""

import json
from typing import Dict, Optional

# Cache pour éviter de recharger le fichier à chaque fois
_commentaires_cache: Dict[str, str] = {}

def load_commentaires(file_path: str = "iso27001_annexe_a.json") -> Dict[str, str]:
    """
    Charge les commentaires depuis le fichier JSON
    
    Args:
        file_path: Chemin vers le fichier JSON
        
    Returns:
        Dictionnaire avec code -> commentaire
    """
    global _commentaires_cache
    
    # Utiliser le cache si disponible
    if _commentaires_cache:
        return _commentaires_cache
    
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        
        # Extraire les commentaires
        for critere in data.get('criteres', []):
            code = critere.get('code')
            commentaire = critere.get('commentaire', '')
            if code and commentaire:
                _commentaires_cache[code] = commentaire
        
        return _commentaires_cache
    
    except Exception as e:
        print(f"Erreur lors du chargement des commentaires ISO: {e}")
        return {}


def get_commentaire(code: str, file_path: str = "iso27001_annexe_a.json") -> Optional[str]:
    """
    Récupère le commentaire d'un critère spécifique
    
    Args:
        code: Code du critère (ex: "5.1")
        file_path: Chemin vers le fichier JSON
        
    Returns:
        Commentaire du critère ou None si non trouvé
    """
    commentaires = load_commentaires(file_path)
    return commentaires.get(code)


def clear_cache():
    """Vide le cache des commentaires"""
    global _commentaires_cache
    _commentaires_cache = {}
