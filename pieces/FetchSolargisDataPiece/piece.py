import argparse
import boto3
import os
from urllib.parse import urlparse

def main(s3_path, output_path):
    print(f"[INFO] Fetching data from {s3_path} → {output_path}")
    
    # Parse S3 path
    parsed = urlparse(s3_path, allow_fragments=False)
    if parsed.scheme == "s3":
        bucket = parsed.netloc
        key = parsed.path.lstrip('/')
        
        # Initialize S3 client
        s3 = boto3.client('s3')
        
        # Create output directory if not exists
        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        
        # Download file
        s3.download_file(bucket, key, output_path)
        print(f"[SUCCESS] Downloaded {s3_path}")
    else:
        raise ValueError("Only S3 paths are supported")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--s3_path", required=True)
    parser.add_argument("--output_path", required=True)
    args = parser.parse_args()
    main(args.s3_path, args.output_path)