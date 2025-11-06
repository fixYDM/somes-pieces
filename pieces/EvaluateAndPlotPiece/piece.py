import argparse
import pandas as pd
import joblib
import json
import matplotlib.pyplot as plt
import os
from sklearn.metrics import mean_absolute_error, r2_score

def main(data_path, model_path, metrics_out, plot_out):
    print(f"[INFO] Evaluating model: {model_path}")
    
    # Load data and model
    df = pd.read_csv(data_path)
    model = joblib.load(model_path)
    
    # Prepare features and target
    features = ['GHI', 'DIF', 'TEMP', 'diffuse_fraction', 'solar_elevation_sin', 'hour_of_day']
    X = df[features]
    y_true = df['PVOUT']
    
    # Predict
    y_pred = model.predict(X)
    
    # Calculate metrics
    mae = mean_absolute_error(y_true, y_pred)
    r2 = r2_score(y_true, y_pred)
    
    # Save metrics
    metrics = {
        "MAE_kW": round(mae, 4),
        "R2": round(r2, 4),
        "samples": len(y_true)
    }
    os.makedirs(os.path.dirname(metrics_out), exist_ok=True)
    with open(metrics_out, "w") as f:
        json.dump(metrics, f, indent=2)
    
    # Plot comparison
    os.makedirs(os.path.dirname(plot_out), exist_ok=True)
    plt.figure(figsize=(12, 5))
    plt.plot(y_true.values, label="Solargis PVOUT", color="steelblue")
    plt.plot(y_pred, '--', label="XGBoost prediction", color="crimson")
    plt.title(f"XGBoost vs Solargis (MAE={mae:.3f} kW, R²={r2:.3f})")
    plt.xlabel("Time index (15-min steps)")
    plt.ylabel("Power (kW)")
    plt.legend()
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(plot_out, dpi=150)
    plt.close()
    
    print(f"[SUCCESS] Evaluation complete. Metrics: {metrics}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data_path", required=True)
    parser.add_argument("--model_path", required=True)
    parser.add_argument("--metrics_out", required=True)
    parser.add_argument("--plot_out", required=True)
    args = parser.parse_args()
    main(args.data_path, args.model_path, args.metrics_out, args.plot_out)