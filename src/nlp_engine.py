"""
Moteur NLP Sémantique (SBERT)
EF2 : Moteur NLP Sémantique (Cœur du Projet - Coût Zéro)

Implémente l'analyse sémantique basée sur les embeddings contextuels SBERT
et le calcul de similarité cosinus.

Architecture inspirée d'AISCA appliquée au cinéma.
"""

import pandas as pd
import numpy as np
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict, Tuple, Optional
import logging

logger = logging.getLogger(__name__)


class NLPEngine:
    """
    Moteur d'analyse sémantique utilisant SBERT (EF2)
    
    Équivalent au moteur de matching de compétences d'AISCA,
    adapté pour la recommandation de films.
    """
    
    def __init__(self, model_name: str = 'paraphrase-multilingual-MiniLM-L12-v2'):
        """
        Initialise le moteur NLP avec SBERT (EF2.2)
        
        Args:
            model_name: Nom du modèle SentenceTransformer
                       (multilingue pour supporter le français)
        """
        logger.info(f"🔄 Chargement du modèle SBERT: {model_name}")
        
        # EF2.2: Modélisation Sémantique avec SBERT (Open-Source, Local, Coût Zéro)
        self.model = SentenceTransformer(model_name)
        self.model_name = model_name
        self.referentiel = None
        self.embeddings_cache = {}
        
        logger.info("✅ Modèle SBERT chargé avec succès")
    
    def load_referentiel(self, filepath: str = 'data/films_referentiel.csv') -> pd.DataFrame:
        """
        Charge le référentiel de films (EF2.1 - Référentiel de Compétences adapté)
        
        Dans AISCA: charge les blocs de compétences
        Ici: charge les blocs de genres cinématographiques
        
        Args:
            filepath: Chemin vers le fichier CSV du référentiel
            
        Returns:
            DataFrame du référentiel
        """
        logger.info(f"📂 Chargement du référentiel cinématographique: {filepath}")
        
        self.referentiel = pd.read_csv(filepath)
        
        # Créer une colonne avec la description complète pour l'analyse sémantique
        # (équivalent à la compilation des compétences dans AISCA)
        self.referentiel['texte_complet'] = self.referentiel.apply(
            lambda row: self._build_film_text(row),
            axis=1
        )
        
        logger.info(f"✅ Référentiel chargé: {len(self.referentiel)} films répartis en blocs de genres")
        logger.info(f"📊 Genres disponibles: {self.referentiel['Categorie'].unique().tolist()}")
        
        return self.referentiel
    
    def _build_film_text(self, row: pd.Series) -> str:
        """
        Construit le texte sémantique complet d'un film
        
        Args:
            row: Ligne du DataFrame
            
        Returns:
            Texte enrichi pour l'embedding
        """
        return (
            f"{row['Film']} ({row['Annee']}). "
            f"Réalisé par {row['Realisateur']}. "
            f"Genre: {row['Genre']}. "
            f"Description: {row['Description']} "
            f"Mots-clés: {row['Keywords']}. "
            f"Ambiance: {row['Mood']}."
        )
    
    def encode_text(self, text: str, cache_key: Optional[str] = None) -> np.ndarray:
        """
        Encode un texte en vecteur d'embeddings (EF2.2 - SBERT)
        
        Args:
            text: Texte à encoder
            cache_key: Clé pour le cache (optionnel)
            
        Returns:
            Vecteur d'embeddings contextuels
        """
        # Vérifier le cache
        if cache_key and cache_key in self.embeddings_cache:
            logger.debug(f"✅ Cache HIT pour: {cache_key}")
            return self.embeddings_cache[cache_key]
        
        # Encoder le texte avec SBERT
        embedding = self.model.encode(text, convert_to_numpy=True, show_progress_bar=False)
        
        # Mettre en cache
        if cache_key:
            self.embeddings_cache[cache_key] = embedding
            logger.debug(f"💾 Embedding mis en cache: {cache_key}")
        
        return embedding
    
    def encode_referentiel(self) -> np.ndarray:
        """
        Encode tous les films du référentiel en embeddings
        
        Équivalent AISCA: encode tous les blocs de compétences
        
        Returns:
            Matrice d'embeddings (n_films, embedding_dim)
        """
        if self.referentiel is None:
            raise ValueError("❌ Le référentiel doit être chargé avant l'encodage")
        
        logger.info(f"🔄 Encodage de {len(self.referentiel)} films avec SBERT...")
        
        # Encoder tous les textes
        embeddings = self.model.encode(
            self.referentiel['texte_complet'].tolist(),
            convert_to_numpy=True,
            show_progress_bar=True,
            batch_size=32
        )
        
        logger.info(f"✅ Encodage terminé - Shape: {embeddings.shape}")
        
        return embeddings
    
    def calculate_similarity(
        self, 
        user_embedding: np.ndarray, 
        referentiel_embeddings: np.ndarray
    ) -> np.ndarray:
        """
        Calcule la similarité cosinus (EF2.3 - Mesure de Similarité)
        
        Équivalent AISCA: calcule le matching entre profil utilisateur et compétences
        
        Args:
            user_embedding: Embedding de la requête utilisateur
            referentiel_embeddings: Embeddings du référentiel de films
            
        Returns:
            Array des scores de similarité [0, 1]
        """
        # Reshape si nécessaire
        if user_embedding.ndim == 1:
            user_embedding = user_embedding.reshape(1, -1)
        
        # EF2.3: Mesure de Similarité Cosinus
        similarities = cosine_similarity(user_embedding, referentiel_embeddings)[0]
        
        logger.info(f"📊 Similarité calculée - "
                   f"Min: {similarities.min():.3f}, "
                   f"Max: {similarities.max():.3f}, "
                   f"Moyenne: {similarities.mean():.3f}")
        
        return similarities
    
    def get_top_matches(
        self, 
        similarities: np.ndarray, 
        top_n: int = 3
    ) -> List[Tuple[int, float]]:
        """
        Récupère les top N films les plus similaires
        
        Équivalent AISCA: récupère les top profils métiers
        
        Args:
            similarities: Array des scores de similarité
            top_n: Nombre de recommandations à retourner (défaut: 3 comme dans AISCA)
            
        Returns:
            Liste de tuples (index, score) triée par score décroissant
        """
        # Trier par similarité décroissante
        top_indices = np.argsort(similarities)[::-1][:top_n]
        
        results = [(idx, float(similarities[idx])) for idx in top_indices]
        
        logger.info(f"🎯 Top {top_n} matches identifiés avec scores: {[f'{s:.3f}' for _, s in results]}")
        
        return results
    
    def analyze_user_input(
        self, 
        user_text: str, 
        top_n: int = 3
    ) -> Tuple[List[Dict], np.ndarray]:
        """
        Pipeline complet d'analyse sémantique
        
        Équivalent AISCA: pipeline complet de cartographie des compétences
        
        Args:
            user_text: Texte consolidé de l'utilisateur
            top_n: Nombre de recommandations (EF3.2: top 3)
            
        Returns:
            (recommandations, similarités): Liste des films recommandés et array des scores
        """
        if self.referentiel is None:
            raise ValueError("❌ Le référentiel doit être chargé avant l'analyse")
        
        logger.info("🔍 Début de l'analyse sémantique...")
        
        # 1. Encoder l'entrée utilisateur
        logger.info("📝 Étape 1/4: Encodage de l'entrée utilisateur")
        user_embedding = self.encode_text(user_text, cache_key="current_user_query")
        
        # 2. Encoder le référentiel
        logger.info("📚 Étape 2/4: Encodage du référentiel de films")
        referentiel_embeddings = self.encode_referentiel()
        
        # 3. Calculer les similarités
        logger.info("🔢 Étape 3/4: Calcul de la similarité cosinus")
        similarities = self.calculate_similarity(user_embedding, referentiel_embeddings)
        
        # 4. Obtenir les top matches
        logger.info(f"🎯 Étape 4/4: Extraction des top {top_n} recommandations")
        top_matches = self.get_top_matches(similarities, top_n)
        
        # 5. Construire les recommandations détaillées
        recommendations = []
        for idx, score in top_matches:
            film = self.referentiel.iloc[idx]
            recommendations.append({
                'film_id': film['FilmID'],
                'titre': film['Film'],
                'realisateur': film['Realisateur'],
                'annee': int(film['Annee']),
                'genre': film['Genre'],
                'categorie': film['Categorie'],
                'description': film['Description'],
                'keywords': film['Keywords'],
                'mood': film['Mood'],
                'block_id': film['BlockID'],
                'score_similarite': float(score),
                'rang': len(recommendations) + 1
            })
        
        logger.info(f"✅ Analyse terminée: {len(recommendations)} recommandations générées")
        
        return recommendations, similarities
    
    def get_genre_distribution(
        self, 
        similarities: np.ndarray, 
        threshold: float = 0.5
    ) -> Dict[str, float]:
        """
        Analyse la distribution des genres basée sur la similarité
        
        Équivalent AISCA: distribution des blocs de compétences
        
        Args:
            similarities: Array des scores de similarité
            threshold: Seuil minimal de similarité
            
        Returns:
            Dictionnaire {genre: score_moyen} trié par score décroissant
        """
        if self.referentiel is None:
            return {}
        
        # Filtrer les films au-dessus du seuil
        mask = similarities >= threshold
        
        if not mask.any():
            logger.warning(f"⚠️ Aucun film au-dessus du seuil {threshold}")
            return {}
        
        # Calculer les scores moyens par genre
        genre_scores = {}
        
        for genre in self.referentiel['Categorie'].unique():
            genre_mask = self.referentiel['Categorie'] == genre
            combined_mask = mask & genre_mask
            
            if combined_mask.any():
                genre_scores[genre] = float(similarities[combined_mask].mean())
        
        # Trier par score décroissant
        sorted_genres = dict(sorted(genre_scores.items(), key=lambda x: x[1], reverse=True))
        
        logger.info(f"📊 Distribution des genres (seuil {threshold}): {len(sorted_genres)} genres")
        
        return sorted_genres
    
    def get_coverage_stats(self, similarities: np.ndarray) -> Dict:
        """
        Statistiques de couverture du profil utilisateur
        
        Équivalent AISCA: couverture des compétences
        
        Args:
            similarities: Array des scores de similarité
            
        Returns:
            Statistiques détaillées
        """
        return {
            'score_moyen': float(similarities.mean()),
            'score_median': float(np.median(similarities)),
            'score_max': float(similarities.max()),
            'score_min': float(similarities.min()),
            'films_haute_affinite': int((similarities >= 0.7).sum()),
            'films_affinite_moyenne': int(((similarities >= 0.5) & (similarities < 0.7)).sum()),
            'films_faible_affinite': int((similarities < 0.5).sum()),
            'total_films': len(similarities)
        }
