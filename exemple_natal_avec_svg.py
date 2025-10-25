#!/usr/bin/env python3
"""
Exemple d'utilisation de l'endpoint natal avec SVG intégré
"""

import requests
import json
import base64

def exemple_natal_complet():
    """Exemple complet d'utilisation de l'endpoint natal avec SVG"""
    print("🌟 EXEMPLE : ENDPOINT NATAL AVEC SVG INTÉGRÉ")
    print("=" * 60)
    
    # Données de naissance
    data = {
        "name": "Marie Dubois",
        "year": 1990,
        "month": 6,
        "day": 15,
        "hour": 14,
        "minute": 30,
        "city": "Paris",
        "nation": "FR",
        # Options SVG
        "theme": "dark",
        "language": "FR"
    }
    
    print("📤 Envoi de la requête...")
    print(f"   Nom: {data['name']}")
    print(f"   Date: {data['day']}/{data['month']}/{data['year']}")
    print(f"   Heure: {data['hour']}:{data['minute']:02d}")
    print(f"   Lieu: {data['city']}, {data['nation']}")
    print(f"   Thème: {data['theme']}")
    print(f"   Langue: {data['language']}")
    print()
    
    try:
        response = requests.post("http://localhost:3000/api/natal", json=data, timeout=60)
        
        if response.status_code == 200:
            result = response.json()
            data = result['data']
            
            print("✅ RÉPONSE REÇUE AVEC SUCCÈS!")
            print()
            
            # Informations de base
            print("👤 INFORMATIONS PERSONNELLES:")
            basic_info = data['basic_info']
            print(f"   Nom: {basic_info['name']}")
            print(f"   Date de naissance: {basic_info['birth_date']}")
            print(f"   Heure: {basic_info['birth_time']}")
            print(f"   Lieu: {basic_info['location']}")
            print(f"   Coordonnées: {basic_info['coordinates']['latitude']:.4f}°N, {basic_info['coordinates']['longitude']:.4f}°E")
            print()
            
            # Positions planétaires
            print("🪐 POSITIONS PLANÉTAIRES:")
            for planet, info in data['planets'].items():
                if 'sign' in info and 'position' in info:
                    print(f"   {info['planet_name']}: {info['sign']} ({info['position']:.2f}°)")
            print()
            
            # Maisons astrologiques
            print("🏠 MAISONS ASTROLOGIQUES:")
            for house, info in data['houses'].items():
                if 'sign' in info:
                    house_name = house.replace('_', ' ').title()
                    print(f"   {house_name}: {info['sign']}")
            print()
            
            # Interprétations
            print("🔮 INTERPRÉTATIONS:")
            for key, interpretation in data['interpretations'].items():
                print(f"   • {interpretation}")
            print()
            
            # SVG
            if 'svg' in data:
                svg_info = data['svg']
                print("🎨 CARTE DU CIEL SVG:")
                print(f"   Généré: {'✅ Oui' if svg_info['generated'] else '❌ Non'}")
                print(f"   Fichier: {svg_info['filename']}")
                
                if svg_info['generated'] and svg_info['base64']:
                    print(f"   Taille: {len(svg_info['base64'])} caractères")
                    
                    # Sauvegarder le SVG
                    svg_content = base64.b64decode(svg_info['base64'])
                    filename = f"exemple_{svg_info['filename']}"
                    
                    with open(filename, 'wb') as f:
                        f.write(svg_content)
                    
                    print(f"   💾 Sauvegardé: {filename}")
                    print("   🌐 Ouvrez le fichier dans un navigateur pour voir la carte!")
                else:
                    print(f"   ❌ Erreur: {svg_info.get('error', 'Inconnue')}")
            print()
            
            # Données brutes (optionnel)
            print("📊 DONNÉES BRUTES DISPONIBLES:")
            print(f"   • {len(data['planets'])} planètes")
            print(f"   • {len(data['houses'])} maisons")
            print(f"   • {len(data['interpretations'])} interprétations")
            print("   • Données JSON complètes dans 'raw_data'")
            
            return True
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def exemple_utilisation_programmatique():
    """Exemple d'utilisation programmatique"""
    print("\n" + "=" * 60)
    print("💻 EXEMPLE D'UTILISATION PROGRAMMATIQUE")
    print("=" * 60)
    
    # Données de naissance
    data = {
        "name": "Jean Martin",
        "year": 1985,
        "month": 3,
        "day": 20,
        "hour": 10,
        "minute": 0,
        "city": "Lyon",
        "nation": "FR",
        "theme": "classic",
        "language": "FR"
    }
    
    try:
        response = requests.post("http://localhost:3000/api/natal", json=data, timeout=60)
        result = response.json()
        
        if result['success']:
            data = result['data']
            
            # Extraire les informations importantes
            name = data['basic_info']['name']
            sun_sign = data['planets']['sun']['sign']
            moon_sign = data['planets']['moon']['sign']
            ascendant = data['houses']['first_house']['sign']
            
            print(f"👤 {name}")
            print(f"☀️  Soleil: {sun_sign}")
            print(f"🌙 Lune: {moon_sign}")
            print(f"⬆️  Ascendant: {ascendant}")
            
            # Sauvegarder le SVG si disponible
            if data['svg']['generated']:
                svg_content = base64.b64decode(data['svg']['base64'])
                with open(f"carte_{name.replace(' ', '_')}.svg", 'wb') as f:
                    f.write(svg_content)
                print(f"🎨 Carte SVG sauvegardée!")
            
            return True
        else:
            print(f"❌ Erreur: {result['error']}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🌟 EXEMPLES D'UTILISATION DE L'ENDPOINT NATAL AVEC SVG")
    print("=" * 70)
    print("L'endpoint /api/natal génère maintenant TOUT en une seule requête:")
    print("• Données astrologiques complètes")
    print("• Interprétations personnalisées")
    print("• Carte du ciel en SVG (Base64)")
    print("• Métadonnées et coordonnées")
    print()
    
    # Exemple 1: Utilisation complète
    success1 = exemple_natal_complet()
    
    # Exemple 2: Utilisation programmatique
    success2 = exemple_utilisation_programmatique()
    
    # Résumé
    print("\n" + "=" * 70)
    print("📊 RÉSUMÉ")
    print("=" * 70)
    
    print(f"Exemple complet: {'✅ RÉUSSI' if success1 else '❌ ÉCHOUÉ'}")
    print(f"Exemple programmatique: {'✅ RÉUSSI' if success2 else '❌ ÉCHOUÉ'}")
    
    if success1 and success2:
        print("\n🎉 TOUS LES EXEMPLES SONT RÉUSSIS!")
        print("🌟 L'endpoint natal avec SVG fonctionne parfaitement!")
    else:
        print("\n⚠️  Certains exemples ont échoué.")
    
    print("\n💡 AVANTAGES DE LA NOUVELLE FONCTIONNALITÉ:")
    print("   • Une seule requête pour tout obtenir")
    print("   • Données + SVG en même temps")
    print("   • Plus efficace pour les applications")
    print("   • Économise les appels API")
    print("   • SVG prêt à être affiché ou sauvegardé")

if __name__ == "__main__":
    main()
