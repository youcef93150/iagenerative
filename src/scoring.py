"""
Système de Scoring et Recommandation
EF3: Système de Scoring et Recommandation

Implémente la formule de score pondérée combinant:
- Score sémantique (SBERT similarité cosinus)
- Score de genres (préférences Likert)
- Score de moods (préférences Likert)

Équivalent AISCA: calcul du score de couverture des compétences
"""

import numpy as np
import pandas as pd
from typing import List, Dict, Tuple
import logging

logger = logging.getLogger(__name__)


class ScoringSystem:
    """
    Système de scoring pour la recommandation de films (EF3)
    
    Adapte la formule de scoring d'AISCA au domaine cinématographique.
    """
    
    def __init__(
        self,
        alpha: float = 0.50,  # Poids de la similarité sémantique
        beta: float = 0.30,   # Poids des préférences de genre
        gamma: float = 0.20   # Poids des préférences de mood
    ):
        """
        Initialise le système de scoring avec les pondérations (EF3.1)
        
        Formule (équivalent AISCA):
        Score_Final = α × Score_Sémantique + β × Score_Genres + γ × Score_Moods
        
        Args:
            alpha: Poids pour la similarité sémantique (description libre)
            beta: Poids pour les préférences de genre (Likert)
            gamma: Poids pour les préférences de mood (Likert)
        """
        # Vérifier que les poids somment à 1.0
        total_weight = alpha + beta + gamma
        if not np.isclose(total_weight, 1.0):
            logger.warning(f"⚠️ Les poids ne somment pas à 1.0 ({total_weight}). Normalisation automatique.")
            alpha = alpha / total_weight
            beta = beta / total_weight
            gamma = gamma / total_weight
        
        self.alpha = alpha
        self.beta = beta
        self.gamma = gamma
        
        logger.info(f"✅ ScoringSystem initialisé - α={alpha:.2f}, β={beta:.2f}, γ={gamma:.2f}")
    
    def calculate_genre_score(
        self,
        film_genres: str,
        user_genre_weights: Dict[str, float]
    ) -> float:
        """
        Calcule le score basé sur les préférences de genre
        
        Args:
            film_genres: Genres du film (ex: "Science-Fiction, Thriller")
            user_genre_weights: Poids utilisateur par genre {genre: poids [0,1]}
            
        Returns:
            Score de genre normalisé [0, 1]
        """
        # Parser les genres du film
        film_genre_list = [g.strip() for g in film_genres.split()]
        
        # Calculer le score moyen pour les genres du film
        scores = []
        for genre in film_genre_list:
            # Chercher le genre dans les préférences utilisateur
            for user_genre, weight in user_genre_weights.items():
                if genre in user_genre or user_genre in genre:
                    scores.append(weight)
                    break
        
        # Si aucun match, score par défaut de 0.5 (neutre)
        if not scores:
            return 0.5
        
        # Retourner la moyenne des scores
        return float(np.mean(scores))
    
    def calculate_mood_score(
        self,
        film_mood: str,
        user_mood_weights: Dict[str, float]
    ) -> float:
        """
        Calcule le score basé sur les préférences de mood/ambiance
        
        Args:
            film_mood: Mood du film (ex: "sombre, intense")
            user_mood_weights: Poids utilisateur par mood {mood: poids [0,1]}
            
        Returns:
            Score de mood normalisé [0, 1]
        """
        # Parser les moods du film
        film_mood_list = [m.strip().lower() for m in film_mood.split()]
        
        # Calculer le score moyen pour les moods du film
        scores = []
        for mood in film_mood_list:
            # Chercher des correspondances dans les préférences utilisateur
            for user_mood, weight in user_mood_weights.items():
                user_mood_lower = user_mood.lower()
                # Match si le mood est dans la description ou vice-versa
                if mood in user_mood_lower or any(word in mood for word in user_mood_lower.split('/')):
                    scores.append(weight)
                    break
        
        # Si aucun match, score par défaut de 0.5 (neutre)
        if not scores:
            return 0.5
        
        # Retourner la moyenne des scores
        return float(np.mean(scores))
    
    def calculate_final_score(
        self,
        semantic_similarity: float,
        genre_score: float,
        mood_score: float
    ) -> float:
        """
        Calcule le score final pondéré (EF3.1 - Formule de Score)
        
        Formule:
        Score_Final = α × Sim_Sémantique + β × Score_Genre + γ × Score_Mood
        
        Args:
            semantic_similarity: Score de similarité cosinus SBERT [0, 1]
            genre_score: Score basé sur les genres [0, 1]
            mood_score: Score basé sur les moods [0, 1]
            
        Returns:
            Score final normalisé [0, 1]
        """
        final_score = (
            self.alpha * semantic_similarity +
            self.beta * genre_score +
            self.gamma * mood_score
        )
        
        # Assurer que le score reste dans [0, 1]
        final_score = np.clip(final_score, 0.0, 1.0)
        
        return float(final_score)
    
    def rank_films(
        self,
        recommendations: List[Dict],
        semantic_similarities: np.ndarray,
        user_genre_weights: Dict[str, float],
        user_mood_weights: Dict[str, float],
        referentiel: pd.DataFrame
    ) -> List[Dict]:
        """
        Calcule les scores finaux et reclasse les recommandations
        
        Args:
            recommendations: Liste des recommandations initiales (basées sur SBERT uniquement)
            semantic_similarities: Array complet des similarités sémantiques
            user_genre_weights: Poids utilisateur pour les genres
            user_mood_weights: Poids utilisateur pour les moods
            referentiel: DataFrame du référentiel de films
            
        Returns:
            Liste des recommandations enrichies et reclassées
        """
        logger.info("🔄 Calcul des scores finaux pondérés...")
        
        enriched_recs = []
        
        for rec in recommendations:
            # Récupérer les données du film
            film_genres = rec['genre']
            film_mood = rec['mood']
            semantic_sim = rec['score_similarite']
            
            # Calculer les composantes du score
            genre_score = self.calculate_genre_score(film_genres, user_genre_weights)
            mood_score = self.calculate_mood_score(film_mood, user_mood_weights)
            
            # Calculer le score final
            final_score = self.calculate_final_score(
                semantic_similarity=semantic_sim,
                genre_score=genre_score,
                mood_score=mood_score
            )
            
            # Enrichir la recommandation
            enriched_rec = rec.copy()
            enriched_rec.update({
                'score_genre': genre_score,
                'score_mood': mood_score,
                'score_final': final_score,
                'composantes': {
                    'sémantique': semantic_sim,
                    'genre': genre_score,
                    'mood': mood_score
                }
            })
            
            enriched_recs.append(enriched_rec)
        
        # Reclasser par score final décroissant
        enriched_recs.sort(key=lambda x: x['score_final'], reverse=True)
        
        # Mettre à jour les rangs
        for idx, rec in enumerate(enriched_recs):
            rec['rang'] = idx + 1
        
        logger.info(f"✅ Scores calculés et films reclassés")
        top_scores = [f"{r['score_final']:.3f}" for r in enriched_recs[:3]]
        logger.info(f"🏆 Top 3 scores finaux: {top_scores}")
        
        return enriched_recs
    
    def get_top_recommendations(
        self,
        ranked_films: List[Dict],
        top_n: int = 3
    ) -> List[Dict]:
        """
        Retourne les top N recommandations (EF3.2)
        
        Args:
            ranked_films: Liste des films classés
            top_n: Nombre de recommandations à retourner (défaut: 3)
            
        Returns:
            Top N films recommandés
        """
        return ranked_films[:top_n]
    
    def calculate_coverage_score(
        self,
        semantic_similarities: np.ndarray,
        user_genre_weights: Dict[str, float],
        user_mood_weights: Dict[str, float],
        referentiel: pd.DataFrame
    ) -> float:
        """
        Calcule un score de couverture global du profil utilisateur
        
        Équivalent AISCA: Coverage Score des compétences
        
        Args:
            semantic_similarities: Toutes les similarités sémantiques
            user_genre_weights: Poids des genres
            user_mood_weights: Poids des moods
            referentiel: Référentiel de films
            
        Returns:
            Score de couverture global [0, 1]
        """
        # Prendre les top 10 films pour le calcul de couverture
        top_10_indices = np.argsort(semantic_similarities)[::-1][:10]
        
        scores = []
        for idx in top_10_indices:
            film = referentiel.iloc[idx]
            genre_score = self.calculate_genre_score(film['Genre'], user_genre_weights)
            mood_score = self.calculate_mood_score(film['Mood'], user_mood_weights)
            
            final_score = self.calculate_final_score(
                semantic_similarity=semantic_similarities[idx],
                genre_score=genre_score,
                mood_score=mood_score
            )
            scores.append(final_score)
        
        # Moyenne pondérée (plus de poids aux premiers)
        weights = np.array([1.0 / (i + 1) for i in range(len(scores))])
        weights = weights / weights.sum()
        
        coverage_score = float(np.average(scores, weights=weights))
        
        logger.info(f"📊 Score de couverture global: {coverage_score:.3f}")
        
        return coverage_score
    
    def identify_weak_genres(
        self,
        semantic_similarities: np.ndarray,
        referentiel: pd.DataFrame,
        threshold: float = 0.4
    ) -> List[str]:
        """
        Identifie les genres faiblement couverts par le profil utilisateur
        
        Équivalent AISCA: compétences à développer (gaps)
        
        Args:
            semantic_similarities: Array des similarités
            referentiel: Référentiel de films
            threshold: Seuil de similarité faible
            
        Returns:
            Liste des genres à explorer
        """
        genre_avg_scores = {}
        
        for genre in referentiel['Categorie'].unique():
            genre_mask = referentiel['Categorie'] == genre
            genre_sims = semantic_similarities[genre_mask]
            
            if len(genre_sims) > 0:
                genre_avg_scores[genre] = float(genre_sims.mean())
        
        # Identifier les genres sous le seuil
        weak_genres = [
            genre for genre, score in genre_avg_scores.items()
            if score < threshold
        ]
        
        # Trier par score croissant (les plus faibles en premier)
        weak_genres.sort(key=lambda g: genre_avg_scores[g])
        
        logger.info(f"📉 Genres faiblement couverts: {weak_genres}")
        
        return weak_genres
