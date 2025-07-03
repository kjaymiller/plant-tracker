"""
Get readings from grow hat
"""

import socket
import time
import os
import datetime
import json
import logging

import dotenv
import psycopg

from grow.moisture import Moisture


dotenv.load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.WARNING,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%dT%H:%M:%S",
    handlers=[logging.FileHandler("grow_hat.log"), logging.StreamHandler()],
)

logger = logging.getLogger(__name__)

connection = psycopg.connect(os.getenv("PG_CONNECTION_STRING"))

sensors = {
    "m1": Moisture(1),
    "m2": Moisture(2),
    "m3": Moisture(3),
}


def reading():
    time.sleep(2)
    try:
        data = {
            "sensors": {k: v._reading for k, v in sensors.items() if v.active},
            "device": socket.gethostname(),
        }
        dumped_data = json.dumps(data)

        with connection.cursor() as cursor:
            cursor.execute(
                """
                Insert INTO moisture_logs (datetime, moisture_data) 
                VALUES (%s, %s)
                """,
                (datetime.datetime.now().isoformat(), dumped_data),
            )
            connection.commit()
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    reading()
