# 🎬 Agent Intelligent de Recommandation Cinématographique (AISCA-Cinema)

## 📋 Description du Projet

**Système de recommandation de films basé sur l'analyse sémantique avec SBERT et l'IA générative (Gemini).**

Adaptation de l'architecture AISCA (Agent Intelligent Sémantique et Génératif pour la Cartographie des Compétences) appliquée au domaine cinématographique.

**Projet EFREI - IA Générative 2025-26 - RNCP40875 Bloc 2**

---

## 🎯 Objectifs du Projet

### Objectif Principal
Développer un agent RAG (Retrieval-Augmented Generation) capable de :
- Analyser sémantiquement les préférences cinématographiques d'un utilisateur
- Recommander les 3 films les plus pertinents via similarité cosinus (SBERT)
- Générer des justifications personnalisées via IA générative (Gemini)
- Proposer un profil cinéphile et un plan de découverte

### Architecture RAG Appliquée
1. **Retrieval** : Extraction des films pertinents via embeddings SBERT
2. **Augmented Context** : Construction d'un contexte enrichi avec scores sémantiques
3. **Generation** : Production de recommandations personnalisées via Gemini

---

## 🏗️ Architecture Technique

```
cinema-recommendation-agent/
├── README.md                       # Documentation
├── requirements.txt                # Dependances Python
├── .env.example                    # Template configuration API
├── .gitignore                      # Fichiers a ignorer
├── app.py                          # Interface Streamlit principale
├── data/
│   └── films_referentiel.csv       # Base de donnees 260 films reels
├── src/
│   ├── __init__.py
│   ├── questionnaire.py            # Questionnaire hybride
│   ├── nlp_engine.py               # Moteur NLP SBERT
│   ├── scoring.py                  # Systeme de scoring
│   ├── genai_integration.py        # Integration Gemini AI
│   ├── visualization.py            # Graphiques et visualisations
│   └── cache_manager.py            # Cache pour limiter couts API
└── .cache/                         # Cache local GenAI
```

---

## 🚀 Installation et Lancement

### Prérequis
- Python 3.9+
- pip
- Compte Google AI (pour Gemini API - gratuit)

### 1. Cloner le projet
```bash
cd /Users/youcef/Downloads/cinema-recommendation-agent
```

### 2. Créer un environnement virtuel
```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
```

### 3. Installer les dépendances
```bash
pip install -r requirements.txt
```

### 4. Configuration de l'API Gemini
1. Obtenir une clé API gratuite : https://makersuite.google.com/app/apikey
2. Copier `.env.example` vers `.env` :
   ```bash
   cp .env.example .env
   ```
3. Éditer `.env` et ajouter votre clé :
   ```
   GEMINI_API_KEY=votre_clé_api_ici
   ```

### 5. Lancer l'application
```bash
streamlit run app.py
```

L'application s'ouvre automatiquement à : `http://localhost:8501`

---

## 📊 Exigences Fonctionnelles Implémentées

### ✅ EF1 : Acquisition de la Donnée

**EF1.1 - Questionnaire Hybride**
- ✅ Description libre du film souhaité (texte libre, min. 20 caractères)
- ✅ Auto-déclaration par genre (Likert 1-5) : 10 genres
- ✅ Auto-déclaration d'ambiance/mood (Likert 1-5) : 8 moods
- ✅ Questions guidées : période, réalisateurs favoris, films références
- ✅ Éléments à éviter (optionnel)

**EF1.2 - Structuration**
- ✅ Stockage JSON structuré (`data/user_responses.json`)
- ✅ Format timestamp pour traçabilité

### ✅ EF2 : Moteur NLP Sémantique (Coût Zéro)

**EF2.1 - Référentiel Cinématographique**
- ✅ 55 films structurés en 10 blocs de genres
- ✅ Catégories : Science-Fiction, Drame, Fantasy, Animation, Thriller, Comédie, Horreur, Romance, Action, Biopic
- ✅ Champs : Description narrative, Keywords, Mood, Genre, Réalisateur, Année

