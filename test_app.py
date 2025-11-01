"""
Version simplifiée de app.py pour diagnostic Streamlit Cloud
"""

import streamlit as st

# Configuration minimale
st.set_page_config(
    page_title="Sécurité 360 - Test",
    page_icon="🔐",
    layout="wide"
)

# Test des imports un par un
try:
    st.write("🔍 Test des imports...")
    
    # Test 1: Utils
    from utils.config import APP_NAME, APP_VERSION
    st.success(f"✅ utils.config OK - {APP_NAME} v{APP_VERSION}")
    
    # Test 2: Auth
    from auth import Auth
    st.success("✅ auth OK")
    
    # Test 3: Database  
    from database import Database
    st.success("✅ database OK")
    
    # Test 4: Logo
    from logo import logo_config
    st.success("✅ logo OK")
    
    st.balloons()
    st.success("🎉 Tous les imports réussis ! L'application fonctionne !")
    
except Exception as e:
    st.error(f"❌ Erreur: {e}")
    st.code(str(e))

st.write("🚀 Si vous voyez ce message, Streamlit Cloud fonctionne !")