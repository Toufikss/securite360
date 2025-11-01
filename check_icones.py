"""
Utilitaire de maintenance pour les icônes - Sécurité 360
Script pour vérifier, synchroniser et maintenir les icônes KPI
"""

import os
import sys
from pathlib import Path

# Ajouter le dossier parent au path pour les imports
sys.path.append(str(Path(__file__).parent))

try:
    from utils.icons import icon_manager, ICONS_CONFIG, ICONS_PATHS
except ImportError:
    print("❌ Erreur: Impossible d'importer le module icons")
    sys.exit(1)

def check_folder_structure():
    """Vérifie la structure des dossiers d'icônes"""
    print("🔍 Vérification de la structure des dossiers...")
    
    for category, path in ICONS_PATHS.items():
        full_path = os.path.abspath(path)
        exists = os.path.exists(full_path)
        
        status = "✅" if exists else "❌"
        print(f"  {status} {category}: {full_path}")
        
        if exists and os.path.isdir(full_path):
            files = [f for f in os.listdir(full_path) if f.lower().endswith(('.png', '.jpg', '.jpeg', '.svg', '.gif'))]
            print(f"    📁 {len(files)} fichier(s) image trouvé(s)")

def check_configured_icons():
    """Vérifie les icônes configurées vs fichiers disponibles"""
    print("\n📋 Vérification des icônes configurées...")
    
    availability = icon_manager.check_icons_availability()
    total_icons = 0
    missing_icons = 0
    
    for category, icons in availability.items():
        print(f"\n📂 Catégorie: {category}")
        
        for icon_key, info in icons.items():
            total_icons += 1
            status = "✅" if info["exists"] else "❌"
            
            if not info["exists"]:
                missing_icons += 1
            
            print(f"  {status} {icon_key}")
            print(f"      📄 Fichier: {info['file']}")
            print(f"      📍 Chemin: {info['path']}")
            
            if info.get("description"):
                print(f"      📝 Description: {info['description']}")
    
    print(f"\n📊 Résumé:")
    print(f"  • Total icônes configurées: {total_icons}")
    print(f"  • Icônes disponibles: {total_icons - missing_icons}")
    print(f"  • Icônes manquantes: {missing_icons}")
    
    return missing_icons == 0

def list_available_files():
    """Liste tous les fichiers d'icônes disponibles"""
    print("\n📁 Fichiers d'icônes disponibles sur le disque...")
    
    for category, path in ICONS_PATHS.items():
        if os.path.exists(path) and os.path.isdir(path):
            print(f"\n📂 Dossier: {path}")
            
            files = []
            for ext in ['.png', '.jpg', '.jpeg', '.svg', '.gif']:
                files.extend([f for f in os.listdir(path) if f.lower().endswith(ext)])
            
            if files:
                for file in sorted(files):
                    # Vérifier si le fichier est configuré
                    is_configured = False
                    for icon_key, config in ICONS_CONFIG.get(category, {}).items():
                        if config["file"] == file:
                            is_configured = True
                            break
                    
                    status = "✅ Configuré" if is_configured else "⚠️  Non configuré"
                    print(f"  📄 {file} - {status}")
            else:
                print("  (aucun fichier image trouvé)")

def suggest_missing_configurations():
    """Suggère des configurations pour les fichiers non configurés"""
    print("\n💡 Suggestions de configuration pour fichiers non configurés...")
    
    kpi_path = ICONS_PATHS.get("kpi", "icone Indicateurs clés de performance")
    if not os.path.exists(kpi_path):
        print(f"❌ Dossier KPI non trouvé: {kpi_path}")
        return
    
    # Fichiers configurés
    configured_files = set()
    for config in ICONS_CONFIG.get("kpi", {}).values():
        configured_files.add(config["file"])
    
    # Fichiers disponibles
    available_files = []
    for ext in ['.png', '.jpg', '.jpeg', '.svg', '.gif']:
        available_files.extend([f for f in os.listdir(kpi_path) if f.lower().endswith(ext)])
    
    # Fichiers non configurés
    unconfigured = set(available_files) - configured_files
    
    if unconfigured:
        print("\n🔧 Code à ajouter dans utils/icons.py pour les nouveaux fichiers:")
        print('```python')
        
        for file in sorted(unconfigured):
            # Générer une clé basée sur le nom de fichier
            key = file.replace('.png', '').replace(' ', '_').replace('é', 'e').replace('è', 'e').lower()
            
            print(f'        "{key}": {{')
            print(f'            "file": "{file}",')
            print(f'            "alt": "{file.replace(".png", "").title()}",')
            print(f'            "description": "Description pour {file.replace(".png", "")}",')
            print(f'            "fallback": "📊",')
            print(f'            "category": "custom"')
            print(f'        }},')
        
        print('```')
    else:
        print("✅ Tous les fichiers disponibles sont configurés!")

