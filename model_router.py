"""
Model Router Module
Handles model selection and cost calculation
"""

from typing import Tuple, Dict
from . import config


class ModelRouter:
    """Handles model selection based on request classification"""
    
    @staticmethod
    def select_model(classification: str) -> Tuple[Dict, str]:
        """
        Select appropriate model based on request classification
        
        Args:
            classification: Request category (SIMPLE, COMPLEX, LONG, etc.)
            
        Returns:
            Tuple of (model_config, selection_reason)
        """
        if classification == config.CLASSIFICATION_SIMPLE:
            return (
                config.CHEAP_MODEL,
                'Simple query - using cost-efficient model'
            )
        elif classification in [config.CLASSIFICATION_COMPLEX, config.CLASSIFICATION_LONG]:
            return (
                config.STRONG_MODEL,
                f'{classification.title()} query - requires advanced model'
            )
        else:
            return (
                None,
                f'Invalid classification: {classification}'
            )
    
    @staticmethod
    def calculate_cost(tokens: int, model_config: Dict) -> float:
        """
        Calculate cost based on tokens and model
        
        Args:
            tokens: Estimated token count
            model_config: Model configuration dict
            
        Returns:
            Estimated cost in dollars
        """
        if model_config is None:
            return 0.0
        
        cost_per_1k = model_config.get('cost_per_1k', 0.0)
        return (tokens / 1000) * cost_per_1k
    
    @staticmethod
    def estimate_tokens(prompt: str) -> int:
        """
        Estimate tokens using heuristic
        
        Args:
            prompt: Input text
            
        Returns:
            Estimated token count
        """
        if not prompt or not prompt.strip():
            return 0
        
        word_count = len(prompt.strip().split())
        return int(word_count * config.TOKEN_MULTIPLIER)
