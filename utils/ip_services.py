import requests
from flask import jsonify
from config import Config
import logging

logger = logging.getLogger(__name__)


class IPLocationservice:
    def __init__(self):
        self.ip_api = Config.IP_API_URL
        self.ipify = Config.IPIFY_URL

    def get_public_ip(self):
        logger.info(f"Start to request IP {self.ipify}")
        try:
            ip = requests.get(self.ipify, timeout=10).json().get("ip")
            if ip:
                return ip
            else:
                logger.error("Failed to extract IP from response")
                return None
        except requests.RequestException as e:
            logger.error(f"Network Error for public ip : {e}")
            return None

    def get_location_data(self, ip_address=None):
        logger.info(f"Start to request IP {self.ip_api}/{ip_address}")
        try:
            response = requests.get(f"{self.ip_api}/{ip_address}", timeout=10)
            response.raise_for_status()
            data = response.json()

            if data.get("status") == "fail":
                return jsonify({"status": "fail", "data": "Could not fetch location"})
            return jsonify(data)

        except requests.RequestException as e:
            logger.error(f"Network Error for ip location: {e}")
            return jsonify(
                {"status": "fail", "data": f"Failed to fetch data: {str(e)}"}
            )
