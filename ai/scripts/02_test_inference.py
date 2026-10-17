import json
import os
from pathlib import Path
from ai.inference.engine import InferenceEngine

def test_inference():
    # 1. Setup paths
    # In a real scenario, ensure ai/models/weights/best.pt exists
    model_path = "ai/models/weights/best.pt"

    # Use a sample image from the processed test set
    test_images_dir = Path("data/processed/multi_hazards/images/test")
    if not test_images_dir.exists() or not list(test_images_dir.glob("*.png")):
        print("Error: No test images found in data/processed/multi_hazards/images/test")
        return

    sample_img = list(test_images_dir.glob("*.png"))[0]
    print(f"Testing inference on: {sample_img}")

    # 2. Initialize Engine
    engine = InferenceEngine(model_path=model_path)

    try:
        # 3. Run Prediction
        print("Running prediction...")
        result = engine.predict(str(sample_img))

        # 4. Print JSON Output
        print("\n--- AI Damage Summary ---")
        print(json.dumps(result, indent=2))
        print("------------------------\n")

        # 5. Save Visualization
        output_viz = "ai/visualizations/test_inference_result.png"
        engine.save_prediction_image(str(sample_img), output_viz)
        print(f"Visualization saved to: {output_viz}")

    except RuntimeError as e:
        print(f"Inference failed: {e}")
        print("Note: This is expected if ai/models/weights/best.pt has not been downloaded from Colab yet.")
    except Exception as e:
        print(f"An unexpected error occurred: {e}")

if __name__ == "__main__":
    test_inference()
