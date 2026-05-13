#!/bin/bash

# Arrête le script au moindre échec (Best practice DevOps)
set -e

echo "--- 🚀 Démarrage du déploiement local ---"

# 1. Gestion de l'environnement virtuel
if [ ! -d "venv" ]; then
    echo "📦 Création de l'environnement virtuel..."
    python -m venv venv
fi

# 2. Installation/Mise à jour des dépendances
echo "📥 Installation des dépendances..."
./venv/Scripts/pip install -r requirements.txt

# 3. Exécution des tests
echo "🧪 Exécution des tests unitaires..."
./venv/Scripts/python -m pytest

# 4. Lancement de l'application
echo "✅ Tests réussis ! Lancement de l'API..."
./venv/Scripts/python src/app.py
