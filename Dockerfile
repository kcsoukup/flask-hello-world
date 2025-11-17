FROM python:3.11-slim

# Create non-root user
RUN useradd -m -u 1000 appuser

WORKDIR /app

# Copy requirements and change ownership
COPY --chown=appuser:appuser requirements.txt .

# Switch to non-root user before installing dependencies
USER appuser

# Install dependencies as non-root user
RUN pip install --no-cache-dir --user -r requirements.txt

# Copy application code
COPY --chown=appuser:appuser . .

# Ensure user's local bin is in PATH for pip-installed packages
ENV PATH=/home/appuser/.local/bin:$PATH

# Document the port
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "4", "--worker-class", "gevent", "--worker-connections", "1000", "app:app"]
