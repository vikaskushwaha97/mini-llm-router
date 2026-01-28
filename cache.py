"""
Cache Module
Simple in-memory cache with MD5 hashing
"""

import hashlib
from typing import Dict, Optional
from datetime import datetime


class CacheManager:
    """Manages response caching with in-memory storage"""
    
    def __init__(self):
        self._cache: Dict[str, Dict] = {}
        self._hits = 0
        self._misses = 0
        self._tokens_saved = 0
        self._cost_saved = 0.0
    
    def _hash_prompt(self, prompt: str) -> str:
        """Generate hash key for prompt"""
        return hashlib.md5(prompt.encode()).hexdigest()
    
    def get(self, prompt: str) -> Optional[Dict]:
        """
        Check if prompt exists in cache
        
        Args:
            prompt: Input prompt
            
        Returns:
            Cached data dict or None
        """
        key = self._hash_prompt(prompt)
        
        if key in self._cache:
            self._hits += 1
            cached = self._cache[key]
            self._tokens_saved += cached['tokens']
            self._cost_saved += cached['cost']
            return cached
        
        self._misses += 1
        return None
    
    def set(self, prompt: str, tokens: int, model: str, cost: float):
        """
        Store prompt result in cache
        
        Args:
            prompt: Input prompt
            tokens: Token count
            model: Model used
            cost: Cost incurred
        """
        key = self._hash_prompt(prompt)
        self._cache[key] = {
            'tokens': tokens,
            'model': model,
            'cost': cost,
            'timestamp': datetime.now().isoformat()
        }
    
    def get_stats(self) -> Dict:
        """Get cache statistics"""
        return {
            'hits': self._hits,
            'misses': self._misses,
            'tokens_saved': self._tokens_saved,
            'cost_saved': self._cost_saved,
            'cache_size': len(self._cache)
        }
    
    def clear(self):
        """Clear all cache data"""
        self._cache.clear()
        self._hits = 0
        self._misses = 0
        self._tokens_saved = 0
        self._cost_saved = 0
