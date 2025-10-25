#!/usr/bin/env python3
"""
Test de l'endpoint natal avec génération SVG intégrée
"""

import requests
import json
import base64

def test_natal_avec_svg():
    """Test de l'endpoint natal avec SVG"""
    print("🪐 Test de l'endpoint natal avec SVG intégré...")
    
    data = {
        "name": "Sophie Martin",
        "year": 1992,
        "month": 8,
        "day": 15,
        "hour": 14,
        "minute": 30,
        "city": "Paris",
        "nation": "FR",
        "theme": "dark",
        "language": "FR"
    }
    
    try:
        response = requests.post("http://localhost:3000/api/natal", json=data, timeout=60)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            data = result['data']
            
            print("✅ Thème natal généré avec succès!")
            print(f"   Nom: {data['basic_info']['name']}")
            print(f"   Date: {data['basic_info']['birth_date']}")
            print(f"   Soleil: {data['planets']['sun']['sign']}")
            print(f"   Lune: {data['planets']['moon']['sign']}")
            print(f"   Ascendant: {data['houses']['first_house']['sign']}")
            print()
            
            # Vérifier le SVG
            if 'svg' in data:
                svg_info = data['svg']
                print("🎨 Informations SVG:")
                print(f"   Généré: {svg_info['generated']}")
                print(f"   Fichier: {svg_info['filename']}")
                
                if svg_info['generated'] and svg_info['base64']:
                    print(f"   Taille SVG: {len(svg_info['base64'])} caractères")
                    
                    # Sauvegarder le SVG
                    svg_content = base64.b64decode(svg_info['base64'])
                    filename = f"test_{svg_info['filename']}"
                    
                    with open(filename, 'wb') as f:
                        f.write(svg_content)
                    
                    print(f"   💾 SVG sauvegardé: {filename}")
                else:
                    print(f"   ❌ Erreur SVG: {svg_info.get('error', 'Inconnue')}")
            else:
                print("❌ Pas d'informations SVG dans la réponse")
            
            print()
            print("🔮 Interprétations:")
            for key, interpretation in data['interpretations'].items():
                print(f"   • {interpretation}")
            
            return True
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_natal_simple():
    """Test de l'endpoint natal simple (sans options SVG)"""
    print("\n🪐 Test de l'endpoint natal simple...")
    
    data = {
        "name": "Pierre Dubois",
        "year": 1988,
        "month": 5,
        "day": 20,
        "hour": 10,
        "minute": 0,
        "city": "Lyon",
        "nation": "FR"
    }
    
    try:
        response = requests.post("http://localhost:3000/api/natal", json=data, timeout=60)
        print(f"Status: {response.status_code}")
        
        if response.status_code == 200:
            result = response.json()
            data = result['data']
            
            print("✅ Thème natal généré avec succès!")
            print(f"   Nom: {data['basic_info']['name']}")
            print(f"   Soleil: {data['planets']['sun']['sign']}")
            
            # Vérifier le SVG
            if 'svg' in data and data['svg']['generated']:
                print(f"   🎨 SVG généré: {data['svg']['filename']}")
            else:
                print("   ❌ SVG non généré")
            
            return True
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return False
            
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def main():
    """Fonction principale"""
    print("🌟 TEST DE L'ENDPOINT NATAL AVEC SVG INTÉGRÉ")
    print("=" * 60)
    
    # Test 1: Natal avec options SVG
    print("\n1. Test avec options SVG (thème dark, français):")
    success1 = test_natal_avec_svg()
    
    # Test 2: Natal simple
    print("\n2. Test simple (sans options SVG):")
    success2 = test_natal_simple()
    
    # Résumé
    print("\n" + "=" * 60)
    print("📊 RÉSUMÉ DES TESTS")
    print("=" * 60)
    
    print(f"Test avec options SVG: {'✅ RÉUSSI' if success1 else '❌ ÉCHOUÉ'}")
    print(f"Test simple: {'✅ RÉUSSI' if success2 else '❌ ÉCHOUÉ'}")
    
    if success1 and success2:
        print("\n🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("🌟 L'endpoint natal avec SVG fonctionne parfaitement!")
    else:
        print("\n⚠️  Certains tests ont échoué.")
    
    print("\n💡 L'endpoint /api/natal génère maintenant:")
    print("   • Toutes les données astrologiques")
    print("   • Les interprétations")
    print("   • La carte SVG en Base64")
    print("   • Tout en une seule requête!")

if __name__ == "__main__":
    main()
