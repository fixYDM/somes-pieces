import argparse
import pandas as pd
import joblib
from xgboost import XGBRegressor

def main(data_path, model_out, log_out):
    df = pd.read_csv(data_path)
    features = ['GHI', 'DIF', 'TEMP', 'diffuse_fraction', 'solar_elevation_sin', 'hour_of_day']
    X = df[features]
    y = df['PVOUT']
    
    model = XGBRegressor(
        objective='reg:squarederror',
        learning_rate=0.05,
        max_depth=3,
        n_estimators=250
    )
    model.fit(X, y)
    
    joblib.dump(model, model_out)
    with open(log_out, "w") as f:
        f.write(f"Model trained at {pd.Timestamp.now()}")
    print(f"[INFO] Model saved to {model_out}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--data", required=True)
    parser.add_argument("--model_out", required=True)
    parser.add_argument("--log_out", required=True)
    args = parser.parse_args()
    main(args.data, args.model_out, args.log_out)