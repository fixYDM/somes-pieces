import argparse
import pandas as pd
import joblib
import matplotlib.pyplot as plt
import os

def main(model_path, features_csv, output_csv, output_plot):
    print(f"[INFO] Running forecast using model: {model_path}")
    
    # Load model
    model = joblib.load(model_path)
    
    # Load forecast features
    df = pd.read_csv(features_csv)
    features = ['GHI', 'DIF', 'TEMP', 'diffuse_fraction', 'solar_elevation_sin', 'hour_of_day']
    X = df[features]
    
    # Predict
    df['PVOUT_kW'] = model.predict(X)
    
    # Save forecast
    os.makedirs(os.path.dirname(output_csv), exist_ok=True)
    df[['datetime', 'PVOUT_kW']].to_csv(output_csv, index=False)
    
    # Plot
    os.makedirs(os.path.dirname(output_plot), exist_ok=True)
    plt.figure(figsize=(10, 4))
    plt.plot(df['datetime'], df['PVOUT_kW'], 'b-', label='Forecasted PV Output')
    plt.title('Next-Day Solar Generation Forecast')
    plt.xlabel('Time')
    plt.ylabel('Power (kW)')
    plt.xticks(rotation=45)
    plt.grid(alpha=0.3)
    plt.tight_layout()
    plt.savefig(output_plot)
    plt.close()
    
    print(f"[SUCCESS] Forecast saved to {output_csv}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--model_path", required=True)
    parser.add_argument("--features_csv", required=True)
    parser.add_argument("--output_csv", required=True)
    parser.add_argument("--output_plot", required=True)
    args = parser.parse_args()
    main(args.model_path, args.features_csv, args.output_csv, args.output_plot)