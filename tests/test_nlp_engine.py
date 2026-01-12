"""
Tests Unitaires pour le Moteur NLP
"""

import unittest
import pandas as pd
import numpy as np
from src.nlp_engine import NLPEngine


class TestNLPEngine(unittest.TestCase):
    """Tests pour le moteur NLP/SBERT"""
    
    def setUp(self):
        """Initialisation avant chaque test"""
        self.engine = NLPEngine()
    
    def test_engine_initialization(self):
        """Test de l'initialisation du moteur"""
        self.assertIsNotNone(self.engine.model)
        self.assertEqual(self.engine.model_name, 'paraphrase-multilingual-MiniLM-L12-v2')
    
    def test_encode_text(self):
        """Test de l'encodage de texte"""
        text = "J'aime les films de science-fiction"
        embedding = self.engine.encode_text(text)
        
        self.assertIsInstance(embedding, np.ndarray)
        self.assertEqual(embedding.ndim, 1)
        self.assertGreater(len(embedding), 0)
    
    def test_similarity_range(self):
        """Test que la similarité est dans [0, 1]"""
        text1 = "Science fiction épique avec des visuels impressionnants"
        text2 = "Film romantique léger et amusant"
        
        emb1 = self.engine.encode_text(text1)
        emb2 = self.engine.encode_text(text2)
        
        similarity = self.engine.calculate_similarity(emb1, emb2.reshape(1, -1))
        
        self.assertTrue(0 <= similarity[0] <= 1)
    
    def test_cache_functionality(self):
        """Test du système de cache"""
        text = "Test de cache"
        
        # Premier encodage
        emb1 = self.engine.encode_text(text, cache_key="test_cache")
        
        # Deuxième encodage (doit venir du cache)
        emb2 = self.engine.encode_text(text, cache_key="test_cache")
        
        np.testing.assert_array_equal(emb1, emb2)
        self.assertIn("test_cache", self.engine.embeddings_cache)


if __name__ == '__main__':
    unittest.main()
