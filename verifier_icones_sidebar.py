"""
Vérification des Icônes de Sidebar - Sécurité 360
Script pour vérifier la disponibilité des icônes de navigation
"""

import os
from utils.icons import get_sidebar_icon, icon_manager

def verifier_icones_sidebar():
    """Vérifie toutes les icônes de sidebar"""
    
    print("🔍 Vérification des icônes de sidebar")
    print("=" * 50)
    
    # Liste des icônes de navigation requises
    icones_requises = [
        "dashboard",
        "politique", 
        "declaration",
        "directive",
        "audits",
        "rapports",
        "users",
        "data_automation",
        "settings",
        "navigation"
    ]
    
    # Vérifier chaque icône
    toutes_ok = True
    
    for icon_key in icones_requises:
        try:
            # Tester le chargement de l'icône
            icon_html = get_sidebar_icon(icon_key)
            
            # Vérifier si c'est un HTML valide ou un fallback emoji
            if icon_html and len(icon_html) > 10 and "<img" in icon_html:
                print(f"✅ {icon_key:<20} : Icône chargée")
            elif len(icon_html) <= 5:  # Probablement un emoji fallback
                print(f"⚠️  {icon_key:<20} : Utilise le fallback emoji")
                toutes_ok = False
            else:
                print(f"❌ {icon_key:<20} : HTML généré mais suspect")
                toutes_ok = False
                
        except Exception as e:
            print(f"❌ {icon_key:<20} : Erreur - {str(e)}")
            toutes_ok = False
    
    print("=" * 50)
    
    if toutes_ok:
        print("🎉 Toutes les icônes sidebar sont disponibles !")
    else:
        print("⚠️ Certaines icônes utilisent des fallbacks")
    
    return toutes_ok

def verifier_fichiers_physiques():
    """Vérifie la présence des fichiers PNG dans le dossier"""
    
    print("\n📁 Vérification des fichiers physiques")
    print("-" * 40)
    
    dossier_sidebar = "icone sidebar"
    
    if not os.path.exists(dossier_sidebar):
        print(f"❌ Dossier '{dossier_sidebar}' non trouvé")
        return False
    
    # Correspondance entre clés et noms de fichiers
    fichiers_attendus = {
        "dashboard": "tableau de bord.png",
        "politique": "politique de sécurité.png",
        "declaration": "declaration d'applicapilité.png", 
        "directive": "directives et mesures.png",
        "audits": "audites interne.png",
        "rapports": "rapport.png",
        "users": "gestion utilisateurs.png",
        "data_automation": "automatisation.png",
        "settings": "parametres.png",
        "navigation": "navigation.png"
    }
    
    tous_fichiers_ok = True
    
    for icon_key, filename in fichiers_attendus.items():
        filepath = os.path.join(dossier_sidebar, filename)
        
        if os.path.exists(filepath):
            # Vérifier la taille du fichier
            size = os.path.getsize(filepath)
            print(f"✅ {icon_key:<20} : {filename} ({size} bytes)")
        else:
            print(f"❌ {icon_key:<20} : {filename} - MANQUANT")
            tous_fichiers_ok = False
    
    return tous_fichiers_ok

def tester_affichage():
    """Teste l'affichage des icônes"""
    
    print("\n🎨 Test d'affichage des icônes")
    print("-" * 40)
    
    icones_test = ["dashboard", "politique", "audits", "users"]
    
    for icon_key in icones_test:
        try:
            # Différentes tailles
            small = get_sidebar_icon(icon_key, "16px")
            normal = get_sidebar_icon(icon_key, "20px") 
            large = get_sidebar_icon(icon_key, "24px")
            
            print(f"📌 {icon_key}:")
            print(f"   16px: {'✅' if '<img' in small else '⚠️ fallback'}")
            print(f"   20px: {'✅' if '<img' in normal else '⚠️ fallback'}")  
            print(f"   24px: {'✅' if '<img' in large else '⚠️ fallback'}")
            
        except Exception as e:
            print(f"❌ Erreur avec {icon_key}: {str(e)}")

def afficher_statistiques():
    """Affiche les statistiques générales"""
    
    print(f"\n📊 Statistiques")
    print("-" * 40)
    
    # Compter les icônes configurées
    sidebar_icons = icon_manager.list_available_icons().get("sidebar", {})
    
    print(f"• Icônes sidebar configurées: {len(sidebar_icons)}")
    
    # Vérifier le dossier
    dossier_sidebar = "icone sidebar"
    if os.path.exists(dossier_sidebar):
        fichiers_png = [f for f in os.listdir(dossier_sidebar) if f.lower().endswith('.png')]
        print(f"• Fichiers PNG disponibles: {len(fichiers_png)}")
    
    print(f"• Fonction get_sidebar_icon: {'✅ Disponible' if hasattr(icon_manager, 'get_sidebar_icon') else '❌ Manquante'}")

def generer_exemple_code():
    """Génère des exemples de code d'utilisation"""
    
    print(f"\n💻 Exemples de code d'utilisation")
    print("-" * 40)
    
    print("""
# Import
from utils.icons import get_sidebar_icon

# Utilisation basique
dashboard_icon = get_sidebar_icon("dashboard")
politique_icon = get_sidebar_icon("politique", "24px")

# Dans Streamlit
st.markdown(f'{get_sidebar_icon("audits")} Audits internes', unsafe_allow_html=True)

# Menu complet
menu_items = {
    f'{get_sidebar_icon("dashboard")} Tableau de bord': "dashboard",
    f'{get_sidebar_icon("audits")} Audits': "audits"
}
""")

if __name__ == "__main__":
    print("🎨 Vérificateur d'icônes Sidebar - Sécurité 360\n")
    
    # Exécuter toutes les vérifications
    icones_ok = verifier_icones_sidebar()
    fichiers_ok = verifier_fichiers_physiques() 
    
    tester_affichage()
    afficher_statistiques()
    
    # Résumé final
    print(f"\n🎯 Résumé Final")
    print("=" * 50)
    
    if icones_ok and fichiers_ok:
        print("✅ Système d'icônes sidebar prêt !")
        print("🚀 Vous pouvez utiliser les icônes dans l'application")
    else:
        if not fichiers_ok:
            print("❌ Certains fichiers PNG sont manquants")
        if not icones_ok:
            print("⚠️ Certaines icônes utilisent des fallbacks")
    
    generer_exemple_code()
    
    print("\n📱 Pour voir les résultats dans l'application:")
    print("   streamlit run app.py")
    print("   Puis vérifiez la sidebar !")