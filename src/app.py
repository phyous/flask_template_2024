from flask import Flask, jsonify
from models import User

app = Flask(__name__)

@app.route("/healthcheck")
def healthcheck():
    return jsonify({"status": "healthy"}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8000) 