**EF2.2 - Modélisation Sémantique**
- ✅ SBERT : `paraphrase-multilingual-MiniLM-L12-v2` (support français)
- ✅ Embeddings contextuels locaux (pas d'appel API)
- ✅ Cache des embeddings pour performance

**EF2.3 - Mesure de Similarité**
- ✅ Calcul de similarité cosinus
- ✅ Scores normalisés [0, 1]

### ✅ EF3 : Scoring et Recommandation

**EF3.1 - Formule de Score Pondérée**
```
Score_Final = α × Score_Sémantique + β × Score_Genres + γ × Score_Moods

Avec pondérations ajustables :
- α = 0.50 (priorité à la description libre)
- β = 0.30 (genres déclarés)
- γ = 0.20 (ambiance/mood)
```

**EF3.2 - Recommandation Top 3**
- ✅ Classement des films par score décroissant
- ✅ Affichage des 3 meilleures recommandations
- ✅ Détails complets pour chaque film

### ✅ EF4 : Augmentation par GenAI (Gemini - Limitée)

**EF4.1 - Augmentation de saisie (OPTIONNEL)**
- ✅ Enrichissement automatique si description < 15 mots
- ✅ Appel conditionnel uniquement
- ✅ Cache pour éviter appels répétés

**EF4.2 - Génération du Plan de Découverte**
- ✅ Identification des genres/moods faiblement couverts
- ✅ Suggestions de films à découvrir
- ✅ **UN SEUL appel API** pour tout le plan

**EF4.3 - Synthèse de Profil Cinéphile**
- ✅ Bio personnalisée style "executive summary"
- ✅ **UN SEUL appel API**
- ✅ Basée sur les recommandations et préférences

**Contraintes GenAI Respectées**
- ✅ Appels API strictement limités (3 max par session)
- ✅ Caching automatique (fichier `.cache/genai_cache.json`)
- ✅ Gestion du quota Free Tier

---

## 🎨 Fonctionnalités Interface

### Visualisations Interactives
1. **Graphique Radar** : Préférences par genre (10 axes)
2. **Graphique Radar** : Ambiance/Mood (8 axes)
3. **Barres** : Scores de similarité Top 3
4. **Cartes de Films** : Détails visuels des recommandations
5. **Distribution des Genres** : Affinité sémantique globale

### Sections de l'Application
1. 🎬 **Questionnaire** : Collecte des préférences
2. 🔍 **Analyse Sémantique** : Traitement SBERT
3. 🎯 **Recommandations** : Top 3 + justifications
4. 📊 **Visualisations** : Graphiques interactifs
5. 🎭 **Profil Cinéphile** : Bio personnalisée
6. 📚 **Plan de Découverte** : Suggestions d'exploration

---

## 🧪 Technologies Utilisées

| Technologie | Usage | Version |
|------------|-------|---------|
| **Python** | Langage principal | 3.9+ |
| **Streamlit** | Interface web | 1.31.0 |
| **SentenceTransformers** | Embeddings SBERT | 2.3.1 |
| **Google Gemini** | IA générative | API v0.3.2 |
| **Pandas** | Manipulation données | 2.2.0 |
| **Plotly** | Visualisations | 5.18.0 |
| **scikit-learn** | Similarité cosinus | 1.4.0 |
| **python-dotenv** | Gestion .env | 1.0.1 |

---

## 📐 Formule de Scoring Détaillée

### 1. Score Sémantique (SBERT)
```python
Similarité_Cosinus(Embedding_User, Embedding_Film) → [0, 1]
```

### 2. Score Genres
```python
Score_Genre = moyenne([Préférence_Likert(g) / 5 for g in genres_film])
```

### 3. Score Moods
```python
Score_Mood = moyenne([Préférence_Likert(m) / 5 for m in moods_film])
```

### 4. Score Final Pondéré
```python
Score_Final = 0.50 × Sim_Cosinus + 0.30 × Score_Genre + 0.20 × Score_Mood
```

---

## 📂 Référentiel de Films

### Structure du Référentiel
| Colonne | Description | Exemple |
|---------|-------------|---------|
| FilmID | Identifiant unique | F001 |
| BlockID | Bloc de genre | B01 |
| Categorie | Genre principal | Science-Fiction |
| Film | Titre du film | Inception |
| Realisateur | Réalisateur | Christopher Nolan |
| Annee | Année de sortie | 2010 |
| Description | Synopsis narratif riche | "Un voleur qui s'introduit..." |
| Keywords | Mots-clés sémantiques | "rêves, réalité, heist" |
| Mood | Ambiance/Atmosphère | "mind-bending, intense" |
| Genre | Genres (multi) | "Science-Fiction, Thriller" |

### Statistiques
- **Total films** : 55
- **Blocs de genres** : 10
- **Période couverte** : 1980-2024
- **Réalisateurs** : 40+

---

## 🔬 Compétences RNCP40875 - Bloc 2 Validées

### Compétences Principales
- ✅ Collecter et préparer données non structurées (texte libre)
- ✅ Concevoir et implémenter modèles NLP (SBERT)
- ✅ Prototyper solution IA (RAG, embeddings, GenAI)
- ✅ Développer pipeline data bout en bout
- ✅ Optimiser coûts (cache, API limitée)
- ✅ Documenter solution technique

### Compétences Techniques Mobilisées
- **NLP** : Embeddings contextuels, similarité cosinus
- **IA Générative** : Prompt engineering, RAG, caching
- **Data Engineering** : Pipeline structuré, versioning Git
- **Software** : Interface Streamlit, visualisations
- **Professionnelles** : MVP, documentation, présentation

---

## 🎓 Justification des Choix Techniques

### Pourquoi SBERT ?
- ✅ Embeddings contextuels multilingues (français)
- ✅ Performance supérieure à Word2Vec/GloVe
- ✅ Local (coût zéro)
- ✅ Optimisé pour phrases/paragraphes

### Pourquoi Gemini ?
- ✅ API gratuite (Free Tier généreux)
- ✅ Rapide (Flash 2.0)
- ✅ Support français natif
- ✅ Bonne qualité de génération

### Pourquoi Streamlit ?
- ✅ Prototypage rapide
- ✅ Interface réactive native
- ✅ Pas de frontend à coder
- ✅ Déploiement facile

### Pourquoi Architecture RAG ?
- ✅ Réduit hallucinations GenAI
- ✅ Contrôle total sur recommandations
- ✅ Approche industrielle standard
- ✅ Optimise coûts API

---

## 📝 Livrables du Projet

### À soumettre sur Moodle + GitHub
1. ✅ Code source complet + documentation
2. ✅ Référentiel de films (55+)
3. ✅ README.md technique
4. ✅ Présentation PowerPoint
5. ✅ Démo vidéo (optionnel)

### Présentation Finale
- 📅 Date : Dernière séance du module
- ⏱️ Durée : 15-20 minutes
- 👥 Format : Tous les membres participent
- 📊 Contenu : Démo live + explication technique

---

## 🤝 Équipe

- **Étudiant 1** : [Votre Nom]
- **Étudiant 2** : [Nom Binôme]

---

## 📄 Licence

Projet académique - EFREI Paris 2025-26  
Module : IA Générative - Data Engineering & AI

---

## 🆘 Dépannage

### Erreur : "Module not found"
```bash
pip install -r requirements.txt
```

### Erreur : "API key invalid"
Vérifiez que votre clé Gemini est correcte dans `.env`

### L'application ne démarre pas
```bash
streamlit run app.py --server.port 8502
```

### Cache trop volumineux
```python
# Dans l'app, section admin :
st.button("Vider le cache GenAI")
```

---

## 📚 Ressources

- [Documentation Streamlit](https://docs.streamlit.io/)
- [SentenceTransformers](https://www.sbert.net/)
- [Google Gemini API](https://ai.google.dev/)
- [Similarité Cosinus](https://en.wikipedia.org/wiki/Cosine_similarity)

---

**🎬 Bon développement ! GOOD LUCK!**
