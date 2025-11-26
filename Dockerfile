FROM python:3.11.11-slim

WORKDIR /app

# Install uv
RUN pip install --no-cache-dir uv

# Copy dependency files
COPY pyproject.toml uv.lock ./

# Install dependencies using uv
RUN uv sync --frozen

# Copy application files
COPY main.py schemas.py sensors.json ./

# Expose the port
EXPOSE 4000

# Run the application
CMD ["uv", "run", "uvicorn", "main:app", "--host", "0.0.0.0", "--port", "4000"]