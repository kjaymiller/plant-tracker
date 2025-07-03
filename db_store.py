"""
Get readings from grow hat
"""

import socket
import os
import time
import datetime
import json
import logging

import dotenv
import psycopg
from rich import print as rprint
from rich.live import Live
from rich.spinner import Spinner

from grow.moisture import Moisture


dotenv.load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.WARNING,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt="%Y-%m-%dT%H:%M:%S",
    handlers=[
        logging.FileHandler('grow_hat.log'),
        logging.StreamHandler()
    ]
)

logger = logging.getLogger(__name__)

connection = psycopg.connect(os.getenv("AIVEN_PG_CONNECTION_STRING"))

def reading():
    meter = [Moisture(_+1) for _ in range(3)]
    spinner = Spinner(name="line", text="Loading Sensors") 
    process_timer = datetime.datetime.now()

    with Live(spinner.render(0.5), refresh_per_second=10) as live:
        meters_online = [m.moisture for m in meter]

        while not all(meters_online):
            meters_online = [m.moisture for m in meter]
            if (process_timer - datetime.datetime.now()).total_seconds() >= 3 and not all(meters_online):
                msg = "Unable to process all nodes please check device"
                logger.warning(msg)
                break
    try:
        data = {
            "sensors": {
                "m1": meter[0].moisture,
                "m2": meter[1].moisture,
                "m3": meter[2].moisture,
            },
            "device": socket.gethostname(),
        }

        dumped_data = json.dumps(data)
        print(dumped_data)
        return

        with connection.cursor() as cursor:
            cursor.execute("""
                Insert INTO moisture_logs (datetime, moisture_data) 
                VALUES (%s, %s)
                """,
                (
                    datetime.datetime.now().isoformat(),
                    dumped_data
                ),
            )
            connection.commit()
    except Exception as e:
        logger.error(e)


if __name__ == "__main__":
    reading()
