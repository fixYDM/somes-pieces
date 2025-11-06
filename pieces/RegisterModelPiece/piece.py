import argparse
import json
import os
from domino import Model, ModelVersion

def main(model_path, metrics_path, name, description):
    print(f"[INFO] Registering model: {name}")
    
    # Load metrics
    with open(metrics_path) as f:
        metrics = json.load(f)
    
    # Create/get model
    model = Model.get_or_create(name=name, description=description or "")
    
    # Register version
    version = ModelVersion.create(
        model=model,
        files=[model_path],
        metadata={
            "MAE_kW": metrics["MAE_kW"],
            "R2": metrics["R2"],
            "samples": metrics["samples"],
            "trained_at": os.getenv("DOMINO_RUN_START_TIME", "unknown")
        },
        description=f"Daily retrain {os.getenv('DOMINO_RUN_START_TIME', 'unknown')}"
    )
    
    print(f"[SUCCESS] Model registered. Version ID: {version.id}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", required=True)
    parser.add_argument("--metrics_path", required=True)
    parser.add_argument("--name", required=True)
    parser.add_argument("--description", required=False, default="")
    args = parser.parse_args()
    main(args.model_path, args.metrics_path, args.name, args.description)