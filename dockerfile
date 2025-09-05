FROM ghcr.io/astral-sh/uv:bookworm

WORKDIR /app

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies
RUN uv sync --frozen
#
# Copy application
COPY . .

EXPOSE 8000

# Run with uv
CMD ["uv", "run", "python", "manage.py", "runserver", "0.0.0.0:8000"]
