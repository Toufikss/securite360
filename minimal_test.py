"""
Version ultra-minimale pour diagnostic Streamlit Cloud
Aucun import custom - seulement Streamlit de base
"""

import streamlit as st

st.title("🔐 Test Minimal Sécurité 360")
st.success("✅ Si vous voyez ce message, Streamlit fonctionne !")
st.write("🚀 Application de test démarrée avec succès")

# Test très basique
st.write("📊 Test d'affichage:")
st.metric("Status", "OK", "100%")

st.balloons()