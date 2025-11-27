"""
Service d'Object Detection utilisant YOLOv8 de Ultralytics
"""

from pathlib import Path
from PIL import Image
import cv2
import numpy as np
from ultralytics import YOLO


class ObjectDetector:
    def __init__(self):
        """
        Initialise le modèle YOLOv8.
        Utilise yolov8n (nano) pour des performances optimales.
        """
        print("🔧 Initialisation du modèle YOLO...")

        # Charger le modèle YOLOv8 nano (le plus léger)
        self.model = YOLO("yolov8n.pt")

        print("✅ Modèle YOLO chargé avec succès")

    def detect_objects(self, image_path: Path) -> dict:
        """
        Détecte les objets dans une image.

        Args:
            image_path: Chemin vers l'image source

        Returns:
            dict contenant:
                - annotated_image_path: Chemin vers l'image avec bounding boxes
                - detections: Liste des objets détectés
                - stats: Statistiques de détection
        """
        # Charger l'image
        image = Image.open(image_path)

        # Effectuer la détection
        results = self.model(image, conf=0.25)  # Seuil de confiance à 25%

        # Obtenir le premier résultat (une seule image)
        result = results[0]

        # Créer l'image annotée avec les bounding boxes
        annotated_image = result.plot()  # Retourne un numpy array

        # Sauvegarder l'image annotée
        output_path = image_path.parent / f"detected_{image_path.name}"
        cv2.imwrite(str(output_path), annotated_image)

        # Extraire les détections
        detections = []
        boxes = result.boxes

        for box in boxes:
            # Coordonnées de la bounding box
            x1, y1, x2, y2 = box.xyxy[0].tolist()

            # Classe et confiance
            class_id = int(box.cls[0])
            confidence = float(box.conf[0])
            class_name = result.names[class_id]

            detections.append(
                {
                    "class": class_name,
                    "confidence": confidence,
                    "bbox": {"x1": x1, "y1": y1, "x2": x2, "y2": y2},
                }
            )

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
            "annotated_image_filename": output_path.name,
            "detections": detections,
            "stats": stats,
        }


# Instance globale (singleton pattern)
_object_detector = None


def get_object_detector() -> ObjectDetector:
    """Retourne l'instance singleton de l'ObjectDetector"""
    global _object_detector
    if _object_detector is None:
        _object_detector = ObjectDetector()
    return _object_detector
