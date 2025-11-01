"""
Test ultra-basique sans aucune configuration
"""

import streamlit as st

# Absolument aucune configuration - utilise les défauts Streamlit
st.write("Hello World from Streamlit Cloud!")
st.success("✅ Test réussi !")

if st.button("Test Button"):
    st.balloons()
    st.write("🎉 Button works!")