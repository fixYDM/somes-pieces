import argparse
import pandas as pd
import numpy as np

def main(input_path, output_path):
    print(f"[INFO] Preprocessing {input_path} → {output_path}")
    
    # Load data
    df = pd.read_csv(input_path, sep=';', parse_dates={'datetime': ['Date', 'Time']}, dayfirst=True)
    df['datetime'] = pd.to_datetime(df['datetime'], format='%d.%m.%Y %H:%M')
    
    # Filter out night hours
    df = df[df['GHI'] > 1].copy()
    
    # Feature engineering for CIS panels
    df['diffuse_fraction'] = np.where(df['GHI'] > 0, df['DIF'] / df['GHI'], 0)
    df['solar_elevation_sin'] = np.sin(np.radians(df['SE']))
    df['hour_of_day'] = df['datetime'].dt.hour
    
    # Save processed data
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    df.to_csv(output_path, index=False)
    print(f"[SUCCESS] Preprocessed data saved to {output_path}")

if __name__ == "__main__":
    import os
    parser = argparse.ArgumentParser()
    parser.add_argument("--input_path", required=True)
    parser.add_argument("--output_path", required=True)
    args = parser.parse_args()
    main(args.input_path, args.output_path)