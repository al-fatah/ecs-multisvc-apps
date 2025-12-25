from flask import Flask, request, jsonify
import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError

BASE_PATH = os.getenv("BASE_PATH", "").rstrip("/")  # e.g. "/sqs"
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
QUEUE_URL = os.getenv("QUEUE_URL")

app = Flask(__name__)
sqs = boto3.client("sqs", region_name=AWS_REGION)

def route(p: str) -> str:
    p = p if p.startswith("/") else f"/{p}"
    return f"{BASE_PATH}{p}"

@app.get(route("/health"))
def health():
    return {"status": "ok", "service": "flask-sqs-service", "base_path": BASE_PATH}

@app.post(route("/send"))
def send():
    if not request.is_json:
        return jsonify({"error": "JSON body required"}), 400

    message = request.json.get("message")
    if not message:
        return jsonify({"error": "'message' field is required"}), 400

    if not QUEUE_URL:
        return jsonify({"message": "SQS send skipped (QUEUE_URL not set)", "body": message}), 200

    try:
        sqs.send_message(QueueUrl=QUEUE_URL, MessageBody=message)
        return jsonify({"message": "Message sent", "queue_url": QUEUE_URL}), 200
    except NoCredentialsError:
        return jsonify({"error": "AWS credentials not available"}), 500
    except ClientError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
