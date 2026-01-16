"""
Questionnaire pour collecter les preferences cinematographiques
"""

import streamlit as st
from typing import Dict, List
import json
from datetime import datetime
from pathlib import Path


class QuestionnaireManager:
    """Gestionnaire du questionnaire"""
    
    def __init__(self):
        """Initialise les categories de films"""
        self.genres = [
            "Science-Fiction",
            "Drame",
            "Fantasy",
            "Animation",
            "Thriller",
            "Comedie",
            "Horreur",
            "Romance",
            "Action",
            "Biopic"
        ]
        
        self.moods = [
            "Intellectuel/Reflexif",
            "Emotionnel/Touchant",
            "Intense/Tendu",
            "Leger/Amusant",
            "Sombre/Derangeant",
            "Inspirant/Optimiste",
            "Contemplatif/Melancolique",
            "Energique/Dynamique"
        ]
        
        self.periodes = [
            "Annees 1980 et avant",
            "Annees 1990",
            "Annees 2000",
            "Annees 2010",
            "Annees 2020"
        ]
    
    def render_questionnaire(self) -> Dict:
        """
        Affiche le questionnaire et collecte les reponses (EF1.1)
        
        Returns:
            Dictionnaire contenant toutes les reponses utilisateur
        """
        st.header("Questionnaire de Preferences Cinematographiques")
        st.markdown("---")
        
        responses = {}
        
        # Section 1: Description libre (EF1.1 - Question ouverte)
        st.subheader("1. Decrivez votre film ideal")
        st.markdown("""
        *Decrivez en quelques phrases le type de film que vous recherchez : 
        ambiance, themes, emotions recherchees, style narratif, atmosphere...*
        
        Conseil : Plus votre description est riche et detaillee, 
        plus l'analyse semantique sera precise.
        """)
        
        responses['description_libre'] = st.text_area(
            "Votre description (minimum 20 caracteres)",
            height=150,
            placeholder="Exemple: Je cherche un film qui melange science-fiction et philosophie, "
                       "avec des visuels impressionnants et une reflexion sur la nature de la realite. "
                       "J'aime les films qui me font reflechir longtemps apres les avoir vus, "
                       "avec une atmosphere contemplative et des twists narratifs surprenants...",
            help="Cette description sera analysee semantiquement via SBERT",
            key="desc_libre"
        )
        
        st.markdown("---")
        
        # Section 2: Auto-declaration par genre (EF1.1 - Likert)
        st.subheader("2. Evaluez votre interet pour chaque genre")
        st.markdown("""
        *Utilisez l'echelle de Likert pour indiquer votre niveau d'interet*
        
        **Echelle** : 1 = Pas du tout interesse | 5 = Tres interesse
        """)
        
        responses['preferences_genres'] = {}
        
        # Affichage en 2 colonnes pour meilleure UX
        cols = st.columns(2)
        for idx, genre in enumerate(self.genres):
            with cols[idx % 2]:
                responses['preferences_genres'][genre] = st.slider(
                    f"{genre}",
                    min_value=1,
                    max_value=5,
                    value=3,
                    key=f"genre_{genre}",
                    help=f"Votre niveau d'interet pour le genre {genre}"
                )
        
        st.markdown("---")
        
        # Section 3: Mood/Ambiance (EF1.1 - Likert)
        st.subheader("3. Quelle ambiance recherchez-vous ?")
        st.markdown("""
        *Evaluez l'intensite de l'ambiance ou du mood souhaite*
        
        **Echelle** : 1 = Pas du tout | 5 = Absolument
        """)
        
        responses['preferences_moods'] = {}
        
        for mood in self.moods:
            responses['preferences_moods'][mood] = st.slider(
                f"{mood}",
                min_value=1,
                max_value=5,
                value=3,
                key=f"mood_{mood}",
                help=f"Intensite souhaitee pour l'ambiance: {mood}"
            )
        
        st.markdown("---")
        
        # Section 4: Questions guidees
        st.subheader("4. Questions complementaires")
        
        # Periode preferee
        responses['periode_preferee'] = st.multiselect(
            "Periode(s) de sortie preferee(s)",
            self.periodes,
            help="Vous pouvez selectionner plusieurs periodes",
            key="periode"
        )
        
        # Realisateurs favoris
        responses['realisateurs_favoris'] = st.text_input(
            "Realisateurs favoris (separes par des virgules)",
            placeholder="Ex: Christopher Nolan, Denis Villeneuve, Hayao Miyazaki",
            help="Optionnel : cela nous aide a mieux cerner vos gouts cinematographiques",
            key="realisateurs"
        )
        
        # Films de reference
        responses['films_references'] = st.text_area(
            "Films que vous avez adores (un par ligne)",
            height=100,
            placeholder="Ex:\nInception\nBlade Runner 2049\nSpirited Away",
            help="Optionnel : listez quelques films que vous considerez comme des references personnelles",
            key="films_ref"
        )
        
        # Elements a eviter
        responses['elements_a_eviter'] = st.text_area(
            "Y a-t-il des elements que vous souhaitez eviter ?",
            height=80,
            placeholder="Ex: violence graphique, fin triste, rythme lent, horreur gore...",
            help="Optionnel : dites-nous ce que vous n'aimez pas ou preferez eviter",
            key="eviter"
        )
        
        # Metadonnees (EF1.2 - Structuration)
        responses['timestamp'] = datetime.now().isoformat()
        responses['version'] = "1.0"
        
        return responses
    
    def validate_responses(self, responses: Dict) -> tuple[bool, str]:
        """
        Valide les reponses du questionnaire
        
        Args:
            responses: Dictionnaire des reponses
            
        Returns:
            (bool, message): (validation reussie?, message d'erreur eventuel)
        """
        # Verifier que la description libre est suffisante
        desc = responses.get('description_libre', '').strip()
        
        if not desc:
            return False, "Veuillez fournir une description de votre film ideal"
        
        if len(desc) < 20:
            return False, f"Description trop courte ({len(desc)} caracteres). Minimum 20 caracteres pour une analyse semantique de qualite."
        
        # Verification optionnelle : au moins une preference forte
        genres_prefs = responses.get('preferences_genres', {})
        has_strong_pref = any(score >= 4 for score in genres_prefs.values())
        
        if not has_strong_pref:
            # Warning mais pas bloquant
            st.info("Astuce : Indiquer au moins un genre avec un score de 4 ou 5 ameliore la precision des recommandations")
        
        return True, "Questionnaire valide"
    
    def save_responses(self, responses: Dict, filepath: str = "data/user_responses.json") -> bool:
        """
        Sauvegarde les reponses utilisateur (EF1.2 - Structuration)
        
        Args:
            responses: Dictionnaire des reponses
            filepath: Chemin du fichier de sauvegarde
            
        Returns:
            True si sauvegarde reussie, False sinon
        """
        try:
            filepath_obj = Path(filepath)
            filepath_obj.parent.mkdir(parents=True, exist_ok=True)
            
            # Charger les reponses existantes
            all_responses = []
            if filepath_obj.exists():
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read().strip()
                        if content:
                            loaded = json.loads(content)
                            all_responses = loaded if isinstance(loaded, list) else [loaded]
                except json.JSONDecodeError:
                    st.warning("Fichier de reponses corrompu, creation d'un nouveau fichier")
                    all_responses = []
            
            # Ajouter les nouvelles reponses
            all_responses.append(responses)
            
            # Sauvegarder
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(all_responses, f, ensure_ascii=False, indent=2)
            
            st.success(f"Reponses sauvegardees avec succes ({len(all_responses)} sessions totales)")
            return True
            
        except Exception as e:
            st.error(f"Erreur lors de la sauvegarde: {e}")
            return False
    
    def get_text_for_analysis(self, responses: Dict) -> str:
        """
        Compile toutes les entrees textuelles pour l'analyse semantique
        
        Args:
            responses: Dictionnaire des reponses
            
        Returns:
            Texte consolide pour l'analyse SBERT
        """
        text_parts = []
        
        # Section 1: Genres preferes (convertis en texte descriptif)
        genres_prefs = responses.get('preferences_genres', {})
        top_genres = [genre for genre, score in sorted(genres_prefs.items(), key=lambda x: x[1], reverse=True) if score >= 4]
        if top_genres:
            text_parts.append(f"J'adore les films de {', '.join(top_genres)}.")
        
        # Section 2: Ambiances preferees (convertis en texte descriptif)
        moods_prefs = responses.get('preferences_moods', {})
        top_moods = [mood for mood, score in sorted(moods_prefs.items(), key=lambda x: x[1], reverse=True) if score >= 4]
        if top_moods:
            text_parts.append(f"Je recherche une ambiance {', '.join(top_moods)}.")
        
        # Section 3: Description principale (poids fort)
        if responses.get('description_libre'):
            text_parts.append(responses['description_libre'])
        
        # Section 4: Realisateurs favoris
        if responses.get('realisateurs_favoris'):
            text_parts.append(f"Realisateurs apprecies: {responses['realisateurs_favoris']}")
        
        # Section 5: Films de reference
        if responses.get('films_references'):
            films_list = responses['films_references'].strip()
            if films_list:
                text_parts.append(f"Films de reference: {films_list}")
        
        # Section 6: Periodes preferees
        if responses.get('periode_preferee'):
            periodes_str = ", ".join(responses['periode_preferee'])
            text_parts.append(f"Periodes preferees: {periodes_str}")
        
        # Section 7: Elements a eviter (avec contexte negatif)
        if responses.get('elements_a_eviter'):
            text_parts.append(f"Je n'aime pas: {responses['elements_a_eviter']}")
        
        return " ".join(text_parts)
    
    def get_genre_weights(self, responses: Dict) -> Dict[str, float]:
        """
        Convertit les preferences Likert en poids normalises
        
        Args:
            responses: Dictionnaire des reponses
            
        Returns:
            Dictionnaire {genre: poids normalise [0,1]}
        """
        prefs = responses.get('preferences_genres', {})
        
        # Normaliser les scores de 1-5 a 0-1
        return {genre: (score / 5.0) for genre, score in prefs.items()}
    
    def get_mood_weights(self, responses: Dict) -> Dict[str, float]:
        """
        Convertit les preferences de mood en poids normalises
        
        Args:
            responses: Dictionnaire des reponses
            
        Returns:
            Dictionnaire {mood: poids normalise [0,1]}
        """
        prefs = responses.get('preferences_moods', {})
        
        # Normaliser les scores de 1-5 a 0-1
        return {mood: (score / 5.0) for mood, score in prefs.items()}
