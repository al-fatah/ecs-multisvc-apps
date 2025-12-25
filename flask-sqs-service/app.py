from flask import Flask, request, jsonify
import boto3
import os
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
QUEUE_URL = os.getenv("QUEUE_URL")

sqs = boto3.client("sqs", region_name=AWS_REGION)

@app.get("/health")
def health():
    return {"status": "ok", "service": "flask-sqs-service"}

@app.post("/send")
def send():
    if not request.is_json:
        return jsonify({"error": "JSON body required"}), 400

    message = request.json.get("message")
    if not message:
        return jsonify({"error": "'message' field is required"}), 400

    # Local-safe behavior
    if not QUEUE_URL:
        return jsonify({
            "message": "SQS send skipped (QUEUE_URL not set)",
            "body": message
        }), 200

    try:
        sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=message
        )
        return jsonify({
            "message": "Message sent",
            "queue_url": QUEUE_URL
        }), 200
    except NoCredentialsError:
        return jsonify({"error": "AWS credentials not available"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
