# Multi-stage build with slim Python image for smaller final size
FROM python:3.11-slim as builder

# Set working directory
WORKDIR /app

# Install system dependencies for building Python packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements and install Python dependencies
COPY req.txt .
RUN pip install --user --no-cache-dir -r req.txt

# Final stage - lightweight runtime image
FROM python:3.11-slim

# Set environment variables (can be overridden at runtime)
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    PATH=/home/appuser/.local/bin:$PATH \
    IP_API_URL=http://ip-api.com/json \
    IPIFY_URL=https://api.ipify.org?format=json \
    DEBUG=False \
    PORT=8001 \
    LOG_LEVEL=INFO

# Create a non-root user for security
RUN groupadd -r appuser && useradd -r -g appuser appuser

# Set working directory
WORKDIR /app

# Copy Python dependencies from builder stage
COPY --from=builder --chown=appuser:appuser /root/.local /home/appuser/.local

# Copy application code
COPY --chown=appuser:appuser config.py .
COPY --chown=appuser:appuser main.py .
COPY --chown=appuser:appuser utils/ ./utils/

# Switch to non-root user
USER appuser

# Expose the Flask application port
EXPOSE 8001

# Health check (optional - uncomment if desired)
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
#    CMD python -c "import requests; requests.get('http://localhost:8001/get-location')" || exit 1

# Run the Flask application
CMD ["python", "main.py"]
