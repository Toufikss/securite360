#!/usr/bin/env python3
"""
Script de test pour vérifier l'affichage correct des icônes sidebar
"""

from utils.icons import get_sidebar_icon

def test_sidebar_icons():
    """Test l'affichage des icônes sidebar"""
    print("🧪 Test des icônes sidebar")
    print("=" * 50)
    
    # Liste des icônes à tester
    sidebar_icons = [
        'navigation',
        'dashboard', 
        'politique',
        'declaration',
        'directive', 
        'audits',
        'rapports',
        'users',
        'data_automation',
        'settings'
    ]
    
    success_count = 0
    
    for icon_name in sidebar_icons:
        try:
            icon_html = get_sidebar_icon(icon_name, '20px')
            
            # Vérifier que c'est du HTML valide avec une balise img
            if '<img' in icon_html and 'base64' in icon_html:
                print(f"✅ {icon_name:15} - Icône générée correctement")
                print(f"   Taille HTML: {len(icon_html)} caractères")
                success_count += 1
            else:
                print(f"❌ {icon_name:15} - HTML invalide")
                print(f"   Contenu: {icon_html[:100]}...")
                
        except Exception as e:
            print(f"❌ {icon_name:15} - Erreur: {str(e)}")
    
    print("\n" + "=" * 50)
    print(f"📊 Résultat: {success_count}/{len(sidebar_icons)} icônes fonctionnelles")
    
    if success_count == len(sidebar_icons):
        print("🎉 Tous les tests sont passés !")
        return True
    else:
        print(f"⚠️  {len(sidebar_icons) - success_count} icône(s) ont des problèmes")
        return False

def test_html_rendering():
    """Test le rendu HTML des icônes"""
    print("\n🎨 Test du rendu HTML")
    print("=" * 50)
    
    # Test d'une icône spécifique
    dashboard_icon = get_sidebar_icon('dashboard', '20px')
    
    print("Exemple de rendu - Icône Dashboard:")
    print("-" * 30)
    print(dashboard_icon)
    print("-" * 30)
    
    # Vérifier les éléments clés
    checks = [
        ('<img', 'Balise img présente'),
        ('src="data:image/png;base64,', 'Données base64 présentes'),
        ('alt="', 'Attribut alt présent'),
        ('class="icon sidebar-icon"', 'Classes CSS présentes'),
        ('width: 20px', 'Largeur spécifiée'),
        ('height: 20px', 'Hauteur spécifiée')
    ]
    
    passed_checks = 0
    for check, description in checks:
        if check in dashboard_icon:
            print(f"✅ {description}")
            passed_checks += 1
        else:
            print(f"❌ {description}")
    
    print(f"\n📊 Validation HTML: {passed_checks}/{len(checks)} critères respectés")
    return passed_checks == len(checks)

if __name__ == "__main__":
    print("🚀 Démarrage des tests des icônes sidebar\n")
    
    # Exécuter les tests
    icons_ok = test_sidebar_icons()
    html_ok = test_html_rendering()
    
    print("\n🏁 Résumé final:")
    print("=" * 50)
    
    if icons_ok and html_ok:
        print("✅ Tous les tests sont réussis !")
        print("🎯 Les icônes sidebar devraient s'afficher correctement dans Streamlit")
    else:
        print("❌ Certains tests ont échoué")
        print("⚠️  Vérifiez les erreurs ci-dessus")