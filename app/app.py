import os
import logging
from flask import Flask, jsonify

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

APP_VERSION = os.environ.get("APP_VERSION", "1.0.0")
APP_COLOR   = os.environ.get("APP_COLOR", "green")
APP_ENV     = os.environ.get("APP_ENV", "production")


@app.route("/")
def home():
    logger.info("GET / called")
    return jsonify({
        "message": "Hello from Blue-Green Deployment Demo!",
        "version": APP_VERSION,
        "color":   APP_COLOR,
        "env":     APP_ENV,
    })


@app.route("/health")
def health():
    return jsonify({"status": "healthy", "version": APP_VERSION}), 200


@app.route("/info")
def info():
    return jsonify({
        "app":     "blue-green-demo",
        "version": APP_VERSION,
        "color":   APP_COLOR,
        "env":     APP_ENV,
    })


if __name__ == "__main__":
    port = int(os.environ.get("PORT", 80))
    app.run(host="0.0.0.0", port=port)
