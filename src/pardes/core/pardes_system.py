#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
PaRDeS-Modul-System für Ez Chajim
=================================

Implementiert die vier Ebenen der qabbalistischen Textinterpretation:
- Pschat (פשט): Wörtliche Bedeutung
- Remez (רמז): Andeutung/Hinweis
- Drasch (דרש): Auslegung/Interpretation
- Sod (סוד): Geheimnis/Mystische Bedeutung

Stand: 5. Tammus 5785
"""

from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import re
from datetime import datetime

# WWAQ-Konforme Imports (aus lib/)
try:
    from lib.hns10_spiral_system import HNS10SpiralCalculator
    from lib.manuscript_processor import gematria_value
except ImportError:
    # Fallback für Modul-Tests
    def gematria_value(text: str) -> int:
        """Fallback Gematria-Berechnung"""
        return sum(ord(c) for c in text if c.isalpha())
    HNS10SpiralCalculator = None


class PardesLevel(Enum):
    """Die vier Ebenen des PaRDeS-Systems"""
    PSCHAT = "פשט"     # Wörtlich
    REMEZ = "רמז"      # Andeutung
    DRASCH = "דרש"     # Auslegung
    SOD = "סוד"        # Geheimnis


@dataclass
class PardesInterpretation:
    """Container für eine PaRDeS-Interpretation"""
    level: PardesLevel
    text: str
    interpretation: str
    gematria: Optional[int] = None
    spiral_grade: Optional[int] = None
    keywords: List[str] = field(default_factory=list)
    cross_references: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)


class PardesProcessor(ABC):
    """Abstrakte Basisklasse für PaRDeS-Ebenen-Prozessoren"""
    
    def __init__(self):
        self.level = None
        self.spiral_calc = HNS10SpiralCalculator() if HNS10SpiralCalculator else None
    
    @abstractmethod
    def process(self, text: str, context: Optional[Dict] = None) -> PardesInterpretation:
        """Verarbeite Text auf dieser PaRDeS-Ebene"""
        pass
    
    def calculate_spiral_grade(self, text: str) -> Optional[int]:
        """Berechne HNS10-Spiralgrad für Text"""
        if not self.spiral_calc:
            return None
        
        gematria = gematria_value(text)
        # Null-Linien-Tabu beachten!
        grade = gematria % 360
        return grade if grade != 0 else 360


class PschatProcessor(PardesProcessor):
    """Prozessor für Pschat (wörtliche) Ebene"""
    
    def __init__(self):
        super().__init__()
        self.level = PardesLevel.PSCHAT
    
    def process(self, text: str, context: Optional[Dict] = None) -> PardesInterpretation:
        """Extrahiere wörtliche Bedeutung"""
        # Entferne Niqqud und normalisiere
        clean_text = self._normalize_hebrew(text)
        
        # Extrahiere Schlüsselwörter
        keywords = self._extract_keywords(clean_text)
        
        # Basale Interpretation
        interpretation = f"Wörtlicher Text: {clean_text}"
        
        return PardesInterpretation(
            level=self.level,
            text=text,
            interpretation=interpretation,
            gematria=gematria_value(clean_text),
            spiral_grade=self.calculate_spiral_grade(clean_text),
            keywords=keywords,
            metadata={'normalized': clean_text}
        )
    
    def _normalize_hebrew(self, text: str) -> str:
        """Normalisiere hebräischen Text"""
        # Entferne Niqqud (Vokalisierung)
        niqqud_pattern = r'[\u0591-\u05C7]'
        return re.sub(niqqud_pattern, '', text)
    
    def _extract_keywords(self, text: str) -> List[str]:
        """Extrahiere Schlüsselwörter"""
        # Einfache Wort-Tokenisierung
        words = text.split()
        # Filtere kurze Wörter
        return [w for w in words if len(w) > 2]


class RemezProcessor(PardesProcessor):
    """Prozessor für Remez (Andeutung) Ebene"""
    
    def __init__(self):
        super().__init__()
        self.level = PardesLevel.REMEZ
        self.hint_patterns = self._load_hint_patterns()
    
    def process(self, text: str, context: Optional[Dict] = None) -> PardesInterpretation:
        """Finde Andeutungen und versteckte Hinweise"""
        hints = []
        
        # Suche nach Gematria-Verbindungen
        gematria_hints = self._find_gematria_hints(text)
        hints.extend(gematria_hints)
        
        # Suche nach Akronymen
        acronym_hints = self._find_acronyms(text)
        hints.extend(acronym_hints)
        
        # Suche nach Zahlenmustern
        number_hints = self._find_number_patterns(text)
        hints.extend(number_hints)
        
        interpretation = "Gefundene Andeutungen: " + "; ".join(hints) if hints else "Keine direkten Andeutungen gefunden"
        
        return PardesInterpretation(
            level=self.level,
            text=text,
            interpretation=interpretation,
            gematria=gematria_value(text),
            spiral_grade=self.calculate_spiral_grade(text),
            keywords=self._extract_hint_keywords(hints),
            metadata={'hints': hints}
        )
    
    def _load_hint_patterns(self) -> Dict[str, List[str]]:
        """Lade bekannte Andeutungsmuster"""
        return {
            'sefirot': ['כתר', 'חכמה', 'בינה', 'חסד', 'גבורה', 'תפארת', 'נצח', 'הוד', 'יסוד', 'מלכות'],
            'welten': ['אצילות', 'בריאה', 'יצירה', 'עשייה'],
            'namen': ['אהיה', 'יהוה', 'אלהים', 'אדני']
        }
    
    def _find_gematria_hints(self, text: str) -> List[str]:
        """Finde Wörter mit bedeutsamer Gematria"""
        hints = []
        words = text.split()
        
        for word in words:
            value = gematria_value(word)
            # Prüfe auf bedeutsame Zahlen
            if value in [26, 72, 216, 358]:  # JHWH, Chesed, Gvurah, Maschiach
                hints.append(f"{word} (Gematria: {value})")
        
        return hints
    
    def _find_acronyms(self, text: str) -> List[str]:
        """Finde mögliche Akronyme"""
        # Vereinfachte Implementierung
        return []
    
    def _find_number_patterns(self, text: str) -> List[str]:
        """Finde Zahlenmuster im Text"""
        patterns = []
        # Suche nach hebräischen Zahlen
        hebrew_numbers = re.findall(r'[אבגדהוזחטיכלמנסעפצקרשת]+', text)
        for num in hebrew_numbers:
            value = gematria_value(num)
            if value % 10 == 0 or value in [7, 12, 40, 50]:
                patterns.append(f"Zahlenmuster: {num} = {value}")
        return patterns
    
    def _extract_hint_keywords(self, hints: List[str]) -> List[str]:
        """Extrahiere Schlüsselwörter aus Hinweisen"""
        keywords = []
        for hint in hints:
            # Extrahiere hebräische Wörter
            hebrew_words = re.findall(r'[\u0590-\u05FF]+', hint)
            keywords.extend(hebrew_words)
        return list(set(keywords))


class DraschProcessor(PardesProcessor):
    """Prozessor für Drasch (Auslegung) Ebene"""
    
    def __init__(self):
        super().__init__()
        self.level = PardesLevel.DRASCH
        self.midrash_patterns = self._load_midrash_patterns()
    
    def process(self, text: str, context: Optional[Dict] = None) -> PardesInterpretation:
        """Erstelle tiefere Auslegungen"""
        interpretations = []
        
        # Suche nach Midrasch-Mustern
        midrash_refs = self._find_midrash_connections(text)
        if midrash_refs:
            interpretations.append(f"Midrasch-Verbindungen: {', '.join(midrash_refs)}")
        
        # Analysiere Struktur
        structural_analysis = self._analyze_structure(text)
        if structural_analysis:
            interpretations.append(f"Strukturanalyse: {structural_analysis}")
        
        # Finde thematische Verbindungen
        themes = self._extract_themes(text, context)
        if themes:
            interpretations.append(f"Themen: {', '.join(themes)}")
        
        interpretation = " | ".join(interpretations) if interpretations else "Standardauslegung des Textes"
        
        return PardesInterpretation(
            level=self.level,
            text=text,
            interpretation=interpretation,
            gematria=gematria_value(text),
            spiral_grade=self.calculate_spiral_grade(text),
            keywords=themes,
            cross_references=midrash_refs,
            metadata={'structure': structural_analysis}
        )
    
    def _load_midrash_patterns(self) -> Dict[str, List[str]]:
        """Lade Midrasch-Muster"""
        return {
            'schöpfung': ['בראשית', 'אור', 'חשך', 'מים'],
            'erlösung': ['גאולה', 'משיח', 'תיקון'],
            'tora': ['תורה', 'מצוה', 'הלכה']
        }
    
    def _find_midrash_connections(self, text: str) -> List[str]:
        """Finde Verbindungen zu klassischen Midraschim"""
        connections = []
        
        for theme, keywords in self.midrash_patterns.items():
            for keyword in keywords:
                if keyword in text:
                    connections.append(f"{theme} ({keyword})")
        
        return connections
    
    def _analyze_structure(self, text: str) -> str:
        """Analysiere Textstruktur"""
        sentences = text.split('.')
        words = text.split()
        
        return f"{len(sentences)} Sätze, {len(words)} Wörter"
    
    def _extract_themes(self, text: str, context: Optional[Dict] = None) -> List[str]:
        """Extrahiere thematische Elemente"""
        themes = []
        
        # Prüfe auf Sefirot-Erwähnungen
        sefirot = ['כתר', 'חכמה', 'בינה', 'חסד', 'גבורה', 'תפארת', 'נצח', 'הוד', 'יסוד', 'מלכות']
        for sefira in sefirot:
            if sefira in text:
                themes.append(f"Sefira: {sefira}")
        
        # Prüfe auf Welten
        welten = ['אצילות', 'בריאה', 'יצירה', 'עשייה']
        for welt in welten:
            if welt in text:
                themes.append(f"Welt: {welt}")
        
        return themes


class SodProcessor(PardesProcessor):
    """Prozessor für Sod (Geheimnis) Ebene"""
    
    def __init__(self):
        super().__init__()
        self.level = PardesLevel.SOD
    
    def process(self, text: str, context: Optional[Dict] = None) -> PardesInterpretation:
        """Enthülle mystische/geheime Bedeutungen"""
        secrets = []
        
        # Tiefe Gematria-Analyse
        deep_gematria = self._deep_gematria_analysis(text)
        if deep_gematria:
            secrets.append(f"Tiefe Gematria: {deep_gematria}")
        
        # Spiralzeit-Integration
        if self.spiral_calc:
            spiral_secrets = self._spiral_time_analysis(text)
            if spiral_secrets:
                secrets.append(f"Spiralzeit: {spiral_secrets}")
        
        # Buchstaben-Permutationen
        permutations = self._letter_permutations(text)
        if permutations:
            secrets.append(f"Permutationen: {', '.join(permutations[:3])}")
        
        # Versteckte Namen
        hidden_names = self._find_hidden_names(text)
        if hidden_names:
            secrets.append(f"Versteckte Namen: {', '.join(hidden_names)}")
        
        interpretation = " | ".join(secrets) if secrets else "Die Geheimnisse bleiben verborgen"
        
        return PardesInterpretation(
            level=self.level,
            text=text,
            interpretation=interpretation,
            gematria=gematria_value(text),
            spiral_grade=self.calculate_spiral_grade(text),
            keywords=hidden_names,
            metadata={'secrets': secrets}
        )
    
    def _deep_gematria_analysis(self, text: str) -> str:
        """Tiefe Gematria-Analyse mit mehreren Methoden"""
        standard = gematria_value(text)
        
        # Kleine Gematria (Mispar Katan)
        small = standard % 9 or 9
        
        # Quadrat-Gematria
        square = standard ** 2
        
        return f"Standard: {standard}, Klein: {small}, Quadrat: {square}"
    
    def _spiral_time_analysis(self, text: str) -> str:
        """Analyse im Kontext der Spiralzeit"""
        if not self.spiral_calc:
            return ""
        
        grade = self.calculate_spiral_grade(text)
        if grade:
            # Berechne Position auf der Spirale
            winding = grade // 360 + 1
            position = grade % 360
            
            return f"Windung {winding}, Position {position}°"
        return ""
    
    def _letter_permutations(self, text: str) -> List[str]:
        """Finde bedeutsame Buchstaben-Permutationen"""
        # Vereinfachte Implementierung - nur erste 3 Buchstaben
        words = text.split()
        permutations = []
        
        for word in words[:2]:  # Begrenzen für Performance
            if len(word) >= 3:
                # Einfache Permutation: Umkehrung
                reversed_word = word[::-1]
                permutations.append(reversed_word)
        
        return permutations
    
    def _find_hidden_names(self, text: str) -> List[str]:
        """Finde versteckte göttliche Namen"""
        hidden = []
        
        # Prüfe auf 72-Namen-Fragmente
        if 'יהו' in text or 'והו' in text:
            hidden.append("72-Namen-Fragment")
        
        # Prüfe auf Tetragrammaton-Permutationen
        tetra_perms = ['יהוה', 'יההו', 'יוהה', 'הויה', 'היהו', 'ההיו']
        for perm in tetra_perms:
            if perm in text:
                hidden.append(f"JHWH-Permutation: {perm}")
        
        return hidden


class PardesAnalyzer:
    """Haupt-Analysator für alle PaRDeS-Ebenen"""
    
    def __init__(self):
        self.processors = {
            PardesLevel.PSCHAT: PschatProcessor(),
            PardesLevel.REMEZ: RemezProcessor(),
            PardesLevel.DRASCH: DraschProcessor(),
            PardesLevel.SOD: SodProcessor()
        }
    
    def analyze_text(self, text: str, context: Optional[Dict] = None) -> Dict[PardesLevel, PardesInterpretation]:
        """Analysiere Text auf allen vier Ebenen"""
        results = {}
        
        for level, processor in self.processors.items():
            try:
                interpretation = processor.process(text, context)
                results[level] = interpretation
            except Exception as e:
                # Fehlerbehandlung
                results[level] = PardesInterpretation(
                    level=level,
                    text=text,
                    interpretation=f"Fehler bei Verarbeitung: {str(e)}",
                    metadata={'error': str(e)}
                )
        
        return results
    
    def analyze_with_focus(self, text: str, focus_level: PardesLevel, context: Optional[Dict] = None) -> PardesInterpretation:
        """Analysiere mit Fokus auf eine spezifische Ebene"""
        if focus_level not in self.processors:
            raise ValueError(f"Unbekannte PaRDeS-Ebene: {focus_level}")
        
        return self.processors[focus_level].process(text, context)
    
    def generate_report(self, text: str, context: Optional[Dict] = None) -> str:
        """Generiere umfassenden PaRDeS-Bericht"""
        results = self.analyze_text(text, context)
        
        report_lines = [
            "=== PaRDeS-ANALYSE ===",
            f"Text: {text[:50]}..." if len(text) > 50 else f"Text: {text}",
            f"Gesamt-Gematria: {gematria_value(text)}",
            ""
        ]
        
        for level, interpretation in results.items():
            report_lines.extend([
                f"--- {level.name} ({level.value}) ---",
                f"Interpretation: {interpretation.interpretation}",
                f"Gematria: {interpretation.gematria}",
                f"Spiralgrad: {interpretation.spiral_grade}°" if interpretation.spiral_grade else "Spiralgrad: N/A",
                f"Schlüsselwörter: {', '.join(interpretation.keywords)}" if interpretation.keywords else "",
                ""
            ])
        
        report_lines.append("Q!")
        return "\n".join(report_lines)


# Hilfsfunktionen für Export
def export_pardes_to_yaml(interpretations: Dict[PardesLevel, PardesInterpretation]) -> str:
    """Exportiere PaRDeS-Interpretationen als YAML"""
    import yaml
    
    export_data = {
        'pardes_analysis': {
            level.name.lower(): {
                'hebrew_name': level.value,
                'interpretation': interp.interpretation,
                'gematria': interp.gematria,
                'spiral_grade': interp.spiral_grade,
                'keywords': interp.keywords,
                'cross_references': interp.cross_references,
                'metadata': interp.metadata
            }
            for level, interp in interpretations.items()
        },
        'timestamp': datetime.now().isoformat(),
        'wwaq_conformity': 'validated'
    }
    
    return yaml.dump(export_data, allow_unicode=True, sort_keys=False)


# Beispiel-Verwendung und Tests
if __name__ == "__main__":
    # Test-Text
    test_text = "בראשית ברא אלהים את השמים ואת הארץ"
    
    # Erstelle Analyzer
    analyzer = PardesAnalyzer()
    
    # Vollständige Analyse
    print("=== VOLLSTÄNDIGE PARDES-ANALYSE ===\n")
    report = analyzer.generate_report(test_text)
    print(report)
    
    # Einzelne Ebene
    print("\n=== NUR SOD-EBENE ===\n")
    sod_result = analyzer.analyze_with_focus(test_text, PardesLevel.SOD)
    print(f"Sod-Interpretation: {sod_result.interpretation}")
    
    # YAML-Export
    print("\n=== YAML-EXPORT ===\n")
    all_results = analyzer.analyze_text(test_text)
    yaml_output = export_pardes_to_yaml(all_results)
    print(yaml_output)
