#!/usr/bin/env python3
"""
Script de build automatisé pour Sécurité 360
Crée l'exécutable Windows avec PyInstaller
"""
import os
import sys
import shutil
import subprocess
from pathlib import Path

def check_requirements():
    """Vérifie que tous les prérequis sont installés"""
    print("📋 Vérification des prérequis...")
    
    required_packages = [
        'pyinstaller', 'streamlit', 'pillow', 'pandas', 
        'plotly', 'bcrypt', 'reportlab'
    ]
    
    missing = []
    for package in required_packages:
        try:
            __import__(package.replace('-', '_'))
            print(f"✅ {package}")
        except ImportError:
            missing.append(package)
            print(f"❌ {package}")
    
    if missing:
        print(f"\n🚨 Packages manquants: {', '.join(missing)}")
        print("Installez-les avec: pip install " + ' '.join(missing))
        return False
    
    return True

def clean_build_dirs():
    """Nettoie les dossiers de build précédents"""
    print("\n🧹 Nettoyage des builds précédents...")
    
    dirs_to_clean = ['build', 'dist', '__pycache__']
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ Supprimé: {dir_name}")

def build_executable():
    """Lance la création de l'exécutable avec PyInstaller"""
    print("\n🔨 Création de l'exécutable...")
    print("Cela peut prendre plusieurs minutes...")
    
    # Commande PyInstaller
    cmd = [
        'pyinstaller',
        '--clean',
        '--noconfirm',
        'Securite360.spec'
    ]
    
    print(f"🚀 Commande: {' '.join(cmd)}")
    
    try:
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        print("✅ Build réussi !")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erreur lors du build:")
        print(e.stdout)
        print(e.stderr)
        return False

def verify_build():
    """Vérifie que l'exécutable a été créé correctement"""
    print("\n🔍 Vérification du build...")
    
    exe_path = Path("dist/Securite360.exe")
    if exe_path.exists():
        size_mb = exe_path.stat().st_size / (1024 * 1024)
        print(f"✅ Exécutable créé: {exe_path}")
        print(f"📏 Taille: {size_mb:.1f} MB")
        return True
    else:
        print("❌ Exécutable non trouvé dans dist/")
        return False

def main():
    """Point d'entrée principal"""
    print("=" * 60)
    print("🛡️  BUILD SÉCURITÉ 360 - EXÉCUTABLE WINDOWS")
    print("=" * 60)
    
    # Vérifications préliminaires
    if not check_requirements():
        sys.exit(1)
    
    if not os.path.exists('launcher.py'):
        print("❌ fichier launcher.py non trouvé")
        sys.exit(1)
    
    if not os.path.exists('Securite360.spec'):
        print("❌ Fichier Securite360.spec non trouvé")
        sys.exit(1)
    
    if not os.path.exists('icone.ico'):
        print("❌ Fichier icone.ico non trouvé")
        sys.exit(1)
    
    # Processus de build
    clean_build_dirs()
    
    if not build_executable():
        sys.exit(1)
    
    if not verify_build():
        sys.exit(1)
    
    print("\n🎉 BUILD TERMINÉ AVEC SUCCÈS !")
    print("📁 L'exécutable se trouve dans: dist/Securite360.exe")
    print("\n📋 Instructions d'utilisation:")
    print("1. Copiez dist/Securite360.exe où vous voulez")
    print("2. Double-cliquez pour lancer l'application")
    print("3. Le splash screen apparaîtra pendant 3 secondes")
    print("4. Puis votre navigateur s'ouvrira automatiquement")
    print("\n✨ Aucune installation de Python n'est nécessaire !")

if __name__ == '__main__':
    main()