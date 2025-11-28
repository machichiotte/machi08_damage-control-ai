"""
Service de Zero-Shot Object Detection utilisant OWL-ViT de Hugging Face.
Permet de détecter des objets spécifiques via des requêtes textuelles (ex: "bumper").
"""

from pathlib import Path
from PIL import Image
import torch
import cv2
import numpy as np
from transformers import OwlViTProcessor, OwlViTForObjectDetection


class ZeroShotDetector:
    def __init__(self):
        """
        Initialise le modèle OWL-ViT.
        Utilise google/owlvit-base-patch32.
        """
        print("🔧 Initialisation du modèle OWL-ViT (Zero-Shot)...")

        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"✓ Utilisation du device: {self.device}")

        try:
            self.processor = OwlViTProcessor.from_pretrained(
                "google/owlvit-base-patch32"
            )
            self.model = OwlViTForObjectDetection.from_pretrained(
                "google/owlvit-base-patch32"
            ).to(self.device)
            self.model.eval()
            print("✅ Modèle OWL-ViT chargé avec succès")
        except Exception as e:
            print(f"❌ Erreur lors du chargement de OWL-ViT: {e}")
            raise e

    def detect_parts(self, image_path: Path, text_queries: list = None) -> dict:
        """
        Détecte des pièces spécifiques dans une image.

        Args:
            image_path: Chemin vers l'image source
            text_queries: Liste des textes à chercher (ex: ["bumper", "door"])

        Returns:
            dict contenant l'image annotée et les détections
        """
        if text_queries is None:
            # Requêtes simplifiées (sans "car") pour meilleure détection
            text_queries = [
                "bumper",
                "door",
                "window",
                "wheel",
                "headlight",
                "hood",
                "trunk",
                "mirror",
                "windshield",
                "tire",
                "roof",
                "fender",
            ]

        # Charger l'image
        image = Image.open(image_path).convert("RGB")
        target_sizes = torch.Tensor([image.size[::-1]])

        # Préparer les inputs
        inputs = self.processor(
            text=text_queries, images=image, return_tensors="pt"
        ).to(self.device)

        # Inférence
        with torch.no_grad():
            outputs = self.model(**inputs)

        # Post-processing pour obtenir les bounding boxes
        # Threshold augmenté pour réduire les fausses détections
        results = self.processor.post_process_object_detection(
            outputs=outputs, target_sizes=target_sizes.to(self.device), threshold=0.15
        )[0]

        # Préparer l'image pour annotation (OpenCV utilise BGR)
        image_cv = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

        detections = []

        for i, (box, score, label) in enumerate(
            zip(results["boxes"], results["scores"], results["labels"])
        ):
            box = [round(i, 2) for i in box.tolist()]
            score = round(score.item(), 3)
            label_text = text_queries[label]

            # Filtrer les scores faibles (augmenté de 0.05 à 0.1)
            if score < 0.1:
                continue

            x1, y1, x2, y2 = map(int, box)

            # Dessiner la bounding box
            # Couleur différente pour chaque classe (hash du label)
            color_seed = hash(label_text) % 255
            color = (color_seed, (color_seed * 2) % 255, (color_seed * 3) % 255)

            cv2.rectangle(image_cv, (x1, y1), (x2, y2), color, 2)

            # Ajouter le label
            label_display = f"{label_text} {score:.2f}"
            (w, h), _ = cv2.getTextSize(label_display, cv2.FONT_HERSHEY_SIMPLEX, 0.5, 1)
            cv2.rectangle(image_cv, (x1, y1 - 20), (x1 + w, y1), color, -1)
            cv2.putText(
                image_cv,
                label_display,
                (x1, y1 - 5),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (255, 255, 255),
                1,
            )

            detections.append(
                {
                    "class": label_text,
                    "confidence": score,
                    "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                }
            )

        # Appliquer NMS pour éliminer les détections qui se chevauchent
        detections = self._apply_nms(detections, iou_threshold=0.5)

        # Sauvegarder l'image annotée
        output_filename = f"parts_{image_path.name}"
        output_path = image_path.parent / output_filename
        cv2.imwrite(str(output_path), image_cv)

        # Statistiques
        stats = {
            "total_objects": len(detections),
            "classes_detected": list(set([d["class"] for d in detections])),
            "avg_confidence": np.mean([d["confidence"] for d in detections])
            if detections
            else 0,
        }

        return {
            "annotated_image_path": str(output_path),
            "annotated_image_filename": output_filename,
            "detections": detections,
            "stats": stats,
        }

    def _apply_nms(self, detections: list, iou_threshold: float = 0.5) -> list:
        """
        Applique Non-Maximum Suppression pour éliminer les détections qui se chevauchent

        Args:
            detections: Liste des détections
            iou_threshold: Seuil IoU pour considérer deux boxes comme chevauchantes

        Returns:
            Liste filtrée des détections
        """
        if len(detections) == 0:
            return detections

        # Trier par confiance décroissante
        detections = sorted(detections, key=lambda x: x["confidence"], reverse=True)

        filtered_detections = []

        while detections:
            # Prendre la détection avec la plus haute confiance
            best = detections.pop(0)
            filtered_detections.append(best)

            # Filtrer les détections qui se chevauchent trop avec celle-ci
            detections = [
                det
                for det in detections
                if self._calculate_iou(best["bbox"], det["bbox"]) < iou_threshold
            ]

        return filtered_detections

    def _calculate_iou(self, box1: dict, box2: dict) -> float:
        """
        Calcule l'Intersection over Union (IoU) entre deux bounding boxes

        Args:
            box1, box2: Dictionnaires avec x1, y1, x2, y2

        Returns:
            IoU score entre 0 et 1
        """
        # Coordonnées de l'intersection
        x1 = max(box1["x1"], box2["x1"])
        y1 = max(box1["y1"], box2["y1"])
        x2 = min(box1["x2"], box2["x2"])
        y2 = min(box1["y2"], box2["y2"])

        # Aire de l'intersection
        intersection = max(0, x2 - x1) * max(0, y2 - y1)

        # Aires des deux boxes
        area1 = (box1["x2"] - box1["x1"]) * (box1["y2"] - box1["y1"])
        area2 = (box2["x2"] - box2["x1"]) * (box2["y2"] - box2["y1"])

        # Union
        union = area1 + area2 - intersection

        # IoU
        return intersection / union if union > 0 else 0


# Instance globale
_zero_shot_detector = None


def get_zero_shot_detector() -> ZeroShotDetector:
    """Retourne l'instance singleton du ZeroShotDetector"""
    global _zero_shot_detector
    if _zero_shot_detector is None:
        _zero_shot_detector = ZeroShotDetector()
    return _zero_shot_detector
