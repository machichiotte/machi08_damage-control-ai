"""
Service d'analyse de contrat d'assurance.
Extrait les informations clés (franchise, plafond, garanties) via regex.
"""

import re
from typing import Dict, Optional


class ContractAnalyzer:
    def __init__(self):
        """
        Initialise l'analyseur de contrat.
        """
        print("🔧 Initialisation du ContractAnalyzer...")
        print("✅ ContractAnalyzer prêt")

    def extract_franchise(self, text: str) -> Optional[Dict]:
        """
        Extrait la franchise du contrat.

        Args:
            text: Texte du contrat

        Returns:
            Dict avec la franchise trouvée ou None
        """
        # Patterns pour détecter la franchise
        patterns = [
            r"franchise[:\s]+(\d+[\s,.]?\d*)\s*€",
            r"franchise[:\s]+(\d+[\s,.]?\d*)\s*euros?",
            r"montant de la franchise[:\s]+(\d+[\s,.]?\d*)\s*€",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount = match.group(1).replace(" ", "").replace(",", ".")
                return {"amount": float(amount), "currency": "EUR", "found": True}

        return {"found": False, "amount": None}

    def extract_plafond(self, text: str) -> Optional[Dict]:
        """
        Extrait le plafond de garantie du contrat.

        Args:
            text: Texte du contrat

        Returns:
            Dict avec le plafond trouvé ou None
        """
        # Patterns pour détecter le plafond
        patterns = [
            r"plafond[:\s]+(\d+[\s,.]?\d*)\s*€",
            r"plafond de garantie[:\s]+(\d+[\s,.]?\d*)\s*€",
            r"limite de garantie[:\s]+(\d+[\s,.]?\d*)\s*€",
            r"montant maximum[:\s]+(\d+[\s,.]?\d*)\s*€",
        ]

        for pattern in patterns:
            match = re.search(pattern, text, re.IGNORECASE)
            if match:
                amount = match.group(1).replace(" ", "").replace(",", ".")
                return {"amount": float(amount), "currency": "EUR", "found": True}

        return {"found": False, "amount": None}

    def extract_garanties(self, text: str) -> Dict:
        """
        Détecte le type de garanties présentes dans le contrat.

        Args:
            text: Texte du contrat

        Returns:
            Dict avec les garanties détectées
        """
        garanties = {
            "tous_risques": False,
            "tiers": False,
            "vol": False,
            "incendie": False,
            "bris_de_glace": False,
            "assistance": False,
        }

        text_lower = text.lower()

        if "tous risques" in text_lower or "tout risque" in text_lower:
            garanties["tous_risques"] = True

        if "responsabilité civile" in text_lower or "au tiers" in text_lower:
            garanties["tiers"] = True

        if "vol" in text_lower:
            garanties["vol"] = True

        if "incendie" in text_lower:
            garanties["incendie"] = True

        if "bris de glace" in text_lower or "brise de glace" in text_lower:
            garanties["bris_de_glace"] = True

        if "assistance" in text_lower or "dépannage" in text_lower:
            garanties["assistance"] = True

        return garanties

    def analyze_contract(self, text: str) -> Dict:
        """
        Analyse complète du contrat.

        Args:
            text: Texte extrait du contrat

        Returns:
            Dict avec toutes les informations extraites
        """
        print("📋 Analyse du contrat en cours...")

        franchise = self.extract_franchise(text)
        plafond = self.extract_plafond(text)
        garanties = self.extract_garanties(text)

        # Compter les garanties actives
        garanties_actives = [k for k, v in garanties.items() if v]

        result = {
            "franchise": franchise,
            "plafond": plafond,
            "garanties": garanties,
            "summary": {
                "franchise_found": franchise["found"],
                "plafond_found": plafond["found"],
                "garanties_count": len(garanties_actives),
                "garanties_actives": garanties_actives,
            },
        }

        print(f"✓ Analyse terminée: {len(garanties_actives)} garanties détectées")
        return result


# Instance globale
_contract_analyzer = None


def get_contract_analyzer() -> ContractAnalyzer:
    """Retourne l'instance singleton du ContractAnalyzer"""
    global _contract_analyzer
    if _contract_analyzer is None:
        _contract_analyzer = ContractAnalyzer()
    return _contract_analyzer
