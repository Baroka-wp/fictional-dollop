#!/usr/bin/env python3
"""
API Astrologique Kerykeion pour Vercel
Point d'entrée principal pour le déploiement sur Vercel
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import os
import tempfile
from datetime import datetime
from typing import Dict, Any, Optional
import base64
from io import BytesIO

from kerykeion import (
    AstrologicalSubject, 
    KerykeionChartSVG, 
    Report,
    SynastryAspects,
    CompositeSubjectFactory
)

# Configuration Flask pour Vercel
app = Flask(__name__)
CORS(app)

# Configuration
app.config['JSON_AS_ASCII'] = False
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max

# Cache pour optimiser les performances
cache = {}

def get_cache_key(data: Dict[str, Any]) -> str:
    """Génère une clé de cache basée sur les données"""
    return f"{data.get('name', '')}_{data.get('year', '')}_{data.get('month', '')}_{data.get('day', '')}_{data.get('hour', '')}_{data.get('minute', '')}_{data.get('city', '')}_{data.get('nation', '')}"

def create_astrological_subject(data: Dict[str, Any]) -> AstrologicalSubject:
    """Crée un sujet astrologique à partir des données"""
    return AstrologicalSubject(
        name=data['name'],
        year=data['year'],
        month=data['month'],
        day=data['day'],
        hour=data['hour'],
        minute=data['minute'],
        city=data.get('city', 'Paris'),
        nation=data.get('nation', 'FR'),
        lng=data.get('lng'),
        lat=data.get('lat'),
        tz_str=data.get('tz_str'),
        zodiac_type=data.get('zodiac_type', 'Tropic'),
        sidereal_mode=data.get('sidereal_mode') if data.get('zodiac_type') == 'Sidereal' else None,
        houses_system_identifier=data.get('houses_system', 'P'),
        perspective_type=data.get('perspective_type', 'Apparent Geocentric'),
        online=data.get('online', True),
        geonames_username=data.get('geonames_username')
    )

def get_planet_interpretation(planet_data: Dict[str, Any], planet_name: str) -> Dict[str, Any]:
    """Génère une interprétation basique pour une planète"""
    sign = planet_data['sign']
    position = planet_data['position']
    house = planet_data.get('house', 'Unknown')
    
    # Dictionnaire des signes en français
    signs_fr = {
        'Ari': 'Bélier', 'Tau': 'Taureau', 'Gem': 'Gémeaux', 'Can': 'Cancer',
        'Leo': 'Lion', 'Vir': 'Vierge', 'Lib': 'Balance', 'Sco': 'Scorpion',
        'Sag': 'Sagittaire', 'Cap': 'Capricorne', 'Aqu': 'Verseau', 'Pis': 'Poissons'
    }
    
    # Dictionnaire des maisons en français
    houses_fr = {
        'First_House': 'Maison 1 (Ascendant)', 'Second_House': 'Maison 2', 'Third_House': 'Maison 3',
        'Fourth_House': 'Maison 4', 'Fifth_House': 'Maison 5', 'Sixth_House': 'Maison 6',
        'Seventh_House': 'Maison 7 (Descendant)', 'Eighth_House': 'Maison 8', 'Ninth_House': 'Maison 9',
        'Tenth_House': 'Maison 10 (MC)', 'Eleventh_House': 'Maison 11', 'Twelfth_House': 'Maison 12'
    }
    
    # Dictionnaire des planètes en français
    planets_fr = {
        'Sun': 'Soleil', 'Moon': 'Lune', 'Mercury': 'Mercure', 'Venus': 'Vénus',
        'Mars': 'Mars', 'Jupiter': 'Jupiter', 'Saturn': 'Saturne', 'Uranus': 'Uranus',
        'Neptune': 'Neptune', 'Pluto': 'Pluton', 'Mean_Node': 'Nœud Nord', 'True_Node': 'Nœud Nord Vrai',
        'Chiron': 'Chiron', 'Mean_Lilith': 'Lilith'
    }
    
    return {
        'planet_name': planets_fr.get(planet_name, planet_name),
        'sign': signs_fr.get(sign, sign),
        'position': round(position, 2),
        'house': houses_fr.get(house, house),
        'element': planet_data.get('element', ''),
        'quality': planet_data.get('quality', ''),
        'retrograde': planet_data.get('retrograde', False),
        'interpretation': f"Le {planets_fr.get(planet_name, planet_name)} en {signs_fr.get(sign, sign)} à {position:.2f}° dans la {houses_fr.get(house, house)}"
    }

@app.route('/', methods=['GET'])
def home():
    """Page d'accueil de l'API"""
    return jsonify({
        'message': 'API Astrologique Kerykeion - Déployée sur Vercel',
        'version': '1.0.0',
        'status': 'online',
        'endpoints': {
            'natal': '/api/natal - Génère un thème natal complet avec SVG',
            'synastry': '/api/synastry - Analyse de compatibilité entre deux personnes',
            'transit': '/api/transit - Carte de transit',
            'composite': '/api/composite - Carte composite',
            'chart_svg': '/api/chart-svg - Génère une carte SVG',
            'interpretations': '/api/interpretations - Interprétations astrologiques'
        },
        'documentation': '/docs'
    })

@app.route('/api/natal', methods=['POST'])
def generate_natal_chart():
    """Génère un thème natal complet avec interprétations et SVG"""
    try:
        data = request.get_json()
        
        if not data:
            return jsonify({'error': 'Données JSON requises'}), 400
        
        # Vérifier les champs requis
        required_fields = ['name', 'year', 'month', 'day', 'hour', 'minute']
        for field in required_fields:
            if field not in data:
                return jsonify({'error': f'Champ requis manquant: {field}'}), 400
        
        # Créer le sujet astrologique
        subject = create_astrological_subject(data)
        
        # Générer le rapport
        report = Report(subject)
        
        # Collecter toutes les données
        result = {
            'basic_info': {
                'name': subject.name,
                'birth_date': f"{subject.day}/{subject.month}/{subject.year}",
                'birth_time': f"{subject.hour}:{subject.minute:02d}",
                'location': f"{subject.city}, {subject.nation}",
                'coordinates': {
                    'longitude': subject.lng,
                    'latitude': subject.lat
                }
            },
            'planets': {},
            'houses': {},
            'aspects': [],
            'interpretations': {},
            'raw_data': json.loads(subject.json(dump=True))
        }
        
        # Collecter les données des planètes
        planets = ['sun', 'moon', 'mercury', 'venus', 'mars', 'jupiter', 'saturn', 
                  'uranus', 'neptune', 'pluto', 'mean_node', 'true_node', 'chiron', 'mean_lilith']
        
        for planet in planets:
            if hasattr(subject, planet):
                planet_data = getattr(subject, planet)
                if isinstance(planet_data, dict):
                    result['planets'][planet] = get_planet_interpretation(planet_data, planet)
                else:
                    # Si ce n'est pas un dict, essayer d'accéder aux attributs
                    try:
                        planet_dict = {
                            'sign': getattr(planet_data, 'sign', ''),
                            'position': getattr(planet_data, 'position', 0),
                            'element': getattr(planet_data, 'element', ''),
                            'quality': getattr(planet_data, 'quality', ''),
                            'house': getattr(planet_data, 'house', ''),
                            'retrograde': getattr(planet_data, 'retrograde', False)
                        }
                        result['planets'][planet] = get_planet_interpretation(planet_dict, planet)
                    except:
                        result['planets'][planet] = {'error': f'Impossible de lire les données de {planet}'}
        
        # Collecter les données des maisons
        houses = ['first_house', 'second_house', 'third_house', 'fourth_house', 
                 'fifth_house', 'sixth_house', 'seventh_house', 'eighth_house',
                 'ninth_house', 'tenth_house', 'eleventh_house', 'twelfth_house']
        
        for house in houses:
            if hasattr(subject, house):
                house_data = getattr(subject, house)
                result['houses'][house] = {
                    'sign': house_data.get('sign', ''),
                    'position': house_data.get('position', 0),
                    'element': house_data.get('element', ''),
                    'quality': house_data.get('quality', '')
                }
        
        # Générer des interprétations basiques
        result['interpretations'] = {
            'sun_sign': f"Signe solaire: {result['planets']['sun']['sign']}",
            'moon_sign': f"Signe lunaire: {result['planets']['moon']['sign']}",
            'ascendant': f"Ascendant: {result['houses']['first_house']['sign']}",
            'dominant_element': "Analyse des éléments dominants...",
            'personality_summary': f"Personnalité marquée par le {result['planets']['sun']['sign']} avec une lune en {result['planets']['moon']['sign']}"
        }
        
        # Générer la carte SVG
        try:
            chart = KerykeionChartSVG(
                subject,
                chart_type="Natal",
                theme=data.get('theme', 'classic'),
                chart_language=data.get('language', 'FR'),
                new_output_directory=tempfile.gettempdir()
            )
            chart.makeSVG()
            
            # Lire le fichier SVG généré
            svg_filename = f"{subject.name} - Natal Chart.svg"
            svg_path = os.path.join(tempfile.gettempdir(), svg_filename)
            
            if os.path.exists(svg_path):
                with open(svg_path, 'r', encoding='utf-8') as f:
                    svg_content = f.read()
                
                # Encoder en base64 pour l'envoi
                svg_base64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
                
                result['svg'] = {
                    'base64': svg_base64,
                    'filename': svg_filename,
                    'generated': True
                }
            else:
                result['svg'] = {
                    'base64': None,
                    'filename': None,
                    'generated': False,
                    'error': 'Erreur lors de la génération du SVG'
                }
        except Exception as e:
            result['svg'] = {
                'base64': None,
                'filename': None,
                'generated': False,
                'error': f'Erreur lors de la génération du SVG: {str(e)}'
            }
        
        return jsonify({
            'success': True,
            'data': result,
            'timestamp': datetime.now().isoformat()
        })
        
    except Exception as e:
        return jsonify({
            'success': False,
            'error': str(e),
            'timestamp': datetime.now().isoformat()
        }), 500

@app.route('/docs', methods=['GET'])
def documentation():
    """Documentation de l'API"""
    return jsonify({
        'title': 'API Astrologique Kerykeion - Vercel',
        'version': '1.0.0',
        'description': 'API REST pour générer des cartes du ciel et analyses astrologiques - Déployée sur Vercel',
        'status': 'online',
        'endpoints': {
            'POST /api/natal': {
                'description': 'Génère un thème natal complet avec SVG',
                'parameters': {
                    'name': 'string (requis)',
                    'year': 'int (requis)',
                    'month': 'int (requis)',
                    'day': 'int (requis)',
                    'hour': 'int (requis)',
                    'minute': 'int (requis)',
                    'city': 'string (optionnel)',
                    'nation': 'string (optionnel)',
                    'theme': 'string (classic, dark, light)',
                    'language': 'string (FR, EN, ES, IT, DE)'
                }
            }
        },
        'examples': {
            'natal_request': {
                'name': 'Jean Dupont',
                'year': 1990,
                'month': 6,
                'day': 15,
                'hour': 14,
                'minute': 30,
                'city': 'Paris',
                'nation': 'FR',
                'theme': 'dark',
                'language': 'FR'
            }
        }
    })

# Export pour Vercel

if __name__ == '__main__':
    import os
    port = int(os.environ.get('PORT', 3000))
    debug = os.environ.get('FLASK_ENV') == 'development'
    
    print("🌟 Démarrage de l'API Astrologique Kerykeion sur Vercel...")
    print(f"📡 API disponible sur: http://localhost:{port}")
    print(f"📖 Documentation: http://localhost:{port}/docs")
    print(f"🏠 Accueil: http://localhost:{port}/")
    print(f"🌍 Mode: {'Développement' if debug else 'Production'}")
    
    app.run(debug=debug, host='0.0.0.0', port=port)
