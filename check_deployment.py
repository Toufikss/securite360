#!/usr/bin/env python3
"""
Script de vérification de la compatibilité de déploiement
Vérifie que tous les modules requis sont disponibles et compatibles
"""

import sys
import importlib
from typing import Dict, List, Tuple

def check_module_availability() -> Dict[str, bool]:
    """Vérifie la disponibilité de tous les modules requis"""
    
    required_modules = {
        # Modules externes
        'streamlit': 'streamlit>=1.31.0',
        'bcrypt': 'bcrypt>=4.1.2',
        'plotly': 'plotly>=5.18.0',
        'pandas': 'pandas>=2.1.4',
        'reportlab': 'reportlab>=4.0.9',
        'PIL': 'Pillow>=10.2.0',
        'typing_extensions': 'typing-extensions>=4.0.0',
        
        # Modules standard Python (doivent être disponibles)
        'sqlite3': 'built-in',
        'pathlib': 'built-in',
        'os': 'built-in',
        'datetime': 'built-in',
        'json': 'built-in',
        'hashlib': 'built-in',
        'base64': 'built-in',
        'io': 'built-in'
    }
    
    results = {}
    
    for module_name, version_info in required_modules.items():
        try:
            importlib.import_module(module_name)
            results[module_name] = True
            print(f"✅ {module_name} - {version_info}")
        except ImportError:
            results[module_name] = False
            print(f"❌ {module_name} - {version_info} - MANQUANT")
    
    return results

def check_python_version() -> bool:
    """Vérifie la version Python"""
    min_version = (3, 11)
    current_version = sys.version_info[:2]
    
    if current_version >= min_version:
        print(f"✅ Python {current_version[0]}.{current_version[1]} (minimum requis: {min_version[0]}.{min_version[1]})")
        return True
    else:
        print(f"❌ Python {current_version[0]}.{current_version[1]} (minimum requis: {min_version[0]}.{min_version[1]})")
        return False

def check_package_structure() -> bool:
    """Vérifie la structure des packages Python"""
    import os
    
    required_init_files = [
        'utils/__init__.py',
        'pages/__init__.py'
    ]
    
    print("📁 Vérification de la structure des packages:")
    all_ok = True
    
    for init_file in required_init_files:
        if os.path.exists(init_file):
            print(f"✅ {init_file}")
        else:
            print(f"❌ {init_file} - MANQUANT")
            all_ok = False
    
    return all_ok

def main():
    """Fonction principale de vérification"""
    print("🔍 Vérification de la compatibilité de déploiement")
    print("=" * 60)
    
    # Vérification version Python
    python_ok = check_python_version()
    print()
    
    # Vérification structure packages
    structure_ok = check_package_structure()
    print()
    
    # Vérification modules
    print("📦 Vérification des modules requis:")
    modules_results = check_module_availability()
    print()
    
    # Test import principal
    print("🧪 Test d'import de l'application:")
    try:
        from utils.config import APP_NAME, APP_VERSION, GLOBAL_CSS, COLORS
        print("✅ Import utils.config réussi")
        app_import_ok = True
    except ImportError as e:
        print(f"❌ Erreur import utils.config: {e}")
        app_import_ok = False
    print()
    
    # Résumé
    all_modules_ok = all(modules_results.values())
    
    if python_ok and structure_ok and all_modules_ok and app_import_ok:
        print("🎉 SUCCÈS: Tous les prérequis sont satisfaits!")
        print("✨ Votre application est prête pour le déploiement!")
        return 0
    else:
        print("⚠️  ATTENTION: Des prérequis sont manquants!")
        if not python_ok:
            print("   - Version Python insuffisante")
        if not structure_ok:
            print("   - Structure de packages incorrecte")
        if not all_modules_ok:
            missing = [k for k, v in modules_results.items() if not v]
            print(f"   - Modules manquants: {', '.join(missing)}")
        if not app_import_ok:
            print("   - Erreur d'import de l'application")
        return 1

if __name__ == "__main__":
    exit(main())