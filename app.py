"""
Application principale de recommandation de films
Interface Streamlit pour AISCA-Cinema

Projet EFREI - IA Générative 2025-26
RNCP40875 - Bloc 2

Architecture RAG pour recommander des films
Basé sur le framework AISCA adapté au cinéma
"""

import streamlit as st
import logging
from pathlib import Path

# Imports des modules du projet
from src.questionnaire import QuestionnaireManager
from src.nlp_engine import NLPEngine
from src.scoring import ScoringSystem
from src.genai_integration import GenAIIntegration
from src.visualization import VisualizationManager

# Configuration des logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Configuration de la page Streamlit
st.set_page_config(
    page_title="AISCA-Cinema | Recommandation Cinématographique IA",
    page_icon="🎬",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(120deg, #FF6B6B, #4ECDC4);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #7F8C8D;
        margin-bottom: 2rem;
    }
    .stButton>button {
        width: 100%;
    }
</style>
""", unsafe_allow_html=True)


def initialize_session_state():
    """Initialise les variables de session"""
    if 'responses' not in st.session_state:
        st.session_state.responses = None
    if 'recommendations' not in st.session_state:
        st.session_state.recommendations = None
    if 'analysis_done' not in st.session_state:
        st.session_state.analysis_done = False


def main():
    """Fonction principale de l'application"""
    
    initialize_session_state()
    
    # Section en-tete de la page
    st.markdown('<h1 class="main-header">🎬 AISCA-Cinema</h1>', unsafe_allow_html=True)
    st.markdown(
        '<p class="sub-header">Agent Intelligent Sémantique et Génératif de Recommandation Cinématographique</p>',
        unsafe_allow_html=True
    )
    
    # Sidebar avec les infos du projet
    with st.sidebar:
        st.image("https://via.placeholder.com/300x100/FF6B6B/FFFFFF?text=AISCA-Cinema", width=300)
        
        st.markdown("### 📋 À propos")
        st.info("""
        **AISCA-Cinema** utilise :
        - 🧠 **SBERT** pour l'analyse sémantique
        - 🤖 **Gemini AI** pour la génération
        - 📊 **Architecture RAG** pour des recommandations fiables
        
        **Projet EFREI 2025-26**  
        Module: IA Générative  
        RNCP40875 - Bloc 2
        """)
        
        st.markdown("### 🔧 Technologies")
        st.markdown("""
        - Python 3.9+
        - Streamlit
        - SentenceTransformers
        - Google Gemini API
        - Plotly
        """)
        
        st.markdown("### 📊 Exigences Implémentées")
        st.success("✅ EF1: Questionnaire Hybride")
        st.success("✅ EF2: Moteur NLP SBERT")
        st.success("✅ EF3: Scoring & Top 3")
        st.success("✅ EF4: GenAI + Cache")
        
        if st.session_state.analysis_done:
            if st.button("🔄 Nouvelle Analyse"):
                st.session_state.responses = None
                st.session_state.recommendations = None
                st.session_state.analysis_done = False
                st.rerun()
    
    # Etape 1 - Affichage du questionnaire
    if not st.session_state.analysis_done:
        st.markdown("## 📝 Étape 1 : Questionnaire de Préférences")
        st.markdown("Complétez le questionnaire ci-dessous pour découvrir vos recommandations personnalisées.")
        
        questionnaire = QuestionnaireManager()
        responses = questionnaire.render_questionnaire()
        
        st.markdown("---")
        
        # Bouton d'analyse
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            analyze_button = st.button("🎯 Analyser mes Préférences", type="primary", use_container_width=True)
        
        if analyze_button:
            # Valider les réponses
            is_valid, message = questionnaire.validate_responses(responses)
            
            if not is_valid:
                st.error(message)
            else:
                st.success(message)
                
                # Sauvegarder les reponses de l'utilisateur
                questionnaire.save_responses(responses)
                
                # Stocker les reponses dans la session
                st.session_state.responses = responses
                
                # Lancer le processus d'analyse
                with st.spinner("🔍 Analyse en cours... Veuillez patienter."):
                    try:
                        # Etape 1 - Initialiser les composants necessaires
                        st.toast("🔧 Initialisation des composants...")
                        nlp_engine = NLPEngine()
                        scoring_system = ScoringSystem(alpha=0.50, beta=0.30, gamma=0.20)
                        genai = GenAIIntegration()
                        
                        # Etape 2 - Charger la base de donnees de films
                        st.toast("📚 Chargement du référentiel de films...")
                        csv_path = Path(__file__).parent / 'data' / 'films_referentiel.csv'
                        referentiel = nlp_engine.load_referentiel(str(csv_path))
                        
                        # Etape 3 - Preparer le texte utilisateur pour l'analyse
                        user_text = questionnaire.get_text_for_analysis(responses)
                        
                        # Etape 4 - Enrichir le texte si trop court avec l'IA
                        user_text, was_enriched = genai.enrich_short_text(user_text, min_words=15)
                        if was_enriched:
                            st.toast("✨ Description enrichie par l'IA")
                        
                        # Etape 5 - Analyse semantique avec SBERT
                        st.toast("🧠 Analyse sémantique avec SBERT...")
                        recommendations, similarities = nlp_engine.analyze_user_input(user_text, top_n=3)
                        
                        # Etape 6 - Calculer les scores ponderes
                        st.toast("🎯 Calcul des scores finaux...")
                        genre_weights = questionnaire.get_genre_weights(responses)
                        mood_weights = questionnaire.get_mood_weights(responses)
                        
                        ranked_recommendations = scoring_system.rank_films(
                            recommendations=recommendations,
                            semantic_similarities=similarities,
                            user_genre_weights=genre_weights,
                            user_mood_weights=mood_weights,
                            referentiel=referentiel
                        )
                        
                        # Etape 7 - Recuperer le top 3 des films
                        top_3 = scoring_system.get_top_recommendations(ranked_recommendations, top_n=3)
                        
                        # Etape 8 - Calculer les statistiques
                        coverage_stats = nlp_engine.get_coverage_stats(similarities)
                        genre_distribution = nlp_engine.get_genre_distribution(similarities, threshold=0.5)
                        coverage_score = scoring_system.calculate_coverage_score(
                            similarities, genre_weights, mood_weights, referentiel
                        )
                        weak_genres = scoring_system.identify_weak_genres(similarities, referentiel, threshold=0.4)
                        
                        # Etape 9 - Generation avec l'IA Gemini
                        st.toast("🤖 Génération du profil et du plan...")
                        
                        # Generer le plan de decouverte avec 1 seul appel API
                        user_profile_summary = f"Genres préférés: {', '.join([g for g, w in sorted(genre_weights.items(), key=lambda x: x[1], reverse=True)[:3]])}. Moods: {', '.join([m for m, w in sorted(mood_weights.items(), key=lambda x: x[1], reverse=True)[:3]])}."
                        discovery_plan = genai.generate_discovery_plan(weak_genres, top_3, user_profile_summary)
                        
                        # Generer le profil cinephile avec 1 seul appel API
                        cinephile_profile = genai.generate_cinephile_profile(
                            top_3, genre_weights, mood_weights, coverage_score
                        )
                        
                        # Sauvegarder tous les resultats
                        st.session_state.recommendations = {
                            'top_3': top_3,
                            'all_recommendations': ranked_recommendations,
                            'similarities': similarities,
                            'coverage_stats': coverage_stats,
                            'genre_distribution': genre_distribution,
                            'coverage_score': coverage_score,
                            'weak_genres': weak_genres,
                            'discovery_plan': discovery_plan,
                            'cinephile_profile': cinephile_profile,
                            'genre_weights': genre_weights,
                            'mood_weights': mood_weights,
                            'api_stats': genai.get_api_stats()
                        }
                        
                        st.session_state.analysis_done = True
                        st.success("✅ Analyse terminée !")
                        st.rerun()
                        
                    except Exception as e:
                        st.error(f"❌ Erreur lors de l'analyse: {str(e)}")
                        logger.error(f"Erreur analyse: {e}", exc_info=True)
    
    # Etape 2 - Affichage des resultats
    else:
        viz = VisualizationManager()
        results = st.session_state.recommendations
        responses = st.session_state.responses
        
        st.markdown("## 🎯 Vos Recommandations Personnalisées")
        st.markdown("---")
        
        # Organiser les resultats en onglets
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "🏆 Top 3 Films",
            "📊 Visualisations",
            "🎭 Profil Cinéphile",
            "📚 Plan de Découverte",
            "⚙️ Statistiques"
        ])
        
        # Onglet 1 - Les 3 meilleurs films recommandes
        with tab1:
            st.markdown("### 🏆 Vos 3 Films Recommandés")
            
            for film in results['top_3']:
                viz.display_film_card(film, film['rang'])
        
        # Onglet 2 - Graphiques et visualisations
        with tab2:
            st.markdown("### 📊 Analyse Visuelle de votre Profil")
            
            col1, col2 = st.columns(2)
            
            with col1:
                viz.plot_genre_radar(results['genre_weights'])
            
            with col2:
                viz.plot_mood_radar(results['mood_weights'])
            
            viz.plot_recommendation_scores(results['top_3'])
            
            viz.plot_genre_distribution(results['genre_distribution'])
            
            st.markdown("### 📈 Statistiques de Couverture")
            viz.display_coverage_stats(results['coverage_stats'])
        
        # Onglet 3 - Profil personnalise genere par l'IA
        with tab3:
            st.markdown("### 🎭 Votre Profil Cinéphile")
            st.info("Généré par l'IA Gemini (1 appel API - EF4.3)")
            
            st.markdown(results['cinephile_profile'])
            
            st.markdown("---")
            st.markdown(f"**Score d'Affinité Global:** {results['coverage_score']:.1%}")
            
            # Interpreter le score pour l'utilisateur
            if results['coverage_score'] >= 0.7:
                st.success("🌟 Excellent ! Vos goûts sont très bien définis.")
            elif results['coverage_score'] >= 0.5:
                st.info("👍 Bon profil cinématographique avec de la diversité.")
            else:
                st.warning("🔍 Profil varié ! Vous êtes ouvert à de nombreux styles.")
        
        # Onglet 4 - Plan de decouverte personnalise
        with tab4:
            st.markdown("### 📚 Plan de Découverte Personnalisé")
            st.info("Généré par l'IA Gemini (1 appel API - EF4.2)")
            
            st.markdown(results['discovery_plan'])
            
            if results['weak_genres']:
                st.markdown("### 🎬 Genres à Explorer")
                cols = st.columns(len(results['weak_genres'][:5]))
                for idx, genre in enumerate(results['weak_genres'][:5]):
                    with cols[idx]:
                        st.metric(f"Genre #{idx+1}", genre)
        
        # Onglet 5 - Details techniques et statistiques
        with tab5:
            st.markdown("### ⚙️ Détails Techniques de l'Analyse")
            
            st.markdown("#### 🧠 Analyse Sémantique (SBERT)")
            st.json({
                "Modèle": "paraphrase-multilingual-MiniLM-L12-v2",
                "Type": "Sentence-BERT (Embeddings Contextuels)",
                "Mesure": "Similarité Cosinus",
                "Films analysés": results['coverage_stats']['total_films']
            })
            
            st.markdown("#### 🎯 Système de Scoring")
            st.code("""
Formule de Score Final:
Score = 0.50 × Similarité_Sémantique 
      + 0.30 × Score_Genre
      + 0.20 × Score_Mood

Où tous les scores sont normalisés dans [0, 1]
            """)
            
            st.markdown("#### 🤖 Utilisation de l'IA Générative")
            viz.display_api_usage(results['api_stats'])
            
            st.markdown("#### 📊 Données Brutes")
            with st.expander("Voir les scores détaillés"):
                import pandas as pd
                df_scores = pd.DataFrame([
                    {
                        'Rang': r['rang'],
                        'Film': r['titre'],
                        'Score Final': f"{r['score_final']:.3f}",
                        'Sémantique': f"{r['composantes']['sémantique']:.3f}",
                        'Genre': f"{r['composantes']['genre']:.3f}",
                        'Mood': f"{r['composantes']['mood']:.3f}"
                    }
                    for r in results['top_3']
                ])
                st.dataframe(df_scores, use_container_width=True)
    
    # Footer de la page
    st.markdown("---")
    st.markdown(
        """
        <div style='text-align: center; color: #7F8C8D;'>
            <p>🎬 <strong>AISCA-Cinema</strong> | Projet EFREI 2025-26 | IA Générative</p>
            <p>Développé avec ❤️ en Python | Streamlit | SBERT | Gemini AI</p>
        </div>
        """,
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
