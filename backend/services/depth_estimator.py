"""
Service de Depth Estimation utilisant Depth Anything de Hugging Face
"""

from pathlib import Path
from PIL import Image
import torch
from transformers import pipeline
import numpy as np
import cv2


class DepthEstimator:
    def __init__(self):
        """
        Initialise le modèle de depth estimation.
        Utilise depth-anything-small pour des performances optimales.
        """
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"🔧 Initialisation du modèle Depth Estimation sur {self.device}...")

        # Utiliser le modèle Depth Anything Small (plus rapide)
        self.pipe = pipeline(
            task="depth-estimation",
            model="LiheYoung/depth-anything-small-hf",
            device=0 if self.device == "cuda" else -1,
        )
        print("✅ Modèle Depth Estimation chargé avec succès")

    def estimate_depth(self, image_path: Path) -> dict:
        """
        Génère une depth map à partir d'une image.

        Args:
            image_path: Chemin vers l'image source

        Returns:
            dict contenant:
                - depth_map_path: Chemin vers la depth map générée
                - depth_array: Array numpy de la profondeur
                - stats: Statistiques (min, max, mean)
        """
        # Charger l'image
        image = Image.open(image_path).convert("RGB")

        # Générer la depth map
        result = self.pipe(image)
        depth_map = result["depth"]

        # Convertir en numpy array pour traitement
        depth_array = np.array(depth_map)

        # Normaliser pour visualisation (0-255)
        depth_normalized = cv2.normalize(
            depth_array, None, 0, 255, cv2.NORM_MINMAX, dtype=cv2.CV_8U
        )

        # Appliquer une colormap pour meilleure visualisation
        depth_colored = cv2.applyColorMap(depth_normalized, cv2.COLORMAP_INFERNO)

        # Sauvegarder la depth map
        output_path = image_path.parent / f"depth_{image_path.name}"
        cv2.imwrite(str(output_path), depth_colored)

        # Calculer des statistiques
        stats = {
            "min_depth": float(depth_array.min()),
            "max_depth": float(depth_array.max()),
            "mean_depth": float(depth_array.mean()),
            "std_depth": float(depth_array.std()),
        }

        return {
            "depth_map_path": str(output_path),
            "depth_map_filename": output_path.name,
            "stats": stats,
            "device_used": self.device,
        }


# Instance globale (singleton pattern)
_depth_estimator = None


def get_depth_estimator() -> DepthEstimator:
    """Retourne l'instance singleton du DepthEstimator"""
    global _depth_estimator
    if _depth_estimator is None:
        _depth_estimator = DepthEstimator()
    return _depth_estimator