def test_icon_loading():
    """Test le chargement de toutes les icônes"""
    print("\n🧪 Test de chargement des icônes...")
    
    success_count = 0
    error_count = 0
    
    for category in ICONS_CONFIG.keys():
        for icon_key in ICONS_CONFIG[category].keys():
            try:
                html = icon_manager.get_icon_html(category, icon_key, "32px")
                if html and len(html) > 10:  # HTML valide généré
                    success_count += 1
                    print(f"  ✅ {category}.{icon_key}")
                else:
                    error_count += 1
                    print(f"  ⚠️  {category}.{icon_key} - HTML vide")
            except Exception as e:
                error_count += 1
                print(f"  ❌ {category}.{icon_key} - Erreur: {str(e)}")
    
    print(f"\n📊 Résultats des tests:")
    print(f"  • Succès: {success_count}")
    print(f"  • Erreurs: {error_count}")
    
    return error_count == 0

def generate_icon_report():
    """Génère un rapport complet sur les icônes"""
    print("\n📄 Génération du rapport complet...")
    
    report_file = "rapport_icones.md"
    
    with open(report_file, 'w', encoding='utf-8') as f:
        f.write("# Rapport des Icônes - Sécurité 360\n\n")
        f.write(f"Généré le: {__import__('datetime').datetime.now().strftime('%d/%m/%Y %H:%M')}\n\n")
        
        # Configuration actuelle
        f.write("## Configuration Actuelle\n\n")
        
        availability = icon_manager.check_icons_availability()
        
        for category, icons in availability.items():
            f.write(f"### Catégorie: {category}\n\n")
            f.write("| Icône | Fichier | Statut | Description |\n")
            f.write("|-------|---------|--------|-----------|\n")
            
            for icon_key, info in icons.items():
                status = "✅ Disponible" if info["exists"] else "❌ Manquant"
                description = info.get("description", "N/A")
                f.write(f"| {icon_key} | {info['file']} | {status} | {description} |\n")
            
            f.write("\n")
        
        # Statistiques
        f.write("## Statistiques\n\n")
        total = sum(len(icons) for icons in availability.values())
        available = sum(1 for icons in availability.values() 
                       for info in icons.values() if info["exists"])
        
        f.write(f"- **Total icônes configurées:** {total}\n")
        f.write(f"- **Icônes disponibles:** {available}\n") 
        f.write(f"- **Icônes manquantes:** {total - available}\n")
        f.write(f"- **Taux de disponibilité:** {(available/total*100):.1f}%\n\n")
        
        # Instructions
        f.write("## Instructions pour ajouter une nouvelle icône\n\n")
        f.write("1. Placez le fichier PNG dans le dossier approprié\n")
        f.write("2. Éditez `utils/icons.py` pour ajouter la configuration\n")
        f.write("3. Utilisez `get_kpi_icon(\"votre_cle\")` dans votre code\n")
    
    print(f"✅ Rapport généré: {report_file}")

def main():
    """Fonction principale"""
    print("🎨 Utilitaire de maintenance des icônes - Sécurité 360\n")
    
    # Vérifications
    check_folder_structure()
    all_ok = check_configured_icons()
    list_available_files()
    suggest_missing_configurations()
    
    # Tests
    test_ok = test_icon_loading()
    
    # Rapport
    generate_icon_report()
    
    # Résumé final
    print(f"\n🎯 Résumé final:")
    
    if all_ok and test_ok:
        print("✅ Tous les tests sont passés!")
        print("✅ Toutes les icônes sont disponibles et fonctionnelles.")
    else:
        print("⚠️  Certains problèmes ont été détectés.")
        print("📋 Consultez le rapport généré pour plus de détails.")
    
    missing = icon_manager.get_missing_icons()
    if missing:
        print(f"\n❌ Icônes manquantes: {', '.join(missing)}")
    
    print(f"\n💡 Pour utiliser les icônes dans votre code:")
    print("```python")
    print("from utils.icons import get_kpi_icon")
    print('icone_html = get_kpi_icon("score_global")')
    print("```")

if __name__ == "__main__":
    main()