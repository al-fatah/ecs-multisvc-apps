from flask import Flask
app = Flask(__name__)

@app.get("/health")
def health():
    return {"status": "ok", "service": "flask-sqs-service"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8081)
