# Plant Tracker

A Django web application for tracking plants, their moisture levels, and associated IoT devices.

## Features

- **Plant Management**: Track individual plants with names, scientific names, and notes
- **Device Integration**: Register and manage IoT devices for monitoring plants
- **Moisture Monitoring**: Log and track moisture data from connected devices
- **Plant Types**: Manage plant species with scientific classifications
- **Device Registration**: Associate devices with specific plants for monitoring

## Models

- **Plants**: Store plant information including names, scientific names, and notes
- **Devices**: Manage IoT devices with hostname and location tracking
- **MoistureLogs**: Record moisture sensor data with timestamps
- **PlantTypes**: Catalog plant species with scientific names
- **PlantDeviceRegistration**: Link plants to monitoring devices

## Requirements

- Python ≥ 3.13
- PostgreSQL database
- Django ≥ 5.2.4

## Setup

### Using UV (Recommended)

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd plant-tracker
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Set up environment variables (create `.env` file):
   ```
   DATABASE_URL=postgresql://username:password@localhost:5432/plant_tracker
   ```

4. Run migrations:
   ```bash
   uv run python manage.py migrate
   ```

5. Create a superuser:
   ```bash
   uv run python manage.py createsuperuser
   ```

6. Start the development server:
   ```bash
   uv run python manage.py runserver
   ```

### Using Docker

1. Build and run with Docker:
   ```bash
   docker build -t plant-tracker .
   docker run -p 8000:8000 plant-tracker
   ```

## Database Configuration

The application uses PostgreSQL and supports multiple connection configurations through `.pg_service.conf` and various credential files for different providers (Aiven, Neon, Supabase, etc.).

## Development

The project structure:
- `plant_tracker/` - Django project settings
- `plants/` - Main application with models, views, and forms
- `requirements.txt` - Python dependencies (legacy)
- `pyproject.toml` - Modern Python project configuration
- `Dockerfile` - Container configuration

## License

Licensed under the terms specified in the LICENSE file.