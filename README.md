# 🎬 Agent de Recommandation Cinéma

**Projet EFREI - IA Générative 2025-26**

Un système intelligent qui recommande des films en fonction de vos goûts, basé sur SBERT et l'IA Gemini.

---

## C'est quoi ce projet ?

En gros, c'est une app qui pose des questions sur vos préférences ciné (genres, ambiances, ce que vous cherchez...) et qui utilise l'IA pour proposer 3 films qui devraient vraiment vous plaire. 

L'app analyse ce que vous dites avec du NLP (traitement du langage), compare ça avec une base de 260 films, et sort les meilleures recommandations avec des explications personnalisées générées par Gemini.

**Architecture RAG** : on récupère les films pertinents avec SBERT (partie Retrieval), puis on génère des textes personnalisés avec Gemini (partie Generation).

---

## Comment lancer l'app ?

### Installation rapide

```bash
# 1. Clonez le projet (ou téléchargez-le)
cd /Users/youcef/Downloads/cinema-recommendation-agent

# 2. Créez un environnement virtuel
python3 -m venv venv
source venv/bin/activate

# 3. Installez les dépendances
pip install -r requirements.txt

# 4. Configurez votre clé API Gemini
cp .env.example .env
# Éditez le fichier .env et mettez votre clé API (gratuite sur https://makersuite.google.com/app/apikey)

# 5. Lancez l'app
streamlit run app.py
```

L'app s'ouvre automatiquement sur `http://localhost:8501`

---

## Comment ça marche ?

### Le questionnaire
Vous remplissez un questionnaire avec :
- Une description libre de ce que vous cherchez (minimum 20 caractères)
- Vos préférences pour 10 genres de films (échelle de 1 à 5)
- Vos préférences pour 8 ambiances différentes (échelle de 1 à 5)
- Période préférée, réalisateurs favoris, films de référence...

### L'analyse sémantique
L'app utilise SBERT (un modèle NLP ultra performant) pour comprendre ce que vous voulez vraiment. Ça transforme votre texte en vecteurs et calcule la similarité avec les 260 films de la base.

### Le scoring
Chaque film reçoit un score basé sur :
- **50%** : similarité sémantique (ce que vous avez écrit)
- **30%** : vos préférences de genres
- **20%** : vos préférences d'ambiance

### Les recommandations
L'app sort les 3 meilleurs films avec :
- Des explications personnalisées (générées par Gemini)
- Des graphiques de vos préférences
- Un profil cinéphile personnalisé
- Des suggestions pour découvrir de nouveaux genres

---

## Technologies utilisées

- **Python 3.9+** : langage principal
- **Streamlit** : interface web interactive
- **SentenceTransformers** : embeddings SBERT pour l'analyse sémantique
- **Google Gemini** : IA générative pour les textes personnalisés
- **Plotly** : graphiques interactifs
- **Pandas** : manipulation des données

---

## Structure du projet

```
cinema-recommendation-agent/
├── app.py                      # App Streamlit principale
├── requirements.txt            # Dépendances Python
├── .env.example               # Template config API
├── data/
│   └── films_referentiel.csv  # Base de 260 films
└── src/
    ├── questionnaire.py       # Interface de questionnaire
    ├── nlp_engine.py          # Moteur SBERT
    ├── scoring.py             # Calcul des scores
    ├── genai_integration.py   # Intégration Gemini
    ├── visualization.py       # Graphiques
    └── cache_manager.py       # Gestion du cache API
```

---

## Fonctionnalités

- Questionnaire hybride (texte libre + échelles)
- Analyse sémantique avec SBERT (pas de coût API)
- Recommandation des 3 meilleurs films
- Graphiques interactifs (radar, barres...)
- Profil cinéphile personnalisé
- Plan de découverte pour explorer de nouveaux genres
- Cache intelligent pour limiter les appels API Gemini

---

## Quelques précisions techniques

**Pourquoi SBERT ?** Parce que c'est super efficace pour comprendre le sens des phrases en français, et ça tourne en local (pas de coût).

**Pourquoi Gemini ?** API gratuite, rapide, et ça génère du texte de qualité en français.

**Pourquoi Streamlit ?** Parce que c'est hyper simple pour faire une interface web sans se prendre la tête avec du HTML/CSS/JS.

**Le cache ?** Pour éviter de taper dans l'API Gemini à chaque fois (économie de quota gratuit).

---

## Si vous avez des problèmes

**L'app ne démarre pas ?**
```bash
streamlit run app.py --server.port 8502
```

**Erreur "Module not found" ?**
```bash
pip install -r requirements.txt
```



---

## Projet réalisé par

- Youcef & Anthony
- EFREI Paris 2025-26
- Module IA Générative




