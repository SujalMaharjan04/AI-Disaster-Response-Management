import json
import logging
from pathlib import Path
from typing import Dict, Any, Tuple
import numpy as np
from ultralytics import YOLO

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class InferenceEngine:
    def __init__(self, model_path: str = "ai/models/weights/best.pt"):
        """
        Initializes the YOLO inference engine.
        model_path: Path to the trained .pt weights.
        """
        self.model_path = Path(model_path)
        if not self.model_path.exists():
            logger.warning(f"Model weights not found at {model_path}. Inference will fail until weights are provided.")
            self.model = None
        else:
            logger.info(f"Loading model from {model_path}...")
            self.model = YOLO(str(self.model_path))

    def predict(self, image_path: str, conf_threshold: float = 0.25) -> Dict[str, Any]:
        """
        Runs inference on an image and returns a structured damage summary.
        """
        if self.model is None:
            raise RuntimeError("Model not loaded. Please check the model path.")

        # Perform prediction
        results = self.model.predict(
            source=image_path,
            conf=conf_threshold,
            save=False,
            verbose=False
        )

        result = results[0]

        # damage_class mapping
        # 0: No Damage, 1: Minor, 2: Major, 3: Destroyed
        counts = {
            "no_damage": 0,
            "minor_damage": 0,
            "major_damage": 0,
            "destroyed": 0
        }

        if result.boxes is not None:
            # Get classes for all detected boxes
            classes = result.boxes.cls.cpu().numpy().astype(int)
            for cls in classes:
                if cls == 0: counts["no_damage"] += 1
                elif cls == 1: counts["minor_damage"] += 1
                elif cls == 2: counts["major_damage"] += 1
                elif cls == 3: counts["destroyed"] += 1

        total_buildings = sum(counts.values())

        # Average confidence of detections
        confidence = float(result.boxes.conf.mean().item()) if result.boxes is not None and len(result.boxes) > 0 else 0.0

        summary = {
            "location": Path(image_path).name,
            "damage_summary": {
                "total_buildings": total_buildings,
                "destroyed": counts["destroyed"],
                "major_damage": counts["major_damage"],
                "minor_damage": counts["minor_damage"],
                "no_damage": counts["no_damage"]
            },
            "confidence": round(confidence, 2)
        }

        return summary

    def save_prediction_image(self, image_path: str, output_path: str):
        """
        Saves an image with predicted masks and boxes overlaid.
        """
        if self.model is None:
            raise RuntimeError("Model not loaded.")

        results = self.model.predict(source=image_path, save=False)
        result = results[0]

        # Plot results on image
        res_plotted = result.plot()

        import cv2
        cv2.imwrite(output_path, res_plotted)
        logger.info(f"Saved prediction visualization to {output_path}")
