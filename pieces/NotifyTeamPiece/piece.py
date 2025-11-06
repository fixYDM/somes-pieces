import argparse
import json
import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def send_email(metrics):
    # Email configuration from environment variables
    smtp_server = os.getenv("SMTP_SERVER", "smtp.gmail.com")
    smtp_port = int(os.getenv("SMTP_PORT", "587"))
    sender_email = os.getenv("SENDER_EMAIL")
    sender_password = os.getenv("SENDER_PASSWORD")
    recipient_email = os.getenv("RECIPIENT_EMAIL", "energy-team@fixydm.com")
    
    if not sender_email or not sender_password:
        print("[WARNING] Email credentials not configured. Skipping email.")
        return
    
    # Create message
    msg = MIMEMultipart()
    msg['From'] = sender_email
    msg['To'] = recipient_email
    msg['Subject'] = f"✅ Solar XGBoost Model Trained - MAE: {metrics['MAE_kW']} kW"
    
    body = f"""
    Hello Team,
    
    The daily XGBoost training has completed successfully.
    
    Performance Metrics:
    - MAE: {metrics['MAE_kW']} kW
    - R²: {metrics['R2']}
    - Samples: {metrics['samples']:,}
    
    Model registered in Domino.
    
    Best regards,
    SoMES Pipeline
    """
    
    msg.attach(MIMEText(body, 'plain'))
    
    # Send email
    try:
        server = smtplib.SMTP(smtp_server, smtp_port)
        server.starttls()
        server.login(sender_email, sender_password)
        text = msg.as_string()
        server.sendmail(sender_email, recipient_email, text)
        server.quit()
        print(f"[SUCCESS] Email sent to {recipient_email}")
    except Exception as e:
        print(f"[ERROR] Failed to send email: {e}")

def send_slack(metrics, webhook_url):
    import requests
    
    payload = {
        "text": f"*Solar XGBoost pipeline completed*\n"
                f"> *MAE*: {metrics['MAE_kW']} kW\n"
                f"> *R²*: {metrics['R2']}\n"
                f"> *Samples*: {metrics['samples']:,}\n"
                f"> <{os.getenv('DOMINO_PROJECT_URL', '#')}|View model in Domino>"
    }
    
    try:
        response = requests.post(webhook_url, json=payload)
        response.raise_for_status()
        print("[SUCCESS] Slack notification sent")
    except Exception as e:
        print(f"[ERROR] Failed to send Slack notification: {e}")

def main(metrics_path, webhook_url):
    print(f"[INFO] Sending notifications...")
    
    # Load metrics
    with open(metrics_path) as f:
        metrics = json.load(f)
    
    # Send email
    send_email(metrics)
    
    # Send Slack notification if webhook provided
    if webhook_url:
        send_slack(metrics, webhook_url)
    
    print("[SUCCESS] Notifications completed")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--metrics_path", required=True)
    parser.add_argument("--webhook_url", required=False)
    args = parser.parse_args()
    main(args.metrics_path, args.webhook_url)