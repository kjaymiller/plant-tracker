# Plant Tracker

A Raspberry Pi-based plant monitoring system that tracks soil moisture levels using the Pimoroni Grow HAT and stores data in a PostgreSQL database.

## Hardware Requirements

- Raspberry Pi (Works with Pi4 and Pi Zero WH. Imaged using the Raspberry Pi Imager)
- [Pimoroni Grow HAT](https://shop.pimoroni.com/products/grow) - Available at Pimoroni
- Up to 3 moisture sensors (connected to the Grow HAT)

## Features

- Real-time moisture monitoring from up to 3 sensors
- Data logging to PostgreSQL database with timestamps
- Device hostname tracking for multi-device deployments
- Plant and device registration system
- Rich console output with loading spinners
- Comprehensive logging to file and console

## Database Schema

The system uses a PostgreSQL database with the following tables:

- **devices**: Store device information (hostname, location)
- **moisture_logs**: Time-series moisture data with JSON storage
- **plant_types**: Scientific plant classification
- **plants**: Individual plant records
- **plant_device_registration**: Links plants to monitoring devices

## Installation

> [!WARNING]
> You need the headers installed on your Pi Zero for the grow hat.

Step 1: Set up your Raspberry Pi with the [Grow HAT python modules](https://github.com/pimoroni/grow-python/tree/main?tab=readme-ov-file#one-line-installs-from-github)
Install required Python dependencies:

```bash
pip install -r requirements.txt
```

Set up your PostgreSQL database using the provided schema:
   ```bash
   psql -f setup.sql
   ```

Configure your database connection in a `.env` file:
```
echo "PG_CONNECTION_STRING=<YOUR_POSTGRESQL_CONNECTION_STRING> > .env"
```

## Usage

Run the moisture reading script:
```bash
python db_store.py
```

The script will:
- Initialize 3 moisture sensors
- Display a loading spinner while sensors come online
- Read moisture levels from all sensors
- Store the data in the database with timestamp and device information

## Data Format

Moisture readings are stored as JSON in the database:
```json
{
  "sensors": {
    "m1": 0.45,
    "m2": 0.62,
    "m3": 0.38
  },
  "device": "raspberrypi-001"
}
```

## Logging

The system logs to both console and file (`grow_hat.log`) with warnings for sensor connection issues and errors for database problems.

## License

See LICENSE file for details.
