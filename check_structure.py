"""
Script pour vérifier la structure des fichiers sur Streamlit Cloud
"""

import os
import sys

def check_file_structure():
    """Vérifie la structure des fichiers"""
    print("📂 Structure des fichiers:")
    print(f"📍 Répertoire courant: {os.getcwd()}")
    print(f"📍 Python path: {sys.path}")
    
    # Lister les fichiers dans le répertoire courant
    print("\n📁 Fichiers dans le répertoire courant:")
    for item in os.listdir('.'):
        if os.path.isdir(item):
            print(f"📁 {item}/")
        else:
            print(f"📄 {item}")
    
    # Vérifier les dossiers importants
    important_dirs = ['utils', 'pages', 'assets', '.streamlit']
    print("\n🔍 Vérification des dossiers importants:")
    
    for dir_name in important_dirs:
        if os.path.exists(dir_name):
            print(f"✅ {dir_name}/ existe")
            if os.path.isdir(dir_name):
                files = os.listdir(dir_name)
                for file in files[:5]:  # Max 5 fichiers
                    print(f"   📄 {file}")
                if len(files) > 5:
                    print(f"   ... et {len(files) - 5} autres fichiers")
        else:
            print(f"❌ {dir_name}/ manquant")

    # Vérifier les fichiers Python importants
    important_files = ['app.py', 'auth.py', 'database.py', 'requirements.txt']
    print("\n📋 Vérification des fichiers importants:")
    
    for file_name in important_files:
        if os.path.exists(file_name):
            size = os.path.getsize(file_name)
            print(f"✅ {file_name} ({size} octets)")
        else:
            print(f"❌ {file_name} manquant")

if __name__ == "__main__":
    print("🔍 VÉRIFICATION STRUCTURE STREAMLIT CLOUD")
    print("=" * 50)
    check_file_structure()