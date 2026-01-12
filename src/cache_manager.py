"""
Gestionnaire de Cache pour les appels GenAI
EF4 - Contrainte obligatoire : Implémentation d'un caching automatique

Objectif : Limiter les coûts API et respecter le Free Tier de Gemini
"""

import json
import hashlib
from pathlib import Path
from typing import Optional, Dict
import logging

logger = logging.getLogger(__name__)


class CacheManager:
    """
    Gestion du cache pour les réponses GenAI
    
    Respecte les contraintes:
    - Appels API strictement limités
    - Réutilisation automatique des réponses
    - Persistance locale (JSON)
    """
    
    def __init__(self, cache_dir: str = ".cache", max_size: int = 100, enabled: bool = True):
        """
        Initialise le gestionnaire de cache
        
        Args:
            cache_dir: Répertoire de stockage du cache
            max_size: Nombre maximum d'entrées dans le cache
            enabled: Activer/désactiver le cache
        """
        self.enabled = enabled
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.cache_file = self.cache_dir / "genai_cache.json"
        self.max_size = max_size
        self.cache = self._load_cache()
        
        logger.info(f"✅ CacheManager initialisé - Enabled: {enabled}, Max size: {max_size}")
        
    def _load_cache(self) -> Dict:
        """Charge le cache depuis le fichier"""
        if not self.enabled:
            return {}
            
        if self.cache_file.exists():
            try:
                with open(self.cache_file, 'r', encoding='utf-8') as f:
                    cache_data = json.load(f)
                    logger.info(f"📂 Cache chargé: {len(cache_data)} entrées")
                    return cache_data
            except Exception as e:
                logger.warning(f"⚠️ Erreur lors du chargement du cache: {e}")
                return {}
        return {}
    
    def _save_cache(self):
        """Sauvegarde le cache dans le fichier"""
        if not self.enabled:
            return
            
        try:
            with open(self.cache_file, 'w', encoding='utf-8') as f:
                json.dump(self.cache, f, ensure_ascii=False, indent=2)
            logger.debug(f"💾 Cache sauvegardé: {len(self.cache)} entrées")
        except Exception as e:
            logger.error(f"❌ Erreur lors de la sauvegarde du cache: {e}")
    
    def _generate_key(self, prompt: str, model: str = "gemini") -> str:
        """
        Génère une clé unique pour un prompt
        
        Args:
            prompt: Le prompt à hasher
            model: Le modèle utilisé
            
        Returns:
            Clé de hash SHA-256
        """
        content = f"{model}:{prompt}"
        return hashlib.sha256(content.encode('utf-8')).hexdigest()
    
    def get(self, prompt: str, model: str = "gemini") -> Optional[str]:
        """
        Récupère une réponse depuis le cache
        
        Args:
            prompt: Le prompt recherché
            model: Le modèle utilisé
            
        Returns:
            La réponse cachée ou None si non trouvée
        """
        if not self.enabled:
            return None
            
        key = self._generate_key(prompt, model)
        response = self.cache.get(key)
        
        if response:
            logger.info(f"✅ Cache HIT - Réponse trouvée (longueur prompt: {len(prompt)} caractères)")
        else:
            logger.info(f"❌ Cache MISS - Nouvel appel API nécessaire")
            
        return response
    
    def set(self, prompt: str, response: str, model: str = "gemini"):
        """
        Ajoute une réponse au cache
        
        Args:
            prompt: Le prompt
            response: La réponse à cacher
            model: Le modèle utilisé
        """
        if not self.enabled:
            return
            
        key = self._generate_key(prompt, model)
        
        # Si le cache est plein, supprimer l'entrée la plus ancienne (FIFO)
        if len(self.cache) >= self.max_size:
            oldest_key = next(iter(self.cache))
            del self.cache[oldest_key]
            logger.info(f"🗑️ Cache plein - Suppression de l'entrée la plus ancienne")
        
        self.cache[key] = response
        self._save_cache()
        logger.info(f"💾 Réponse ajoutée au cache (total: {len(self.cache)}/{self.max_size} entrées)")
    
    def clear(self):
        """Vide le cache complètement"""
        self.cache = {}
        self._save_cache()
        logger.info("🗑️ Cache vidé complètement")
    
    def get_stats(self) -> Dict:
        """
        Retourne les statistiques du cache
        
        Returns:
            Dictionnaire avec les stats
        """
        return {
            "enabled": self.enabled,
            "entries": len(self.cache),
            "max_size": self.max_size,
            "usage_percent": round((len(self.cache) / self.max_size) * 100, 2) if self.max_size > 0 else 0,
            "cache_file": str(self.cache_file),
            "cache_exists": self.cache_file.exists()
        }
    
    def __repr__(self) -> str:
        stats = self.get_stats()
        return f"CacheManager(entries={stats['entries']}/{stats['max_size']}, enabled={stats['enabled']})"
