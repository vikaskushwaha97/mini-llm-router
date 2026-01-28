"""
Decision Module
Contains all request classification and decision logic
"""

from typing import Dict
from datetime import datetime
import re

from . import config
from .cache import CacheManager
from .budget import BudgetManager
from .model_router import ModelRouter


class RequestClassifier:
    """Classifies incoming requests into categories"""

    @staticmethod
    def classify(prompt: str) -> str:
        """
        Classify request into one of:
        EMPTY, GARBAGE, SIMPLE, COMPLEX, LONG
        """

        # 1️⃣ None or invalid type
        if prompt is None or not isinstance(prompt, str):
            return config.CLASSIFICATION_EMPTY

        trimmed = prompt.strip()

        # 2️⃣ Empty or whitespace
        if not trimmed:
            return config.CLASSIFICATION_EMPTY

        # 3️⃣ Garbage: low alphabetic signal
        alpha_count = sum(c.isalpha() for c in trimmed)
        alpha_ratio = alpha_count / len(trimmed)

        if alpha_ratio < config.MIN_ALPHA_RATIO:
            return config.CLASSIFICATION_GARBAGE

        # 4️⃣ Garbage: extremely short
        if len(trimmed) <= config.GARBAGE_THRESHOLD:
            return config.CLASSIFICATION_GARBAGE

        # 5️⃣ Token estimation for length handling
        word_count = len(trimmed.split())
        estimated_tokens = int(word_count * config.TOKEN_MULTIPLIER)

        if estimated_tokens > config.MAX_TOKENS:
            return config.CLASSIFICATION_LONG

        # 6️⃣ Simple vs complex
        if word_count <= config.SIMPLE_THRESHOLD:
            return config.CLASSIFICATION_SIMPLE

        return config.CLASSIFICATION_COMPLEX


