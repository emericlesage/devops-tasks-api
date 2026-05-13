FROM python:3.11-slim AS builder

WORKDIR /build

# Copier uniquement requirements pour cache optimal
COPY requirements.txt .

# Installer dépendances dans user site-packages
RUN pip install --user --no-cache-dir --no-warn-script-location \
    -r requirements.txt

FROM python:3.11-slim

WORKDIR /app

# Créer user non-root
RUN useradd -m -u 1000 appuser && \
    chown -R appuser:appuser /app

# Copier les dépendances depuis builder
COPY --from=builder /root/.local /home/appuser/.local

# Copier le code applicatif
COPY --chown=appuser:appuser app/ /app/app/

# Variables d'environnement
ENV PATH=/home/appuser/.local/bin:$PATH \
    PYTHONUNBUFFERED=1 \
    FLASK_APP=app

#metadata
EXPOSE 5000

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD python -c "import requests; requests.get('http://localhost:5000/health', timeout=5)" || exit 1

# Switcher vers user non-root
USER appuser

# Commande de démarrage
CMD ["python", "-m", "flask", "run", "--host=0.0.0.0"]
