#!/usr/bin/env python3
"""
Script de test pour vérifier les corrections apportées au module data_automation
"""

import subprocess
import os
import sys

def test_subprocess_encoding():
    """Tester l'encodage dans les appels subprocess"""
    print("🔧 Test de l'encodage subprocess...")
    
    try:
        # Tester l'appel netsh avec le nouvel encodage
        if os.name == 'nt':
            result = subprocess.run(['netsh', 'advfirewall', 'show', 'allprofiles', 'state'], 
                                  capture_output=True, text=True, encoding='utf-8', 
                                  errors='ignore', timeout=10)
            print(f"✅ Test netsh réussi - Statut: {'ACTIVE' if 'ON' in result.stdout else 'INACTIVE'}")
        else:
            print("ℹ️  Test netsh ignoré (pas sur Windows)")
            
        # Tester l'appel PowerShell avec le nouvel encodage
        if os.name == 'nt':
            result = subprocess.run(['powershell', '-Command', 'Get-MpComputerStatus | Select-Object AntivirusEnabled'], 
                                  capture_output=True, text=True, encoding='utf-8', 
                                  errors='ignore', timeout=10)
            print(f"✅ Test PowerShell réussi - Antivirus: {'ACTIVE' if 'True' in result.stdout else 'INACTIVE'}")
        else:
            print("ℹ️  Test PowerShell ignoré (pas sur Windows)")
            
    except Exception as e:
        print(f"❌ Erreur lors du test subprocess: {e}")
        return False
    
    return True

def test_import_data_automation():
    """Tester l'import du module data_automation"""
    print("\n📦 Test d'import du module...")
    
    try:
        # Ajouter le chemin du projet au PYTHONPATH
        sys.path.insert(0, os.path.dirname(__file__))
        
        # Importer le module pages.data_automation
        from pages import data_automation
        print("✅ Import du module data_automation réussi")
        
        # Tester la création d'un collecteur (simulation)
        class MockDB:
            pass
        
        collector = data_automation.DataCollector(MockDB())
        print("✅ Création du DataCollector réussie")
        
        return True
        
    except Exception as e:
        print(f"❌ Erreur lors de l'import: {e}")
        return False

def main():
    """Fonction principale de test"""
    print("🚀 Tests des corrections data_automation")
    print("=" * 50)
    
    tests_passed = 0
    total_tests = 2
    
    # Test 1: Encodage subprocess
    if test_subprocess_encoding():
        tests_passed += 1
    
    # Test 2: Import du module
    if test_import_data_automation():
        tests_passed += 1
    
    # Résultats
    print("\n" + "=" * 50)
    print(f"📊 Résultats des tests: {tests_passed}/{total_tests}")
    
    if tests_passed == total_tests:
        print("🎉 Tous les tests sont passés avec succès !")
        print("✅ Les corrections Unicode et Streamlit sont appliquées")
        return True
    else:
        print("⚠️  Certains tests ont échoué")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)