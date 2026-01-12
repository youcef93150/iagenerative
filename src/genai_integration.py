"""
Intégration de l'IA Générative (Gemini)
EF4: Augmentation par GenAI (Stratégique et Limitée)

Contraintes obligatoires respectées:
- Appels API strictement limités
- Un seul appel pour le plan de découverte
- Un seul appel pour la bio/synthèse
- Caching automatique
- Enrichissement conditionnel uniquement

Architecture RAG:
- Retrieval: Fait par le moteur NLP
- Augmented Context: Construction du contexte enrichi ici
- Generation: Production via Gemini
"""

import os
from typing import List, Dict, Optional
import logging
import google.generativeai as genai
from dotenv import load_dotenv
from src.cache_manager import CacheManager

# Charger les variables d'environnement
load_dotenv()

logger = logging.getLogger(__name__)


class GenAIIntegration:
    """
    Intégration de l'IA générative Gemini (EF4)
    
    Respecte l'architecture RAG et toutes les contraintes de limitation des appels.
    """
    
    def __init__(
        self,
        api_key: Optional[str] = None,
        model_name: str = "gemini-2.0-flash-exp",
        cache_enabled: bool = True,
        max_cache_size: int = 100
    ):
        """
        Initialise l'intégration Gemini
        
        Args:
            api_key: Clé API Gemini (ou depuis .env)
            model_name: Nom du modèle Gemini à utiliser
            cache_enabled: Activer le caching
            max_cache_size: Taille max du cache
        """
        # Récupérer la clé API
        self.api_key = api_key or os.getenv('GEMINI_API_KEY')
        
        if not self.api_key:
            raise ValueError(
                "❌ Clé API Gemini manquante. "
                "Définissez GEMINI_API_KEY dans .env ou passez-la en paramètre."
            )
        
        # Configurer Gemini
        genai.configure(api_key=self.api_key)
        self.model_name = model_name
        self.model = genai.GenerativeModel(model_name)
        
        # Initialiser le cache (CONTRAINTE OBLIGATOIRE)
        self.cache = CacheManager(
            cache_dir=".cache",
            max_size=max_cache_size,
            enabled=cache_enabled
        )
        
        # Compteur d'appels (pour monitoring)
        self.api_calls_count = 0
        
        logger.info(f"✅ GenAI initialisé - Modèle: {model_name}, Cache: {cache_enabled}")
    
    def _call_gemini(self, prompt: str, use_cache: bool = True) -> str:
        """
        Appelle l'API Gemini avec gestion du cache
        
        Args:
            prompt: Le prompt à envoyer
            use_cache: Utiliser le cache ou non
            
        Returns:
            Réponse générée
        """
        # Vérifier le cache d'abord
        if use_cache:
            cached_response = self.cache.get(prompt, model=self.model_name)
            if cached_response:
                logger.info("✅ Réponse récupérée du cache (0 appel API)")
                return cached_response
        
        # Appel API
        try:
            logger.info(f"📡 Appel API Gemini #{self.api_calls_count + 1}")
            response = self.model.generate_content(prompt)
            result = response.text
            
            # Mettre en cache
            if use_cache:
                self.cache.set(prompt, result, model=self.model_name)
            
            self.api_calls_count += 1
            logger.info(f"✅ Réponse générée (longueur: {len(result)} caractères)")
            
            return result
            
        except Exception as e:
            logger.error(f"❌ Erreur lors de l'appel API Gemini: {e}")
            return f"[Erreur de génération: {str(e)}]"
    
    def enrich_short_text(self, text: str, min_words: int = 15) -> tuple[str, bool]:
        """
        EF4.1: Enrichissement conditionnel de texte court (OPTIONNEL)
        
        N'appelle l'API QUE si le texte est trop court.
        
        Args:
            text: Texte à éventuellement enrichir
            min_words: Nombre minimum de mots
            
        Returns:
            (texte_enrichi, was_enriched): Texte final et booléen d'enrichissement
        """
        word_count = len(text.split())
        
        # Si le texte est suffisant, ne pas enrichir
        if word_count >= min_words:
            logger.info(f"✅ Texte suffisant ({word_count} mots) - Pas d'enrichissement")
            return text, False
        
        logger.info(f"⚠️ Texte court ({word_count} mots) - Enrichissement via GenAI")
        
        prompt = f"""Tu es un assistant qui enrichit des descriptions de préférences cinématographiques.

Description courte de l'utilisateur : "{text}"

Tâche : Enrichis cette description en ajoutant du contexte technique et des détails sur :
- Les thèmes cinématographiques possibles
- L'atmosphère recherchée
- Le style narratif qui pourrait correspondre

Règles :
- Reste fidèle à l'intention originale
- Ajoute 2-3 phrases maximum
- Utilise un ton naturel
- Ne change pas les préférences exprimées, ajoute seulement du contexte

Description enrichie :"""
        
        enriched = self._call_gemini(prompt, use_cache=True)
        
        # Combiner le texte original avec l'enrichissement
        final_text = f"{text}\n\n{enriched.strip()}"
        
        logger.info(f"✅ Texte enrichi ({len(final_text.split())} mots)")
        
        return final_text, True
    
    def generate_discovery_plan(
        self,
        weak_genres: List[str],
        recommendations: List[Dict],
        user_profile_summary: str
    ) -> str:
        """
        EF4.2: Génération du Plan de Découverte (UN SEUL APPEL API)
        
        Équivalent AISCA: Plan de progression personnalisé
        
        Args:
            weak_genres: Genres faiblement couverts (à explorer)
            recommendations: Top 3 films recommandés
            user_profile_summary: Résumé du profil utilisateur
            
        Returns:
            Plan de découverte personnalisé
        """
        logger.info("🎨 Génération du plan de découverte (1 appel API)")
        
        # Construction du contexte enrichi (AUGMENTED CONTEXT - RAG)
        reco_text = "\n".join([
            f"- {r['titre']} ({r['annee']}) de {r['realisateur']} - Score: {r['score_final']:.2f}"
            for r in recommendations[:3]
        ])
        
        weak_genres_text = ", ".join(weak_genres[:5]) if weak_genres else "Aucun"
        
        prompt = f"""Tu es un conseiller cinématographique expert qui crée des plans de découverte personnalisés.

PROFIL UTILISATEUR :
{user_profile_summary}

FILMS RECOMMANDÉS (Top 3) :
{reco_text}

GENRES À EXPLORER (faible affinité actuelle) :
{weak_genres_text}

TÂCHE : Crée un plan de découverte cinématographique personnalisé incluant :

1. **Prochaines Étapes** : 3-4 films à découvrir en priorité (en dehors du top 3) pour enrichir le profil
2. **Genres à Explorer** : Pourquoi découvrir les genres faiblement couverts et films recommandés par genre
3. **Parcours Thématique** : Une progression logique (ex: du plus accessible au plus expérimental)

Ton : Enthousiaste, pédagogique, personnalisé
Format : Markdown avec sections claires
Longueur : 300-400 mots maximum

Plan de Découverte :"""
        
        plan = self._call_gemini(prompt, use_cache=True)
        
        logger.info("✅ Plan de découverte généré")
        
        return plan.strip()
    
    def generate_cinephile_profile(
        self,
        recommendations: List[Dict],
        genre_weights: Dict[str, float],
        mood_weights: Dict[str, float],
        coverage_score: float
    ) -> str:
        """
        EF4.3: Synthèse de Profil Cinéphile (UN SEUL APPEL API)
        
        Équivalent AISCA: Bio professionnelle (Executive Summary)
        
        Args:
            recommendations: Top 3 films
            genre_weights: Poids des genres préférés
            mood_weights: Poids des moods préférés
            coverage_score: Score de couverture global
            
        Returns:
            Profil cinéphile personnalisé
        """
        logger.info("🎭 Génération du profil cinéphile (1 appel API)")
        
        # Identifier les genres préférés (score > 0.7)
        top_genres = [g for g, w in sorted(genre_weights.items(), key=lambda x: x[1], reverse=True) if w > 0.7][:3]
        
        # Identifier les moods préférés
        top_moods = [m for m, w in sorted(mood_weights.items(), key=lambda x: x[1], reverse=True) if w > 0.7][:3]
        
        # Films recommandés
        reco_titles = [f"{r['titre']} ({r['annee']})" for r in recommendations[:3]]
        
        prompt = f"""Tu es un expert en profils cinématographiques qui rédige des synthèses personnalisées.

DONNÉES DU PROFIL :
- Genres préférés : {', '.join(top_genres) if top_genres else 'Varié'}
- Ambiances recherchées : {', '.join(top_moods) if top_moods else 'Varié'}
- Films recommandés : {', '.join(reco_titles)}
- Score d'affinité global : {coverage_score:.2f}/1.00

TÂCHE : Rédige un profil cinéphile personnalisé (style executive summary) qui :

1. Résume les goûts cinématographiques de la personne
2. Identifie sa "signature" de cinéphile (qu'est-ce qui caractérise ses choix ?)
3. Mentionne les réalisateurs ou mouvements qui pourraient l'intéresser
4. Termine par une phrase accrocheuse qui capture son essence de spectateur

Ton : Professionnel mais chaleureux, précis, valorisant
Format : Un seul paragraphe fluide
Longueur : 150-200 mots maximum

Profil Cinéphile :"""
        
        profile = self._call_gemini(prompt, use_cache=True)
        
        logger.info("✅ Profil cinéphile généré")
        
        return profile.strip()
    
    def generate_film_justification(
        self,
        film: Dict,
        user_description: str,
        score_components: Dict[str, float]
    ) -> str:
        """
        Génère une justification personnalisée pour une recommandation
        
        Args:
            film: Dictionnaire du film recommandé
            user_description: Description originale de l'utilisateur
            score_components: Composantes du score (sémantique, genre, mood)
            
        Returns:
            Justification de la recommandation
        """
        prompt = f"""Explique en 2-3 phrases pourquoi le film "{film['titre']}" ({film['annee']}) 
correspond aux préférences de l'utilisateur.

Préférences utilisateur : {user_description[:200]}...

Description du film : {film['description'][:300]}...

Scores :
- Similarité sémantique : {score_components['sémantique']:.2f}
- Affinité genre : {score_components['genre']:.2f}
- Affinité mood : {score_components['mood']:.2f}

Justification concise et personnalisée :"""
        
        justification = self._call_gemini(prompt, use_cache=True)
        
        return justification.strip()
    
    def get_api_stats(self) -> Dict:
        """
        Retourne les statistiques d'utilisation de l'API
        
        Returns:
            Dictionnaire avec les stats
        """
        cache_stats = self.cache.get_stats()
        
        return {
            "api_calls_count": self.api_calls_count,
            "cache_stats": cache_stats,
            "model_name": self.model_name
        }
