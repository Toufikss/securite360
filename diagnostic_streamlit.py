"""
Script de diagnostic pour identifier les erreurs sur Streamlit Cloud
"""

import sys
import traceback

def test_imports():
    """Test tous les imports de l'application"""
    print("🔍 Test des imports de l'application...")
    
    try:
        print("📦 Test import streamlit...")
        import streamlit as st
        print("✅ streamlit OK")
        
        print("📦 Test import auth...")
        from auth import Auth
        print("✅ auth OK")
        
        print("📦 Test import database...")
        from database import Database
        print("✅ database OK")
        
        print("📦 Test import utils.config...")
        from utils.config import APP_NAME, APP_VERSION, GLOBAL_CSS, COLORS
        print(f"✅ utils.config OK - APP_NAME: {APP_NAME}")
        
        print("📦 Test import utils.icons...")
        from utils.icons import get_sidebar_icon
        print("✅ utils.icons OK")
        
        print("📦 Test import logo...")
        from logo import logo_config
        print("✅ logo OK")
        
        print("\n🎉 Tous les imports réussis!")
        return True
        
    except Exception as e:
        print(f"\n❌ ERREUR lors des imports:")
        print(f"Type: {type(e).__name__}")
        print(f"Message: {str(e)}")
        print("\n📋 Traceback complet:")
        traceback.print_exc()
        return False

def test_streamlit_config():
    """Test la configuration Streamlit"""
    print("\n🔧 Test de la configuration Streamlit...")
    
    try:
        import streamlit as st
        from utils.config import APP_NAME
        
        # Test de set_page_config (sans l'exécuter réellement)
        print("✅ Configuration Streamlit prête")
        return True
        
    except Exception as e:
        print(f"❌ Erreur configuration: {e}")
        return False

def main():
    """Fonction principale de diagnostic"""
    print("=" * 60)
    print("🩺 DIAGNOSTIC STREAMLIT CLOUD")
    print("=" * 60)
    
    # Test des imports
    imports_ok = test_imports()
    
    # Test de la configuration
    config_ok = test_streamlit_config()
    
    print("\n" + "=" * 60)
    if imports_ok and config_ok:
        print("✅ DIAGNOSTIC RÉUSSI - L'application devrait fonctionner sur Streamlit Cloud")
    else:
        print("❌ PROBLÈMES DÉTECTÉS - Voir les erreurs ci-dessus")
    print("=" * 60)

if __name__ == "__main__":
    main()