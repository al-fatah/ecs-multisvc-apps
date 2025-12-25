from flask import Flask, request, jsonify
import boto3
import os
from botocore.exceptions import NoCredentialsError

app = Flask(__name__)

AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
BUCKET_NAME = os.getenv("BUCKET_NAME")

s3 = boto3.client("s3", region_name=AWS_REGION)

@app.get("/health")
def health():
    return {"status": "ok", "service": "flask-s3-service"}

@app.post("/upload")
def upload():
    file = request.files.get("file")
    if not file:
        return jsonify({"error": "file is required"}), 400

    # Local-safe behavior
    if not BUCKET_NAME:
        return jsonify({
            "message": "S3 upload skipped (BUCKET_NAME not set)",
            "filename": file.filename
        }), 200

    try:
        s3.upload_fileobj(file, BUCKET_NAME, file.filename)
        return jsonify({
            "message": "File uploaded",
            "bucket": BUCKET_NAME,
            "filename": file.filename
        }), 200
    except NoCredentialsError:
        return jsonify({"error": "AWS credentials not available"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)
