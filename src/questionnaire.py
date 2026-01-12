"""
Questionnaire Hybride pour la Collecte des Préférences Cinématographiques
EF1 : Acquisition de la Donnée

Combine :
- Questions ouvertes (texte libre)
- Échelles de Likert (auto-déclaration)
- Questions guidées
"""

import streamlit as st
from typing import Dict, List
import json
from datetime import datetime
from pathlib import Path


class QuestionnaireManager:
    """Gestionnaire du questionnaire cinématographique (EF1)"""
    
    def __init__(self):
        """Initialise le questionnaire avec les catégories de films"""
        
        # Blocs de genres (adapté d'AISCA - 10 blocs)
        self.genres = [
            "Science-Fiction",
            "Drame",
            "Fantasy",
            "Animation",
            "Thriller",
            "Comédie",
            "Horreur",
            "Romance",
            "Action",
            "Biopic"
        ]
        
        # Ambiances/Moods (équivalent aux compétences dans AISCA)
        self.moods = [
            "Intellectuel/Réflexif",
            "Émotionnel/Touchant",
            "Intense/Tendu",
            "Léger/Amusant",
            "Sombre/Dérangeant",
            "Inspirant/Optimiste",
            "Contemplatif/Mélancolique",
            "Énergique/Dynamique"
        ]
        
        # Périodes (questions guidées)
        self.periodes = [
            "Années 1980 et avant",
            "Années 1990",
            "Années 2000",
            "Années 2010",
            "Années 2020"
        ]
    
    def render_questionnaire(self) -> Dict:
        """
        Affiche le questionnaire et collecte les réponses (EF1.1)
        
        Returns:
            Dictionnaire contenant toutes les réponses utilisateur
        """
        st.header("🎬 Questionnaire de Préférences Cinématographiques")
        st.markdown("---")
        
        responses = {}
        
        # ============================================================
        # SECTION 1: Description libre (EF1.1 - Question ouverte)
        # ============================================================
        st.subheader("📝 1. Décrivez votre film idéal")
        st.markdown("""
        *Décrivez en quelques phrases le type de film que vous recherchez : 
        ambiance, thèmes, émotions recherchées, style narratif, atmosphère...*
        
        💡 **Conseil** : Plus votre description est riche et détaillée, 
        plus l'analyse sémantique sera précise.
        """)
        
        responses['description_libre'] = st.text_area(
            "Votre description (minimum 20 caractères)",
            height=150,
            placeholder="Exemple: Je cherche un film qui mélange science-fiction et philosophie, "
                       "avec des visuels impressionnants et une réflexion sur la nature de la réalité. "
                       "J'aime les films qui me font réfléchir longtemps après les avoir vus, "
                       "avec une atmosphère contemplative et des twists narratifs surprenants...",
            help="Cette description sera analysée sémantiquement via SBERT",
            key="desc_libre"
        )
        
        st.markdown("---")
        
        # ============================================================
        # SECTION 2: Auto-déclaration par genre (EF1.1 - Likert)
        # ============================================================
        st.subheader("🎭 2. Évaluez votre intérêt pour chaque genre")
        st.markdown("""
        *Utilisez l'échelle de Likert pour indiquer votre niveau d'intérêt*
        
        **Échelle** : 1 = Pas du tout intéressé | 5 = Très intéressé
        """)
        
        responses['preferences_genres'] = {}
        
        # Affichage en 2 colonnes pour meilleure UX
        cols = st.columns(2)
        for idx, genre in enumerate(self.genres):
            with cols[idx % 2]:
                responses['preferences_genres'][genre] = st.slider(
                    f"🎬 {genre}",
                    min_value=1,
                    max_value=5,
                    value=3,
                    key=f"genre_{genre}",
                    help=f"Votre niveau d'intérêt pour le genre {genre}"
                )
        
        st.markdown("---")
        
        # ============================================================
        # SECTION 3: Mood/Ambiance (EF1.1 - Likert)
        # ============================================================
        st.subheader("🎨 3. Quelle ambiance recherchez-vous ?")
        st.markdown("""
        *Évaluez l'intensité de l'ambiance ou du mood souhaité*
        
        **Échelle** : 1 = Pas du tout | 5 = Absolument
        """)
        
        responses['preferences_moods'] = {}
        
        for mood in self.moods:
            responses['preferences_moods'][mood] = st.slider(
                f"🎨 {mood}",
                min_value=1,
                max_value=5,
                value=3,
                key=f"mood_{mood}",
                help=f"Intensité souhaitée pour l'ambiance: {mood}"
            )
        
        st.markdown("---")
        
        # ============================================================
        # SECTION 4: Questions guidées
        # ============================================================
        st.subheader("🔍 4. Questions complémentaires")
        
        # Période préférée
        responses['periode_preferee'] = st.multiselect(
            "📅 Période(s) de sortie préférée(s)",
            self.periodes,
            help="Vous pouvez sélectionner plusieurs périodes",
            key="periode"
        )
        
        # Réalisateurs favoris
        responses['realisateurs_favoris'] = st.text_input(
            "🎬 Réalisateurs favoris (séparés par des virgules)",
            placeholder="Ex: Christopher Nolan, Denis Villeneuve, Hayao Miyazaki",
            help="Optionnel : cela nous aide à mieux cerner vos goûts cinématographiques",
            key="realisateurs"
        )
        
        # Films de référence
        responses['films_references'] = st.text_area(
            "🌟 Films que vous avez adorés (un par ligne)",
            height=100,
            placeholder="Ex:\nInception\nBlade Runner 2049\nSpirited Away",
            help="Optionnel : listez quelques films que vous considérez comme des références personnelles",
            key="films_ref"
        )
        
        # Éléments à éviter
        responses['elements_a_eviter'] = st.text_area(
            "🚫 Y a-t-il des éléments que vous souhaitez éviter ?",
            height=80,
            placeholder="Ex: violence graphique, fin triste, rythme lent, horreur gore...",
            help="Optionnel : dites-nous ce que vous n'aimez pas ou préférez éviter",
            key="eviter"
        )
        
        # Métadonnées (EF1.2 - Structuration)
        responses['timestamp'] = datetime.now().isoformat()
        responses['version'] = "1.0"
        
        return responses
    
    def validate_responses(self, responses: Dict) -> tuple[bool, str]:
        """
        Valide les réponses du questionnaire
        
        Args:
            responses: Dictionnaire des réponses
            
        Returns:
            (bool, message): (validation réussie?, message d'erreur éventuel)
        """
        # Vérifier que la description libre est suffisante
        desc = responses.get('description_libre', '').strip()
        
        if not desc:
            return False, "⚠️ Veuillez fournir une description de votre film idéal"
        
        if len(desc) < 20:
            return False, f"⚠️ Description trop courte ({len(desc)} caractères). Minimum 20 caractères pour une analyse sémantique de qualité."
        
        # Vérification optionnelle : au moins une préférence forte
        genres_prefs = responses.get('preferences_genres', {})
        has_strong_pref = any(score >= 4 for score in genres_prefs.values())
        
        if not has_strong_pref:
            # Warning mais pas bloquant
            st.info("💡 Astuce : Indiquer au moins un genre avec un score de 4 ou 5 améliore la précision des recommandations")
        
        return True, "✅ Questionnaire validé"
    
    def save_responses(self, responses: Dict, filepath: str = "data/user_responses.json") -> bool:
        """
        Sauvegarde les réponses utilisateur (EF1.2 - Structuration)
        
        Args:
            responses: Dictionnaire des réponses
            filepath: Chemin du fichier de sauvegarde
            
        Returns:
            True si sauvegarde réussie, False sinon
        """
        try:
            filepath_obj = Path(filepath)
            filepath_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Charger les réponses existantes
            all_responses = []
            if filepath_obj.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content:
                            loaded = json.loads(content)
                            all_responses = loaded if isinstance(loaded, list) else [loaded]
                except json.JSONDecodeError:
                    st.warning("⚠️ Fichier de réponses corrompu, création d'un nouveau fichier")
                    all_responses = []
            
            # Ajouter les nouvelles réponses
            all_responses.append(responses)
            
            # Sauvegarder
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(all_responses, f, ensure_ascii=False, indent=2)
            
            st.success(f"💾 Réponses sauvegardées avec succès ({len(all_responses)} sessions totales)")
            return True
            
        except Exception as e:
            st.error(f"❌ Erreur lors de la sauvegarde: {e}")
            return False
    
    def get_text_for_analysis(self, responses: Dict) -> str:
        """
        Compile toutes les entrées textuelles pour l'analyse sémantique
        
        Args:
            responses: Dictionnaire des réponses
            
        Returns:
            Texte consolidé pour l'analyse SBERT
        """
        text_parts = []
        
        # Description principale (poids fort)
        if responses.get('description_libre'):
            text_parts.append(responses['description_libre'])
        
        # Ajouter les réalisateurs favoris
        if responses.get('realisateurs_favoris'):
            text_parts.append(f"Réalisateurs appréciés: {responses['realisateurs_favoris']}")
        
        # Ajouter les films de référence
        if responses.get('films_references'):
            films_list = responses['films_references'].strip()
            if films_list:
                text_parts.append(f"Films de référence: {films_list}")
        
        # Ajouter les périodes préférées
        if responses.get('periode_preferee'):
            periodes_str = ", ".join(responses['periode_preferee'])
            text_parts.append(f"Périodes préférées: {periodes_str}")
        
        # Éléments à éviter (avec contexte négatif)
        if responses.get('elements_a_eviter'):
            text_parts.append(f"Éléments à éviter: {responses['elements_a_eviter']}")
        
        return " | ".join(text_parts)
    
    def get_genre_weights(self, responses: Dict) -> Dict[str, float]:
        """
        Convertit les préférences Likert en poids normalisés
        
        Args:
            responses: Dictionnaire des réponses
            
        Returns:
            Dictionnaire {genre: poids normalisé [0,1]}
        """
        prefs = responses.get('preferences_genres', {})
        
        # Normaliser les scores de 1-5 à 0-1
        return {genre: (score / 5.0) for genre, score in prefs.items()}
    
    def get_mood_weights(self, responses: Dict) -> Dict[str, float]:
        """
        Convertit les préférences de mood en poids normalisés
        
        Args:
            responses: Dictionnaire des réponses
            
        Returns:
            Dictionnaire {mood: poids normalisé [0,1]}
        """
        prefs = responses.get('preferences_moods', {})
        
        # Normaliser les scores de 1-5 à 0-1
        return {mood: (score / 5.0) for mood, score in prefs.items()}
