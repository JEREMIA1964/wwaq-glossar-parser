#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WWAQ Parser REST API
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
from datetime import datetime
from wwaq_parser import WWAQGlossarParser

app = Flask(__name__)
CORS(app)
parser = WWAQGlossarParser()

@app.route('/')
def index():
    """API Info"""
    return jsonify({
        'name': 'WWAQ-Glossar-Parser API',
        'version': '5785.1.1',
        'endpoints': {
            'POST /transform': 'Text transformieren',
            'POST /validate': 'Begriff validieren',
            'GET /stats': 'Statistik anzeigen'
        }
    })

@app.route('/transform', methods=['POST'])
def transform():
    """Transformiert Text"""
    data = request.json
    text = data.get('text', '')
    
    transformiert, änderungen = parser.transformiere(text)
    
    return jsonify({
        'original': text,
        'transformiert': transformiert,
        'änderungen': änderungen,
        'anzahl_änderungen': len(änderungen),
        'zeitstempel': datetime.now().isoformat()
    })

@app.route('/validate', methods=['POST'])
def validate():
    """Validiert Begriff"""
    data = request.json
    begriff = data.get('begriff', '')
    
    validierung = parser.validiere_begriff(begriff)
    
    return jsonify(validierung)

@app.route('/stats', methods=['GET'])
def stats():
    """Zeigt Statistik"""
    return jsonify(parser.zeige_statistik())

if __name__ == '__main__':
    print("WWAQ Parser API startet auf Port 5785...")
    app.run(host='0.0.0.0', port=5785, debug=True)
