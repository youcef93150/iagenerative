Projet AISCA-Cinema
Auteurs : Anthony BOUCHER & Youcef DEROUICHE Projet : Agent Intelligent de Recommandation Cinématographique Module : IA Générative - EFREI 2025-2026 (Bloc 2)

Description
AISCA-Cinema est une application web qui recommande des films en analysant le sens de vos phrases (analyse sémantique) plutôt que de simples mots-clés. Elle utilise une architecture RAG (Retrieval-Augmented Generation) combinant :

SBERT (Sentence-BERT) : Pour trouver mathématiquement les films correspondant à votre description.

Google Gemini : Une IA générative pour expliquer les recommandations et créer un profil cinéphile personnalisé.

Installation et Lancement
Suivez ces étapes pour installer le projet sur votre machine.

1. Prérequis techniques
   Python installé (version 3.9 ou supérieure).

Une clé API Google Gemini (gratuite via Google AI Studio).

2. Installation
   Ouvrez un terminal dans le dossier du projet et exécutez les commandes suivantes :

Pour Windows :

Bash

python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
Pour Mac / Linux :

Bash

python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt 3. Configuration de la clé API
L'application a besoin de votre clé Google pour la partie générative.

Dans le dossier du projet, localisez le fichier .env.example.

Renommez ce fichier en .env.

Ouvrez-le avec un éditeur de texte et collez votre clé API à la place du texte existant : GEMINI_API_KEY=votre_cle_commencant_par_AIza...

4. Lancement de l'application
   Une fois l'installation terminée, lancez la commande suivante dans le terminal :

Bash

streamlit run app.py
L'application s'ouvrira automatiquement dans votre navigateur web par défaut.

Fonctionnement de l'application
L'application suit un processus en 4 étapes :

Acquisition : Vous remplissez un questionnaire hybride (texte libre + échelles de préférences).

Analyse (NLP) : Le moteur SBERT transforme votre texte en vecteurs et cherche les films les plus proches dans notre base de données de 260 films.

Scoring : Un algorithme classe les films selon une formule pondérée :

50% : Pertinence sémantique (votre texte).

30% : Vos genres préférés.

20% : L'ambiance (Mood) recherchée.

Génération (IA) : Google Gemini rédige une synthèse de votre profil et vous propose un plan de découverte basé sur les résultats.

Structure du projet
app.py : Point d'entrée de l'interface graphique.

data/ : Contient le fichier CSV des 260 films et le fichier de sauvegarde des réponses.

src/nlp_engine.py : Contient la logique d'analyse sémantique (SBERT).

src/genai_integration.py : Gère les appels à l'API Google Gemini.

src/scoring.py : Contient l'algorithme de calcul des scores.

src/cache_manager.py : Système de cache pour limiter les appels API et les coûts.

Dépannage
Si la commande streamlit n'est pas trouvée : Vérifiez que votre environnement virtuel (venv) est bien activé.

Si vous avez une erreur de clé API : Vérifiez que le fichier se nomme bien .env (et non .env.txt) et qu'il contient votre clé valide.
