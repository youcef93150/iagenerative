# 🚀 Guide de Démarrage Rapide - AISCA-Cinema

## Installation en 5 minutes

### 1. Prérequis
```bash
# Vérifier Python (3.9+)
python3 --version

# Vérifier pip
pip3 --version
```

### 2. Installation
```bash
cd /Users/youcef/Downloads/cinema-recommendation-agent

# Option A: Installation automatique
chmod +x install.sh
./install.sh

# Option B: Installation manuelle
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
pip install -r requirements.txt
```

### 3. Configuration de l'API Gemini
1. Obtenir une clé API gratuite : https://makersuite.google.com/app/apikey
2. Créer le fichier `.env` :
   ```bash
   cp .env.example .env
   ```
3. Éditer `.env` et ajouter votre clé :
   ```
   GEMINI_API_KEY=votre_clé_ici
   ```

### 4. Lancement
```bash
source venv/bin/activate  # Si pas déjà activé
streamlit run app.py
```

L'application s'ouvre automatiquement à : `http://localhost:8501`

---

## Utilisation

### Étape 1 : Questionnaire
1. Décrivez votre film idéal (texte libre, min. 20 caractères)
2. Évaluez vos préférences par genre (échelle 1-5)
3. Évaluez vos préférences d'ambiance (échelle 1-5)
4. Complétez les questions guidées (optionnel)

### Étape 2 : Analyse
Cliquez sur **"Analyser mes Préférences"**

L'application va :
- Encoder votre profil avec SBERT
- Calculer la similarité avec 55 films
- Générer vos Top 3 recommandations
- Créer votre profil cinéphile (via Gemini)
- Proposer un plan de découverte

### Étape 3 : Résultats
Explorez les 5 onglets :
- **Top 3 Films** : Vos recommandations détaillées
- **Visualisations** : Graphiques radars et scores
- **Profil Cinéphile** : Votre synthèse personnalisée
- **Plan de Découverte** : Films à découvrir
- **Statistiques** : Détails techniques

---

## Structure du Projet

```
cinema-recommendation-agent/
├── app.py                      # 🎯 Point d'entrée Streamlit
├── data/
│   └── films_referentiel.csv   # 📊 Base de 55 films
├── src/
│   ├── questionnaire.py        # EF1: Collecte des données
│   ├── nlp_engine.py          # EF2: Analyse SBERT
│   ├── scoring.py             # EF3: Système de scoring
│   ├── genai_integration.py   # EF4: IA générative
│   ├── visualization.py       # Graphiques
│   └── cache_manager.py       # Gestion cache API
└── tests/
    └── test_nlp_engine.py     # Tests unitaires
```

---

## Exigences Fonctionnelles Implémentées

### ✅ EF1 : Acquisition de la Donnée
- Questionnaire hybride (Likert + texte libre)
- Stockage JSON structuré

### ✅ EF2 : Moteur NLP Sémantique
- SBERT multilingue (coût zéro)
- Similarité cosinus
- 55 films répartis en 10 blocs de genres

### ✅ EF3 : Scoring et Recommandation
- Formule pondérée (α=0.5, β=0.3, γ=0.2)
- Top 3 recommandations

### ✅ EF4 : IA Générative (Gemini)
- Enrichissement conditionnel (si texte < 15 mots)
- Plan de découverte (1 appel API)
- Profil cinéphile (1 appel API)
- Cache automatique

---

## Commandes Utiles

### Lancer l'application
```bash
streamlit run app.py
```

### Lancer sur un port différent
```bash
streamlit run app.py --server.port 8502
```

### Exécuter les tests
```bash
python -m pytest tests/
```

### Vider le cache GenAI
```bash
rm -rf .cache/genai_cache.json
```

---

## Dépannage

### Erreur : "Module not found"
```bash
pip install -r requirements.txt
```

### Erreur : "API key invalid"
Vérifiez votre clé dans `.env` :
```bash
cat .env
```

### L'application ne démarre pas
```bash
# Vérifier que l'environnement est activé
which python  # Doit pointer vers venv/bin/python

# Réinstaller Streamlit
pip install --upgrade streamlit
```

### Erreur SBERT "Model not found"
```bash
# Le modèle se télécharge automatiquement au premier lancement
# Vérifier la connexion internet
```

---

## Support

- 📧 Email : votre.email@efrei.net
- 📚 Documentation complète : `README.md`
- 🐛 Issues : Créer une issue sur GitHub

---

**Bon développement ! 🎬**
