"""WWAQ Glossar Manager"""
import yaml

class GlossarManager:
    def __init__(self):
        with open('docs/glossar/wwaq-glossar.yaml', 'r') as f:
            self.glossar = yaml.safe_load(f)
    
    def transform(self, text):
        """Wendet WWAQ-Transformationen an"""
        for old, new in self.glossar['transformationen']['K_zu_Q'].items():
            text = text.replace(old, new)
        for old, new in self.glossar['transformationen']['Zer_Elimination'].items():
            text = text.replace(old, new)
        return text
