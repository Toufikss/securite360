# -*- coding: utf-8 -*-
"""
Verification des imports pour le deploiement
Ce fichier aide a diagnostiquer les problemes d'importation
"""

try:
    import streamlit as st
    print("OK Streamlit importe avec succes")
except ImportError as e:
    print(f"ERREUR Streamlit: {e}")

try:
    import sqlite3
    print("OK SQLite3 importe avec succes")
except ImportError as e:
    print(f"ERREUR SQLite3: {e}")

try:
    import bcrypt
    print("OK BCrypt importe avec succes")
except ImportError as e:
    print(f"ERREUR BCrypt: {e}")

try:
    from pathlib import Path
    print("OK Pathlib importe avec succes")
except ImportError as e:
    print(f"ERREUR Pathlib: {e}")

try:
    from database import Database
    print("OK Database importe avec succes")
except ImportError as e:
    print(f"ERREUR Database: {e}")

try:
    from auth import Auth
    print("OK Auth importe avec succes")
except ImportError as e:
    print(f"ERREUR Auth: {e}")

try:
    from logo import logo_config
    print("OK Logo importe avec succes")
except ImportError as e:
    print(f"ERREUR Logo: {e}")

print("Verification terminee")