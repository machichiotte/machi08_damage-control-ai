"""
Service d'évaluation de sinistre
Croise les données visuelles (dégâts) et contractuelles (garanties) pour décider de la couverture
"""

from typing import Dict, List, Optional
import json
from pathlib import Path


class ClaimEvaluator:
    """Évalue si un sinistre est couvert par le contrat d'assurance"""

    # Coûts moyens des pièces de voiture (en euros)
    PIECE_COSTS = {
        "bumper": 800,
        "front bumper": 800,
        "rear bumper": 750,
        "door": 1200,
        "front door": 1200,
        "rear door": 1100,
        "hood": 900,
        "trunk": 850,
        "fender": 700,
        "headlight": 400,
        "taillight": 300,
        "mirror": 250,
        "side mirror": 250,
        "wheel": 600,
        "tire": 150,
        "windshield": 500,
        "window": 300,
        "roof": 1500,
        "quarter panel": 1000,
    }

    # Mapping des garanties vers les types de dégâts couverts
    GARANTIE_COVERAGE = {
        "tous_risques": ["accident", "collision", "vandalisme", "choc"],
        "tiers": [],  # Ne couvre que les dommages causés aux tiers
        "vol": ["vol", "tentative_vol"],
        "incendie": ["incendie", "explosion"],
        "bris_de_glace": ["bris_glace", "pare_brise", "vitre"],
        "assistance": [],  # Service, pas de couverture matérielle
    }

    def __init__(self):
        print("🧠 ClaimEvaluator initialisé")

    def evaluate_claim(
        self, damage_data: Dict, contract_data: Dict, damage_type: str = "accident"
    ) -> Dict:
        """
        Évalue si le sinistre est couvert

        Args:
            damage_data: Données des dégâts détectés (objets, profondeur)
            contract_data: Données du contrat (franchise, plafond, garanties)
            damage_type: Type de sinistre (accident, vol, incendie, etc.)

        Returns:
            Dict avec la décision et les détails
        """
        print(f"\n📋 Évaluation du sinistre (type: {damage_type})")

        # 1. Vérifier si le type de sinistre est couvert
        is_covered_by_garantie = self._check_garantie_coverage(
            contract_data.get("garanties", {}), damage_type
        )

        # 2. Calculer le coût estimé des dégâts
        estimated_cost = self._calculate_damage_cost(damage_data)

        # 3. Récupérer la franchise
        franchise = contract_data.get("franchise", {})
        franchise_amount = franchise.get("amount", 0) if franchise.get("found") else 0

        # 4. Récupérer le plafond
        plafond = contract_data.get("plafond", {})
        plafond_amount = plafond.get("amount") if plafond.get("found") else None

        # 5. Décision finale
        is_covered = (
            is_covered_by_garantie
            and estimated_cost > franchise_amount
            and (plafond_amount is None or estimated_cost <= plafond_amount)
        )

        # 6. Calculer le montant remboursé
        if is_covered:
            if plafond_amount is None:
                # Pas de plafond = remboursement total (moins la franchise)
                reimbursement = estimated_cost - franchise_amount
            else:
                reimbursement = min(estimated_cost - franchise_amount, plafond_amount)
        else:
            reimbursement = 0

        # 7. Générer le résultat
        result = {
            "decision": {
                "covered": is_covered,
                "reason": self._get_decision_reason(
                    is_covered_by_garantie,
                    estimated_cost,
                    franchise_amount,
                    plafond_amount,
                ),
            },
            "costs": {
                "estimated_damage": estimated_cost,
                "franchise": franchise_amount,
                "plafond": plafond_amount,
                "reimbursement": reimbursement,
                "out_of_pocket": estimated_cost - reimbursement
                if is_covered
                else estimated_cost,
            },
            "coverage": {
                "damage_type": damage_type,
                "garantie_active": is_covered_by_garantie,
                "garanties_applicables": self._get_applicable_garanties(
                    contract_data.get("garanties", {}), damage_type
                ),
            },
            "damages": {
                "detected_parts": damage_data.get("detected_objects", []),
                "severity": self._assess_severity(damage_data),
                "breakdown": self._get_cost_breakdown(damage_data),
            },
        }

        print(f"✅ Décision: {'COUVERT' if is_covered else 'NON COUVERT'}")
        print(f"💰 Coût estimé: {estimated_cost}€")
        print(f"💳 Remboursement: {reimbursement}€")

        return result

    def _check_garantie_coverage(self, garanties: Dict, damage_type: str) -> bool:
        """Vérifie si le type de sinistre est couvert par les garanties actives"""
        for garantie_name, is_active in garanties.items():
            if is_active:
                covered_types = self.GARANTIE_COVERAGE.get(garantie_name, [])
                if damage_type in covered_types or garantie_name == "tous_risques":
                    return True
        return False

    def _get_applicable_garanties(self, garanties: Dict, damage_type: str) -> List[str]:
        """Retourne la liste des garanties applicables pour ce type de sinistre"""
        applicable = []
        for garantie_name, is_active in garanties.items():
            if is_active:
                covered_types = self.GARANTIE_COVERAGE.get(garantie_name, [])
                if damage_type in covered_types or garantie_name == "tous_risques":
                    applicable.append(garantie_name)
        return applicable

    def _calculate_damage_cost(self, damage_data: Dict) -> float:
        """Calcule le coût total des dégâts"""
        total_cost = 0
        detected_objects = damage_data.get("detected_objects", [])

        for obj in detected_objects:
            part_name = obj.get("class", "").lower()
            confidence = obj.get("confidence", 0)

            # Chercher le coût de la pièce
            base_cost = self._get_part_cost(part_name)

            # Ajuster selon la confiance de détection
            adjusted_cost = base_cost * confidence

            total_cost += adjusted_cost

        # Si aucun objet détecté, estimer selon la profondeur
        if total_cost == 0 and "depth_stats" in damage_data:
            total_cost = self._estimate_from_depth(damage_data["depth_stats"])

        return round(total_cost, 2)

    def _get_part_cost(self, part_name: str) -> float:
        """Récupère le coût d'une pièce"""
        # Chercher une correspondance exacte
        if part_name in self.PIECE_COSTS:
            return self.PIECE_COSTS[part_name]

        # Chercher une correspondance partielle
        for key, cost in self.PIECE_COSTS.items():
            if key in part_name or part_name in key:
                return cost

        # Coût par défaut si pièce inconnue
        return 500

    def _estimate_from_depth(self, depth_stats: Dict) -> float:
        """Estime le coût basé sur les statistiques de profondeur"""
        # Plus la profondeur moyenne est élevée, plus le dégât est important
        mean_depth = depth_stats.get("mean", 0)
        max_depth = depth_stats.get("max", 0)

        # Formule simple : profondeur moyenne * facteur
        # (à ajuster selon les tests réels)
        estimated_cost = (mean_depth * 10) + (max_depth * 5)

        return max(estimated_cost, 200)  # Minimum 200€

    def _assess_severity(self, damage_data: Dict) -> str:
        """Évalue la gravité des dégâts"""
        detected_count = len(damage_data.get("detected_objects", []))
        depth_stats = damage_data.get("depth_stats", {})
        mean_depth = depth_stats.get("mean", 0)

        if detected_count >= 3 or mean_depth > 150:
            return "severe"
        elif detected_count >= 2 or mean_depth > 100:
            return "moderate"
        else:
            return "minor"

    def _get_cost_breakdown(self, damage_data: Dict) -> List[Dict]:
        """Détaille le coût par pièce endommagée"""
        breakdown = []
        detected_objects = damage_data.get("detected_objects", [])

        for obj in detected_objects:
            part_name = obj.get("class", "unknown")
            confidence = obj.get("confidence", 0)
            base_cost = self._get_part_cost(part_name.lower())
            adjusted_cost = base_cost * confidence

            breakdown.append(
                {
                    "part": part_name,
                    "confidence": round(confidence * 100, 1),
                    "base_cost": base_cost,
                    "estimated_cost": round(adjusted_cost, 2),
                }
            )

        return breakdown

    def _get_decision_reason(
        self,
        is_covered_by_garantie: bool,
        estimated_cost: float,
        franchise: float,
        plafond: float,
    ) -> str:
        """Génère une explication de la décision"""
        if not is_covered_by_garantie:
            return "Type de sinistre non couvert par les garanties actives"

        if estimated_cost <= franchise:
            return f"Coût estimé ({estimated_cost}€) inférieur à la franchise ({franchise}€)"

        if plafond is not None and estimated_cost > plafond:
            return f"Coût estimé ({estimated_cost}€) supérieur au plafond ({plafond}€)"

        return "Sinistre couvert par le contrat"


# Singleton
_claim_evaluator_instance = None


def get_claim_evaluator() -> ClaimEvaluator:
    """Retourne l'instance singleton du ClaimEvaluator"""
    global _claim_evaluator_instance
    if _claim_evaluator_instance is None:
        _claim_evaluator_instance = ClaimEvaluator()
    return _claim_evaluator_instance
