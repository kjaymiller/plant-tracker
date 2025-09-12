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

### Using UV (Recommended)

1. Clone the repository:
   ```bash
   gh repo clone kjaymiller/plant-tracker
   cd plant-tracker
   ```

2. Install dependencies:
   ```bash
   uv sync
   ```

3. Set up environment variables (create `.env` file):
   ```
   DATABASE_CONNECTION_STRING=postgresql://username:password@localhost:5432/plant_tracker
   ```

### Database Schema Restoration (First Time Setup)

If you're setting up the project for the first time you can load the schema backup. 
**DO THIS BEFORE RUNNING MIGRATIONS:**

   ```bash
   # Wait a moment for PostgreSQL to start, then restore
   psql $DATABASE_CONNECTION_STRING -f schema_backup.sql
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