class DecisionEngine:
    """Main decision engine that orchestrates the routing pipeline"""

    def __init__(self, daily_budget: float = config.DAILY_BUDGET):
        self.classifier = RequestClassifier()
        self.router = ModelRouter()
        self.cache = CacheManager()
        self.budget = BudgetManager(daily_budget)
        self._request_count = 0

    def process_request(self, prompt: str) -> Dict:
        """Process a request through the complete routing pipeline"""

        self._request_count += 1
        timestamp = datetime.now().isoformat()

        # Step 1: Classification
        classification = self.classifier.classify(prompt)

        # Step 2: Reject empty / garbage
        if classification in (
            config.CLASSIFICATION_EMPTY,
            config.CLASSIFICATION_GARBAGE,
        ):
            return self._create_rejection_log(
                timestamp=timestamp,
                prompt=prompt,
                classification=classification,
                reason=f"{classification} input detected",
                decision=config.DECISION_REJECTED,
            )

        # Step 3: Cache lookup
        cached = self.cache.get(prompt)
        if cached:
            return self._create_cache_hit_log(
                timestamp=timestamp,
                prompt=prompt,
                classification=classification,
                cached_data=cached,
            )

        # Step 4: Token estimation
        tokens = self.router.estimate_tokens(prompt)

        # Step 5: Model selection
        model_config, selection_reason = self.router.select_model(classification)

        if model_config is None:
            return self._create_rejection_log(
                timestamp=timestamp,
                prompt=prompt,
                classification=classification,
                reason=selection_reason,
                decision=config.DECISION_REJECTED,
            )

        # Step 6: Cost estimation
        cost = self.router.calculate_cost(tokens, model_config)

        # Step 7: Budget enforcement
        if not self.budget.can_afford(cost):
            return self._create_rejection_log(
                timestamp=timestamp,
                prompt=prompt,
                classification=classification,
                reason="DAILY_BUDGET_EXCEEDED",
                decision=config.DECISION_REJECTED,
                tokens=tokens,
                model=model_config["name"],
                estimated_cost=cost,
            )

        # Step 8: Long prompt warning (graceful degradation)
        if classification == config.CLASSIFICATION_LONG:
            self.budget.deduct(cost)
            self.cache.set(prompt, tokens, model_config["name"], cost)

            return self._create_warning_log(
                timestamp=timestamp,
                prompt=prompt,
                classification=classification,
                tokens=tokens,
                model=model_config,
                cost=cost,
                reason=f"Extremely long prompt ({tokens} tokens)",
            )

        # Step 9: Successful execution
        self.budget.deduct(cost)
        self.cache.set(prompt, tokens, model_config["name"], cost)

        return self._create_success_log(
            timestamp=timestamp,
            prompt=prompt,
            classification=classification,
            tokens=tokens,
            model=model_config,
            cost=cost,
            reason=selection_reason,
        )

    # ---------- LOG HELPERS ----------

    def _create_success_log(
        self,
        timestamp: str,
        prompt: str,
        classification: str,
        tokens: int,
        model: Dict,
        cost: float,
        reason: str,
    ) -> Dict:
        budget_stats = self.budget.get_stats()

        return {
            "timestamp": timestamp,
            "request_id": self._request_count,
            "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            "classification": classification,
            "decision": config.DECISION_PROCESSED,
            "cache_hit": False,
            "tokens_estimated": tokens,
            "model_selected": model["name"],
            "model_type": model["type"],
            "model_changed": False,
            "selection_reason": reason,
            "cost_estimated": round(cost, 6),
            "remaining_budget": round(budget_stats["remaining"], 4),
            "status": config.STATUS_SUCCESS,
        }

    def _create_cache_hit_log(
        self,
        timestamp: str,
        prompt: str,
        classification: str,
        cached_data: Dict,
    ) -> Dict:
        cache_stats = self.cache.get_stats()

        return {
            "timestamp": timestamp,
            "request_id": self._request_count,
            "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            "classification": classification,
            "decision": config.DECISION_CACHE_HIT,
            "cache_hit": True,
            "tokens_estimated": cached_data["tokens"],
            "model_selected": cached_data["model"],
            "cost_estimated": 0.0,
            "cost_saved": round(cached_data["cost"], 6),
            "total_cache_savings": round(cache_stats["cost_saved"], 4),
            "selection_reason": "Exact cache match – zero cost",
            "status": config.STATUS_SUCCESS,
        }

    def _create_rejection_log(
        self,
        timestamp: str,
        prompt: str,
        classification: str,
        reason: str,
        decision: str,
        tokens: int = 0,
        model: str = "None",
        estimated_cost: float = 0.0,
    ) -> Dict:
        budget_stats = self.budget.get_stats()

        return {
            "timestamp": timestamp,
            "request_id": self._request_count,
            "prompt": prompt[:100] + "..." if prompt else "",
            "classification": classification,
            "decision": decision,
            "cache_hit": False,
            "tokens_estimated": tokens,
            "model_selected": model,
            "cost_estimated": round(estimated_cost, 6),
            "remaining_budget": round(budget_stats["remaining"], 4),
            "rejection_reason": reason,
            "status": config.STATUS_REJECTED,
        }

    def _create_warning_log(
        self,
        timestamp: str,
        prompt: str,
        classification: str,
        tokens: int,
        model: Dict,
        cost: float,
        reason: str,
    ) -> Dict:
        budget_stats = self.budget.get_stats()

        return {
            "timestamp": timestamp,
            "request_id": self._request_count,
            "prompt": prompt[:100] + "..." if len(prompt) > 100 else prompt,
            "classification": classification,
            "decision": config.DECISION_PROCESSED_WITH_WARNING,
            "cache_hit": False,
            "tokens_estimated": tokens,
            "model_selected": model["name"],
            "model_type": model["type"],
            "cost_estimated": round(cost, 6),
            "remaining_budget": round(budget_stats["remaining"], 4),
            "warning_reason": reason,
            "status": config.STATUS_WARNING,
        }

    # ---------- STATS & MAINTENANCE ----------

    def get_stats(self) -> Dict:
        return {
            "total_requests": self._request_count,
            "budget": self.budget.get_stats(),
            "cache": self.cache.get_stats(),
        }

    def reset_budget(self):
        self.budget.reset()

    def clear_cache(self):
        self.cache.clear()
