FROM python:3.12.7-slim-bookworm

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Install dependencies first so code-only changes can reuse this layer.
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Run the service as an unprivileged user.
RUN useradd --create-home --uid 10001 appuser
COPY --chown=appuser:appuser app.py .

USER 10001

# Flask/Gunicorn listens on this container port.
EXPOSE 5000

CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--workers", "2", "app:app"]
