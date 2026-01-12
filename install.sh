#!/bin/bash

# Script d'installation pour AISCA-Cinema
# EFREI - Projet IA Générative 2025-26

echo "🎬 Installation d'AISCA-Cinema"
echo "================================"
echo ""

# Vérifier Python
echo "🔍 Vérification de Python..."
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 n'est pas installé. Veuillez l'installer d'abord."
    exit 1
fi

python_version=$(python3 --version)
echo "✅ $python_version détecté"
echo ""

# Créer l'environnement virtuel
echo "📦 Création de l'environnement virtuel..."
python3 -m venv venv

# Activer l'environnement
echo "🔧 Activation de l'environnement virtuel..."
source venv/bin/activate

# Mettre à jour pip
echo "⬆️  Mise à jour de pip..."
pip install --upgrade pip

# Installer les dépendances
echo "📥 Installation des dépendances..."
pip install -r requirements.txt

echo ""
echo "✅ Installation terminée !"
echo ""
echo "📝 Prochaines étapes:"
echo "   1. Activez l'environnement: source venv/bin/activate"
echo "   2. Configurez votre clé API Gemini dans .env"
echo "   3. Lancez l'application: streamlit run app.py"
echo ""
echo "🎬 Bon développement !"
