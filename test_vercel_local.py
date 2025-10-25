#!/usr/bin/env python3
"""
Test de l'API préparée pour Vercel en local
"""

import requests
import json
import base64

def test_vercel_api():
    """Test de l'API configurée pour Vercel"""
    print("🚀 TEST DE L'API PRÉPARÉE POUR VERCEL")
    print("=" * 60)
    
    # URL de l'API (local ou Vercel)
    API_URL = "http://localhost:3000"
    
    # Test 1: Page d'accueil
    print("\n1. 🏠 Test de la page d'accueil...")
    try:
        response = requests.get(f"{API_URL}/", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Page d'accueil accessible")
            print(f"   Message: {result['message']}")
            print(f"   Version: {result['version']}")
            print(f"   Statut: {result['status']}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur de connexion: {e}")
        return False
    
    # Test 2: Documentation
    print("\n2. 📖 Test de la documentation...")
    try:
        response = requests.get(f"{API_URL}/docs", timeout=10)
        if response.status_code == 200:
            result = response.json()
            print("✅ Documentation accessible")
            print(f"   Titre: {result['title']}")
            print(f"   Version: {result['version']}")
            print(f"   Statut: {result['status']}")
        else:
            print(f"❌ Erreur: {response.status_code}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
    
    # Test 3: Endpoint natal avec SVG
    print("\n3. 🪐 Test de l'endpoint natal avec SVG...")
    data = {
        "name": "Sophie Vercel",
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
        response = requests.post(f"{API_URL}/api/natal", json=data, timeout=60)
        if response.status_code == 200:
            result = response.json()
            print("✅ Thème natal généré avec succès!")
            print(f"   Nom: {result['data']['basic_info']['name']}")
            print(f"   Date: {result['data']['basic_info']['birth_date']}")
            print(f"   Soleil: {result['data']['planets']['sun']['sign']}")
            print(f"   Lune: {result['data']['planets']['moon']['sign']}")
            print(f"   Ascendant: {result['data']['houses']['first_house']['sign']}")
            
            # Vérifier le SVG
            if 'svg' in result['data']:
                svg_info = result['data']['svg']
                print(f"   🎨 SVG généré: {svg_info['generated']}")
                if svg_info['generated']:
                    print(f"   📁 Fichier: {svg_info['filename']}")
                    print(f"   📊 Taille: {len(svg_info['base64'])} caractères")
                    
                    # Sauvegarder le SVG
                    svg_content = base64.b64decode(svg_info['base64'])
                    filename = f"vercel_test_{svg_info['filename']}"
                    
                    with open(filename, 'wb') as f:
                        f.write(svg_content)
                    
                    print(f"   💾 SVG sauvegardé: {filename}")
                else:
                    print(f"   ❌ Erreur SVG: {svg_info.get('error', 'Inconnue')}")
            
            return True
        else:
            print(f"❌ Erreur {response.status_code}: {response.text}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_performance():
    """Test de performance pour Vercel"""
    print("\n4. ⚡ Test de performance...")
    
    data = {
        "name": "Performance Test",
        "year": 1990,
        "month": 6,
        "day": 15,
        "hour": 14,
        "minute": 30,
        "city": "Paris",
        "nation": "FR"
    }
    
    import time
    
    try:
        start_time = time.time()
        response = requests.post("http://localhost:3000/api/natal", json=data, timeout=60)
        end_time = time.time()
        
        duration = end_time - start_time
        
        if response.status_code == 200:
            print(f"✅ Requête réussie en {duration:.2f} secondes")
            
            if duration < 10:
                print("   🚀 Performance excellente (< 10s)")
            elif duration < 20:
                print("   ⚡ Performance bonne (< 20s)")
            elif duration < 30:
                print("   ⚠️  Performance acceptable (< 30s)")
            else:
                print("   ❌ Performance lente (> 30s)")
            
            return True
        else:
            print(f"❌ Erreur {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erreur: {e}")
        return False

def test_vercel_compatibility():
    """Test de compatibilité Vercel"""
    print("\n5. 🌐 Test de compatibilité Vercel...")
    
    # Vérifier les variables d'environnement
    import os
    
    print("   Variables d'environnement:")
    print(f"   PORT: {os.environ.get('PORT', 'Non défini')}")
    print(f"   FLASK_ENV: {os.environ.get('FLASK_ENV', 'Non défini')}")
    print(f"   PYTHON_VERSION: {os.environ.get('PYTHON_VERSION', 'Non défini')}")
    
    # Vérifier les fichiers de configuration
    import os
    
    config_files = [
        'vercel.json',
        'requirements.txt',
        '.vercelignore',
        'api/index.py'
    ]
    
    print("\n   Fichiers de configuration:")
    for file in config_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} manquant")
    
    return True

def main():
    """Fonction principale"""
    print("🌟 TEST DE L'API PRÉPARÉE POUR VERCEL")
    print("=" * 70)
    print("Vérification de la compatibilité et des performances...")
    print()
    
    # Tests
    tests = [
        ("API de base", test_vercel_api),
        ("Performance", test_performance),
        ("Compatibilité Vercel", test_vercel_compatibility)
    ]
    
    results = []
    for test_name, test_func in tests:
        print(f"\n{'='*20} {test_name.upper()} {'='*20}")
        success = test_func()
        results.append((test_name, success))
    
    # Résumé
    print("\n" + "="*70)
    print("📊 RÉSUMÉ DES TESTS")
    print("="*70)
    
    for test_name, success in results:
        status = "✅ RÉUSSI" if success else "❌ ÉCHOUÉ"
        print(f"{test_name}: {status}")
    
    successful = sum(1 for _, success in results if success)
    total = len(results)
    
    print(f"\n🎯 Score: {successful}/{total} tests réussis")
    
    if successful == total:
        print("\n🎉 TOUS LES TESTS SONT RÉUSSIS!")
        print("🌟 L'API est prête pour le déploiement sur Vercel!")
        print("\n📋 PROCHAINES ÉTAPES:")
        print("   1. git add .")
        print("   2. git commit -m 'Prêt pour Vercel'")
        print("   3. vercel deploy")
        print("   4. Profiter de votre API globale! 🌍")
    else:
        print("\n⚠️  Certains tests ont échoué.")
        print("   Vérifiez les erreurs avant le déploiement.")
    
    print("\n💡 AVANTAGES VERCEL:")
    print("   • CDN global pour performance mondiale")
    print("   • HTTPS automatique")
    print("   • Déploiements instantanés")
    print("   • Monitoring intégré")
    print("   • Scaling automatique")

if __name__ == "__main__":
    main()
