# Plant Tracker

A Django web application for tracking plants, their moisture levels, and associated IoT devices.

## Features

- **Plant Management**: Track individual plants with names, scientific names, and notes
- **Plant Types**: Manage plant species with scientific classifications

## Requirements

- Python >= 3.13
- PostgreSQL database >= 17.0
- Django >= 5.2.4

## Setup

### Database Schema Restoration (First Time Setup)

If you're setting up the project for the first time and have the schema backup, restore it before running migrations:

1. Start PostgreSQL (either locally or using the provided Docker setup):
   ```bash
   # Using the backup Docker container
   docker build -f Dockerfile.pg18 -t plant-tracker-pg18 .
   docker run --name plant-tracker-db -e POSTGRES_PASSWORD=password -p 5432:5432 -d plant-tracker-pg18
   ```

2. Restore the schema from backup:
   ```bash
   # Wait a moment for PostgreSQL to start, then restore
   psql -h localhost -U postgres -d postgres -f schema_backup.sql
   ```


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

## Development

The project structure:
- `plant_tracker/` - Django project settings
- `plants/` - Main application with models, views, and forms
- `pyproject.toml` - Modern Python project configuration
- `Dockerfile` - Container configuration

## License

Licensed under the terms specified in the [LICENSE](.LICENSE) file.
