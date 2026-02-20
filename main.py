from flask import Flask, jsonify
import requests
from utils.ip_services import IPLocationservice
from config import Config
import logging
import sys

# Configure logging with dynamic log level
logging.basicConfig(
    level=getattr(logging, Config.LOG_LEVEL, logging.INFO),
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stdout,
)

logger = logging.getLogger(__name__)

app = Flask(__name__)
ip_services = IPLocationservice()


@app.route("/get-location", methods=["GET"])
def get_location():
    try:
        ip = ip_services.get_public_ip()
        if not ip:
            return jsonify({"status": "fail", "data": "Could not retrieve public IP"})

        return ip_services.get_location_data(ip)

    except requests.RequestException as e:
        logger.error(f"Network Error : {e}")
        return jsonify({"status": "fail", "data": "Failed to fetch data"}), 500
    except Exception as error:
        logger.error(f"Other Error : {error}")
        return jsonify({"status": "fail", "data": "Failed to fetch data"}), 500


if __name__ == "__main__":
    logger.info(f"Starting IP Location Service on port {Config.PORT}")
    app.run(debug=Config.DEBUG, port=Config.PORT, host="0.0.0.0")
