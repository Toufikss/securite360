"""
Vérification Rapide - Tailles d'Icônes KPI
Script pour confirmer que toutes les icônes sont à 80px
"""

from utils.icon_sizes import get_all_kpi_sizes, ICON_SIZES

def verifier_tailles_kpi():
    """Vérifie que toutes les icônes KPI sont à 80px"""
    
    print("🔍 Vérification des tailles d'icônes KPI")
    print("=" * 50)
    
    # Récupérer toutes les tailles configurées
    all_sizes = get_all_kpi_sizes()
    
    # Vérifier chaque icône
    toutes_80px = True
    
    for icon_key, size in all_sizes.items():
        status = "✅" if size == "80px" else "❌"
        print(f"{status} {icon_key:<25} : {size}")
        
        if size != "80px":
            toutes_80px = False
    
    print("=" * 50)
    
    if toutes_80px:
        print("🎉 PARFAIT ! Toutes les icônes KPI sont à 80px")
        print("📊 Taille uniforme appliquée avec succès")
    else:
        print("⚠️ Certaines icônes ne sont pas à 80px")
    
    print(f"\n📈 Total icônes configurées: {len(all_sizes)}")
    print(f"📏 Taille cible: 80px (xl)")
    
    return toutes_80px

def afficher_configuration():
    """Affiche la configuration complète des tailles"""
    
    print("\n🎨 Configuration des Tailles Disponibles:")
    print("-" * 40)
    
    for size_name, size_value in ICON_SIZES.items():
        marker = "⭐" if size_value == "80px" else "  "
        print(f"{marker} {size_name:<8} : {size_value}")
    
    print("\n⭐ = Taille utilisée pour les icônes KPI")

if __name__ == "__main__":
    # Vérification principale
    resultat = verifier_tailles_kpi()
    
    # Afficher la configuration
    afficher_configuration()
    
    # Instructions pour l'utilisateur
    print("\n" + "=" * 50)
    print("💡 INSTRUCTIONS:")
    print("1. Toutes vos icônes KPI sont maintenant à 80px")
    print("2. Rechargez votre dashboard: http://localhost:8501")
    print("3. Les icônes seront plus grandes et uniformes")
    
    if resultat:
        print("\n🚀 Configuration appliquée avec succès !")
    else:
        print("\n🔧 Vérifiez le fichier utils/icon_sizes.py")