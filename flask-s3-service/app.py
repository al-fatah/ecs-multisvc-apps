from flask import Flask, request, jsonify
import boto3
import os
from botocore.exceptions import NoCredentialsError, ClientError

BASE_PATH = os.getenv("BASE_PATH", "").rstrip("/")  # e.g. "/s3"
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BUCKET_NAME = os.getenv("BUCKET_NAME")

app = Flask(__name__)
s3 = boto3.client("s3", region_name=AWS_REGION)

def route(p: str) -> str:
    p = p if p.startswith("/") else f"/{p}"
    return f"{BASE_PATH}{p}"

@app.get(route("/health"))
def health():
    return {"status": "ok", "service": "flask-s3-service", "base_path": BASE_PATH}

@app.post(route("/upload"))
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "file is required"}), 400

    if not BUCKET_NAME:
        return jsonify({"message": "S3 upload skipped (BUCKET_NAME not set)", "filename": file.filename}), 200

    try:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
        return jsonify({"message": "File uploaded", "bucket": BUCKET_NAME, "filename": file.filename}), 200
    except NoCredentialsError:
        return jsonify({"error": "AWS credentials not available"}), 500
    except ClientError as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
