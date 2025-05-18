# Use a slim Python 3.9 base image for smaller size
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy project files (ensure pyproject.toml, uv.lock, main.py are included)
COPY . .

# Install uv and dependencies
RUN pip install --no-cache-dir uv && \
    uv sync --frozen

# Expose port 8000
EXPOSE 8000

# Run FastAPI in development mode to match local behavior
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]