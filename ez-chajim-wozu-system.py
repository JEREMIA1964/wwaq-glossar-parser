#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Ez Chajim Wozu-Zentriertes Echtzeit-Kommunikationssystem
========================================================

Implementiert Azilut-verankerte Modul-Kommunikation mit
Wozu-Priorisierung zur spirituellen Klarheit.

Stand: 10. Tammus 5785
WWAQ-konform gemäß TIKUN-GLOSSAR Version 5785.22.3
"""

from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
import asyncio
import yaml
from datetime import datetime
import json

# WWAQ-konforme Imports
from src.pardes.core.pardes_system import PardesAnalyzer, PardesLevel
from src.azilut_konverter import AzilutKonverter, Olam
from src.hns10_spiral_system import HNS10SpiralTime
from src.glossar_manager import GlossarManager  # WICHTIG: Für Sprachvalidierung


class FrageTyp(Enum):
    """Hierarchie der Fragewörter nach spiritueller Ebene"""
    WOZU = "למה"     # Azilut - Zweck/Absicht
    WARUM = "מדוע"   # Berija - Ursache
    WIE = "איך"      # Jezira - Methode
    WAS = "מה"       # Asija - Inhalt
    WER = "מי"       # Seelen-Ebene
    WO = "איפה"      # Raum-Ebene
    WANN = "מתי"     # Zeit-Ebene


@dataclass
class WozuValidierung:
    """Container für Wozu-Validierungs-Ergebnis"""
    ist_verankert: bool
    azilut_score: float  # 0.0 - 1.0
    fehlende_wozu_aspekte: List[str]
    empfohlene_korrekturen: List[str]
    weltebene: Olam


@dataclass
class EchtzeitNachricht:
    """WWAQ-konforme Echtzeit-Nachricht zwischen Modulen"""
    inhalt: str
    wozu: str  # Pflichtfeld!
    sender_modul: str
    empfänger_modul: str
    frage_hierarchie: Dict[FrageTyp, str]
    pardes_ebene: Optional[PardesLevel] = None
    spiral_zeit: Optional[Dict] = None
    validierung: Optional[WozuValidierung] = None
    zeitstempel: str = field(default_factory=lambda: datetime.now().isoformat())


class WozuValidator:
    """Validiert Wozu-Zentrierung und Azilut-Verankerung"""
    
    WOZU_INDIKATOREN = [
        "um zu", "damit", "zwecks", "zur", "für die",
        "למען", "כדי", "לשם", "בשביל"
    ]
    
    AZILUT_MARKER = [
        "אין סוף", "unendliches Licht", "Emanation",
        "höchste Absicht", "göttlicher Zweck", "Tiqqun"
    ]
    
    def validiere_wozu_zentrierung(self, nachricht: EchtzeitNachricht) -> WozuValidierung:
        """Prüft ob Nachricht wozu-zentriert und Azilut-verankert ist"""
        
        # Basis-Prüfung: Ist Wozu definiert?
        if not nachricht.wozu:
            return WozuValidierung(
                ist_verankert=False,
                azilut_score=0.0,
                fehlende_wozu_aspekte=["Kein Wozu definiert!"],
                empfohlene_korrekturen=["Definiere klaren Zweck/Absicht"],
                weltebene=Olam.ASIJA
            )
        
        # Tiefere Analyse
        azilut_score = self._berechne_azilut_score(nachricht)
        weltebene = self._erkenne_weltebene(nachricht)
        fehlende_aspekte = self._finde_fehlende_aspekte(nachricht)
        
        return WozuValidierung(
            ist_verankert=azilut_score > 0.7,
            azilut_score=azilut_score,
            fehlende_wozu_aspekte=fehlende_aspekte,
            empfohlene_korrekturen=self._generiere_korrekturen(fehlende_aspekte),
            weltebene=weltebene
        )
    
    def _berechne_azilut_score(self, nachricht: EchtzeitNachricht) -> float:
        """Berechnet Azilut-Verankerungs-Score"""
        score = 0.0
        
        # Wozu vorhanden: Basis-Score
        if nachricht.wozu:
            score += 0.3
        
        # Wozu-Indikatoren im Text
        wozu_count = sum(1 for ind in self.WOZU_INDIKATOREN 
                        if ind in nachricht.wozu.lower())
        score += min(wozu_count * 0.1, 0.2)
        
        # Azilut-Marker
        azilut_count = sum(1 for marker in self.AZILUT_MARKER
                          if marker in nachricht.inhalt or marker in nachricht.wozu)
        score += min(azilut_count * 0.15, 0.3)
        
        # Frage-Hierarchie korrekt?
        if FrageTyp.WOZU in nachricht.frage_hierarchie:
            score += 0.2
        
        return min(score, 1.0)
    
    def _erkenne_weltebene(self, nachricht: EchtzeitNachricht) -> Olam:
        """Erkennt aktuelle Weltebene der Nachricht"""
        konverter = AzilutKonverter()
        return konverter.erkenne_weltebene(nachricht.inhalt)
    
    def _finde_fehlende_aspekte(self, nachricht: EchtzeitNachricht) -> List[str]:
        """Identifiziert fehlende Wozu-Aspekte"""
        fehlend = []
        
        if FrageTyp.WOZU not in nachricht.frage_hierarchie:
            fehlend.append("Wozu-Frage nicht in Hierarchie")
        
        if not any(ind in nachricht.wozu.lower() for ind in self.WOZU_INDIKATOREN):
            fehlend.append("Keine klaren Zweck-Indikatoren")
        
        if nachricht.weltebene == Olam.ASIJA:
            fehlend.append("Zu stark in Asija (Handlung) verhaftet")
        
        return fehlend
    
    def _generiere_korrekturen(self, fehlende: List[str]) -> List[str]:
        """Generiert Korrektur-Empfehlungen"""
        korrekturen = []
        
        for fehler in fehlende:
            if "Wozu-Frage" in fehler:
                korrekturen.append("Füge primäre Wozu-Frage hinzu: 'Wozu dient diese Kommunikation?'")
            elif "Zweck-Indikatoren" in fehler:
                korrekturen.append("Verwende klare Zweck-Formulierungen: 'um zu...', 'damit...'")
            elif "Asija" in fehler:
                korrekturen.append("Erhebe Perspektive: Von WAS (Asija) zu WOZU (Azilut)")
        
        # WWAQ-konforme Formulierungen sicherstellen
        korrekturen.append("Verwende WWAQ-konforme Sprache: wandeln statt wandeln, bersten statt bersten")
        
        return korrekturen


class EchtzeitKommunikator:
    """Haupt-Klasse für Wozu-zentrierte Modul-Kommunikation"""
    
    def __init__(self):
        self.validator = WozuValidator()
        self.pardes = PardesAnalyzer()
        self.azilut_konverter = AzilutKonverter()
        self.spiral_zeit = HNS10SpiralTime()
        self.glossar_manager = GlossarManager()  # WWAQ-Glossar Integration
        self.nachrichten_queue: asyncio.Queue = asyncio.Queue()
        self.module_registry: Dict[str, Any] = {}
    
    async def sende_nachricht(self, nachricht: EchtzeitNachricht) -> bool:
        """Sendet Nachricht mit Wozu-Validierung"""
        
        # 0. WWAQ-Konformität sicherstellen
        nachricht.inhalt = self.glossar_manager.transform(nachricht.inhalt)
        nachricht.wozu = self.glossar_manager.transform(nachricht.wozu)
        
        # 1. Validiere Wozu-Zentrierung
        validierung = self.validator.validiere_wozu_zentrierung(nachricht)
        nachricht.validierung = validierung
        
        # Blockiere nicht-verankerte Nachrichten (nicht als Strafe, sondern als Schutz)
        if not validierung.ist_verankert:
            print(f"⚠️ WARNUNG: Nachricht nicht Azilut-verankert!")
            print(f"   Azilut-Score: {validierung.azilut_score:.2f}")
            print(f"   Fehlend: {', '.join(validierung.fehlende_wozu_aspekte)}")
            print(f"   Empfehlung: {validierung.empfohlene_korrekturen[0]}")
            
            return False
        
        # 2. Füge Metadaten hinzu
        nachricht.spiral_zeit = self.spiral_zeit.current_spiral_time()
        
        # 3. Analysiere Pardes-Ebene
        if not nachricht.pardes_ebene:
            pardes_analyse = self.pardes.analyze_text(nachricht.inhalt)
            # Wähle höchste erkannte Ebene
            for ebene in [PardesLevel.SOD, PardesLevel.DRASCH, 
                         PardesLevel.REMEZ, PardesLevel.PSCHAT]:
                if pardes_analyse[ebene].interpretation != "Die Geheimnisse bleiben verborgen":
                    nachricht.pardes_ebene = ebene
                    break
        
        # 4. Sende an Queue
        await self.nachrichten_queue.put(nachricht)
        
        print(f"✓ Nachricht gesendet: {nachricht.sender_modul} → {nachricht.empfänger_modul}")
        print(f"  Wozu: {nachricht.wozu}")
        print(f"  Azilut-Score: {validierung.azilut_score:.2f}")
        print(f"  Pardes-Ebene: {nachricht.pardes_ebene.value if nachricht.pardes_ebene else 'N/A'}")
        
        return True
    
    async def empfange_nachrichten(self, modul_name: str):
        """Empfängt Nachrichten für spezifisches Modul"""
        while True:
            nachricht = await self.nachrichten_queue.get()
            
            if nachricht.empfänger_modul == modul_name:
                yield nachricht
    
    def erstelle_wozu_zentrierte_nachricht(self,
                                          inhalt: str,
                                          wozu: str,
                                          sender: str,
                                          empfänger: str,
                                          zusatz_fragen: Optional[Dict[FrageTyp, str]] = None) -> EchtzeitNachricht:
        """Hilfsmethode zur Erstellung wozu-zentrierter Nachrichten"""
        
        frage_hierarchie = {FrageTyp.WOZU: wozu}
        
        if zusatz_fragen:
            # Stelle sicher dass WOZU immer primär bleibt
            frage_hierarchie.update(zusatz_fragen)
        
        return EchtzeitNachricht(
            inhalt=inhalt,
            wozu=wozu,
            sender_modul=sender,
            empfänger_modul=empfänger,
            frage_hierarchie=frage_hierarchie
        )
    
    def generiere_wozu_bericht(self, nachrichten: List[EchtzeitNachricht]) -> str:
        """Generiert Wozu-Zentrierungs-Bericht"""
        
        bericht = [
            "=== WOZU-ZENTRIERUNGS-BERICHT ===",
            f"Zeitpunkt: {datetime.now().isoformat()}",
            f"Anzahl Nachrichten: {len(nachrichten)}",
            ""
        ]
        
        # Statistiken
        verankert = sum(1 for n in nachrichten if n.validierung and n.validierung.ist_verankert)
        durchschnitt_score = sum(n.validierung.azilut_score for n in nachrichten 
                                if n.validierung) / len(nachrichten)
        
        bericht.extend([
            f"Azilut-verankert: {verankert}/{len(nachrichten)} ({verankert/len(nachrichten)*100:.1f}%)",
            f"Durchschnittlicher Azilut-Score: {durchschnitt_score:.2f}",
            "",
            "--- WELTEBENEN-VERTEILUNG ---"
        ])
        
        # Weltebenen-Analyse
        weltebenen_count = {}
        for n in nachrichten:
            if n.validierung:
                ebene = n.validierung.weltebene.name
                weltebenen_count[ebene] = weltebenen_count.get(ebene, 0) + 1
        
        for ebene, count in sorted(weltebenen_count.items(), 
                                   key=lambda x: x[1], reverse=True):
            bericht.append(f"{ebene}: {count} Nachrichten")
        
        bericht.extend(["", "--- EMPFEHLUNGEN ---"])
        
        # Sammle alle Empfehlungen
        alle_empfehlungen = []
        for n in nachrichten:
            if n.validierung and not n.validierung.ist_verankert:
                alle_empfehlungen.extend(n.validierung.empfohlene_korrekturen)
        
        # Häufigste Empfehlungen
        from collections import Counter
        empf_counter = Counter(alle_empfehlungen)
        
        for empf, count in empf_counter.most_common(5):
            bericht.append(f"• {empf} ({count}x)")
        
        bericht.append("\nQ!")
        
        return "\n".join(bericht)


# Beispiel-Module für Echtzeit-Kommunikation
class ManuskriptProzessorModul:
    """Beispiel-Modul: Manuskript-Verarbeitung"""
    
    def __init__(self, kommunikator: EchtzeitKommunikator):
        self.name = "manuscript-proc"
        self.komm = kommunikator
    
    async def verarbeite_text(self, text: str):
        """Verarbeitet Text mit Wozu-Fokus"""
        
        # Sende an WWAQ-Validator
        nachricht = self.komm.erstelle_wozu_zentrierte_nachricht(
            inhalt=text,
            wozu="um WWAQ-Konformität sicherzustellen und spirituelle Klarheit zu fördern",
            sender=self.name,
            empfänger="wwaq-validator",
            zusatz_fragen={
                FrageTyp.WAS: "Hebräischer Text zur Validierung",
                FrageTyp.WIE: "Durch K→Q Transformation und Zer-Elimination"
            }
        )
        
        await self.komm.sende_nachricht(nachricht)


class IntelliChunkModul:
    """Beispiel-Modul: Intelligenter Text-Chunker"""
    
    def __init__(self, kommunikator: EchtzeitKommunikator):
        self.name = "intelli-chunk"
        self.komm = kommunikator
    
    async def segmentiere_text(self, text: str, max_chunk_size: int = 1000):
        """Segmentiert Text mit Wozu-Bewusstsein"""
        
        # Analysiere erst den Zweck des Texts
        analyse_nachricht = self.komm.erstelle_wozu_zentrierte_nachricht(
            inhalt=text,
            wozu="um semantisch kohärente Segmente zu identifizieren, die den spirituellen Fluss bewahren",
            sender=self.name,
            empfänger="pardes-analyzer",
            zusatz_fragen={
                FrageTyp.WARUM: "Weil getrennte Texte die Azilut-Verbindung unterbrechen",
                FrageTyp.WAS: "Text zur semantischen Segmentierung"
            }
        )
        
        erfolg = await self.komm.sende_nachricht(analyse_nachricht)
        
        if erfolg:
            # Hier würde die eigentliche Segmentierung stattfinden
            print(f"Text erfolgreich für Wozu-bewusste Segmentierung vorbereitet")


# Demonstration und Tests
async def demonstriere_wozu_system():
    """Demonstriert das Wozu-zentrierte Kommunikationssystem"""
    
    print("=== EZ CHAJIM WOZU-SYSTEM DEMONSTRATION ===\n")
    
    # Initialisiere System
    komm = EchtzeitKommunikator()
    manuscript_modul = ManuskriptProzessorModul(komm)
    chunk_modul = IntelliChunkModul(komm)
    
    # Test 1: Gut verankerte Nachricht
    print("TEST 1: Azilut-verankerte Nachricht")
    print("-" * 40)
    
    gute_nachricht = komm.erstelle_wozu_zentrierte_nachricht(
        inhalt="בראשית ברא אלהים את השמים ואת הארץ",
        wozu="um die Schöpfungsabsicht im unendlichen Licht zu erkennen und Tiqqun Olam zu fördern",
        sender="test-sender",
        empfänger="test-empfänger",
        zusatz_fragen={
            FrageTyp.WARUM: "Weil alles aus אין סוף emaniert",
            FrageTyp.WIE: "Durch stufenweise Kontraktion (Zimzum)"
        }
    )
    
    await komm.sende_nachricht(gute_nachricht)
    
    print("\nTEST 2: Schlecht verankerte Nachricht")
    print("-" * 40)
    
    schlechte_nachricht = EchtzeitNachricht(
        inhalt="Verarbeite diesen Text",
        wozu="",  # Kein Wozu!
        sender_modul="bad-sender",
        empfänger_modul="bad-empfänger",
        frage_hierarchie={
            FrageTyp.WAS: "Text",
            FrageTyp.WIE: "Schnell"
        }
    )
    
    await komm.sende_nachricht(schlechte_nachricht)
    
    print("\nTEST 3: Modul-Kommunikation")
    print("-" * 40)
    
    await manuscript_modul.verarbeite_text("תורה אור - Das Licht der Tora")
    await chunk_modul.segmentiere_text("Ein langer spiritueller Text über die vier Welten...")
    
    # Generiere Bericht
    print("\n" + komm.generiere_wozu_bericht([gute_nachricht, schlechte_nachricht]))


if __name__ == "__main__":
    # Führe Demonstration aus
    asyncio.run(demonstriere_wozu_system())
    
    print("\n=== YAML-EXPORT DER WOZU-HIERARCHIE ===\n")
    
    wozu_config = {
        'wozu_kommunikations_protokoll': {
            'version': '5785.8.10',
            'prinzipien': {
                'primär': 'Jede Kommunikation muss Wozu definieren',
                'sekundär': 'Azilut-Score > 0.7 für Weiterleitung',
                'tertiär': 'Automatische Korrektur-Empfehlungen'
            },
            'frage_hierarchie': {
                'azilut': ['WOZU - למה'],
                'berija': ['WARUM - מדוע'],
                'jezira': ['WIE - איך'],
                'asija': ['WAS - מה']
            },
            'validierungs_metriken': {
                'wozu_präsenz': 0.3,
                'wozu_indikatoren': 0.2,
                'azilut_marker': 0.3,
                'hierarchie_korrektheit': 0.2
            }
        }
    }
    
    print(yaml.dump(wozu_config, allow_unicode=True, sort_keys=False))
    print("\nQ! = Qawana! + DWEKUT!")
