#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WWAQ Echtzeit-Glossar-Parser
Version: 5785.1.1
Stand: 1. Tammus 5785
"""

import re
import json
import yaml
import os
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple, Optional

class WWAQGlossarParser:
    """
    Hauptparser für WWAQ-Transformationen
    """
    
    def __init__(self):
        self.base_path = Path(__file__).parent.parent
        self.glossar_path = self.base_path / "glossar"
        self.glossar = self._lade_glossar()
        self.transformationen = self._initialisiere_transformationen()
        self.statistik = {'transformationen': 0, 'begriffe': 0}
        
    def _lade_glossar(self) -> Dict:
        """Lädt Glossar aus Markdown-Datei"""
        glossar = {}
        glossar_file = self.glossar_path / "wwaq-tikun-glossar.md"
        
        if glossar_file.exists():
            with open(glossar_file, 'r', encoding='utf-8') as f:
                inhalt = f.read()
                # Hier würde normalerweise das Glossar geparst werden
                # Für jetzt nur Basis-Struktur
                glossar['geladen'] = True
                glossar['zeitstempel'] = datetime.now().isoformat()
        
        return glossar
    
    def _initialisiere_transformationen(self) -> Dict:
        """Initialisiert alle Transformationsregeln"""
        return {
            'k_zu_q': {
                # Hauptbegriffe
                r'\bWWAK\b': 'WWAQ',
                r'\bKabbala\b': 'Qabbala',
                r'\bKabbalah\b': 'Qabbala',
                r'\bkabbalistisch\b': 'qabbalistisch',
                r'\bKabbalist\b': 'Qabbalist',
                r'\bKabbalisten\b': 'Qabbalisten',
                r'\bKawana\b': 'Qawana',
                r'\bKavanah\b': 'Qawana',
                r'\bKavana\b': 'Qawana',
            },
            'zer_elimination': {
                # Bersten-Gruppe
                r'\bzerbrechen\b': 'bersten',
                r'\bzerbrach\b': 'barst',
                r'\bzerbrachen\b': 'barsten',
                r'\bzerbricht\b': 'berstet',
                r'\bzerbrochen\b': 'geborsten',
                r'\bZerbrechen\b': 'Bersten',
                r'\bZerbruch\b': 'Bersten',
                
                # Wandeln-Gruppe
                r'\bzerstören\b': 'wandeln',
                r'\bzerstört\b': 'gewandelt',
                r'\bzerstörte\b': 'wandelte',
                r'\bzerstörten\b': 'wandelten',
                r'\bzerstörend\b': 'wandelnd',
                r'\bZerstörung\b': 'Wandlung',
                
                # Öffnen-Gruppe
                r'\bzerreißen\b': 'öffnen',
                r'\bzerriss\b': 'öffnete',
                r'\bzerrissen\b': 'geöffnet',
                r'\bzerreißt\b': 'öffnet',
                
                # Sich wandeln-Gruppe
                r'\bzerfallen\b': 'sich wandeln',
                r'\bzerfällt\b': 'wandelt sich',
                r'\bzerfiel\b': 'wandelte sich',
                r'\bzerfielen\b': 'wandelten sich',
                
                # Weitere
                r'\bzerschlagen\b': 'öffnen',
                r'\bzerschlug\b': 'öffnete',
                r'\bzerschlägt\b': 'öffnet',
                r'\bverschwinden\b': 'schwinden',
                r'\bverschwand\b': 'schwand',
                r'\bverschwunden\b': 'geschwunden',
            },
            'din_31636': {
                r'\bTzimtzum\b': 'Zimzum',
                r'\bTzimzum\b': 'Zimzum',
                r'\bDvekut\b': 'Dwekut',
                r'\bDevekut\b': 'Dwekut',
                r'\bTikkun\b': 'Tiqqun',
                r'\bTikun\b': 'Tiqqun',
                r'\bAtzilut\b': 'Azilut',
                r'\bAtziluth\b': 'Azilut',
            }
        }
    
    def transformiere(self, text: str) -> Tuple[str, List[Dict]]:
        """
        Haupttransformationsfunktion
        
        Args:
            text: Zu transformierender Text
            
        Returns:
            Tuple[str, List[Dict]]: (transformierter_text, änderungen)
        """
        if not text:
            return "", []
            
        transformiert = text
        änderungen = []
        
        # Durchlaufe alle Transformationskategorien
        for kategorie, regeln in self.transformationen.items():
            for muster, ersatz in regeln.items():
                # Finde alle Vorkommen
                matches = list(re.finditer(muster, transformiert))
                
                if matches:
                    # Ersetze
                    transformiert = re.sub(muster, ersatz, transformiert)
                    
                    # Dokumentiere Änderungen
                    for match in matches:
                        änderungen.append({
                            'kategorie': kategorie,
                            'original': match.group(),
                            'ersatz': ersatz,
                            'position': match.start(),
                            'kontext': transformiert[max(0, match.start()-20):match.end()+20],
                            'zeitstempel': datetime.now().isoformat()
                        })
        
        # Aktualisiere Statistik
        self.statistik['transformationen'] += 1
        self.statistik['begriffe'] += len(änderungen)
        
        return transformiert, änderungen
    
    def validiere_begriff(self, begriff: str) -> Dict:
        """Validiert einen Begriff gegen das Glossar"""
        validierung = {
            'begriff': begriff,
            'gültig': True,
            'hinweise': [],
            'zeitstempel': datetime.now().isoformat()
        }
        
        # Prüfe auf nicht-konforme Schreibweisen
        if 'Kabbala' in begriff and 'Qabbala' not in begriff:
            validierung['gültig'] = False
            validierung['hinweise'].append('Kabbala sollte als Qabbala geschrieben werden')
            
        if 'Kawana' in begriff and 'Qawana' not in begriff:
            validierung['gültig'] = False
            validierung['hinweise'].append('Kawana sollte als Qawana geschrieben werden')
            
        # Prüfe auf zer-Präfixe
        if re.search(r'\bzer[a-zäöü]+', begriff, re.IGNORECASE):
            validierung['gültig'] = False
            validierung['hinweise'].append('Destruktive zer-Präfixierung gefunden')
            
        return validierung
    
    def exportiere_glossar_json(self):
        """Exportiert Glossar als JSON"""
        json_path = self.glossar_path / "wwaq-tikun-glossar.json"
        
        export_data = {
            'version': '5785.1.1',
            'stand': datetime.now().isoformat(),
            'transformationen': self.transformationen,
            'statistik': self.statistik
        }
        
        with open(json_path, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, ensure_ascii=False, indent=2)
            
        return json_path
    
    def zeige_statistik(self) -> Dict:
        """Zeigt aktuelle Parser-Statistik"""
        return {
            'transformationen_gesamt': self.statistik['transformationen'],
            'begriffe_transformiert': self.statistik['begriffe'],
            'kategorien': list(self.transformationen.keys()),
            'regeln_gesamt': sum(len(regeln) for regeln in self.transformationen.values()),
            'glossar_geladen': self.glossar.get('geladen', False),
            'zeitstempel': datetime.now().isoformat()
        }


# CLI Interface
if __name__ == "__main__":
    import sys
    
    parser = WWAQGlossarParser()
    
    if len(sys.argv) > 1:
        # Text von Kommandozeile
        text = ' '.join(sys.argv[1:])
        transformiert, änderungen = parser.transformiere(text)
        
        print(f"Original: {text}")
        print(f"Transformiert: {transformiert}")
        print(f"Änderungen: {len(änderungen)}")
        
        if änderungen:
            print("\nDetails:")
            for änd in änderungen:
                print(f"  - {änd['original']} → {änd['ersatz']} ({änd['kategorie']})")
    else:
        # Zeige Statistik
        print("WWAQ-Glossar-Parser v5785.1.1")
        print("="*50)
        stats = parser.zeige_statistik()
        for key, value in stats.items():
            print(f"{key}: {value}")
        print("\nVerwendung: python wwaq_parser.py 'Ihr Text hier'")
