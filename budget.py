"""
Budget Module
Daily budget tracking and enforcement
"""

from typing import Dict
from . import config


class BudgetManager:
    """Manages daily budget tracking"""
    
    def __init__(self, daily_budget: float = config.DAILY_BUDGET):
        self._daily_budget = daily_budget
        self._remaining_budget = daily_budget
        self._total_spent = 0.0
    
    def can_afford(self, cost: float) -> bool:
        """
        Check if budget allows for this cost
        
        Args:
            cost: Estimated cost
            
        Returns:
            True if affordable, False otherwise
        """
        return self._remaining_budget >= cost
    
    def deduct(self, cost: float) -> bool:
        """
        Deduct cost from budget
        
        Args:
            cost: Amount to deduct
            
        Returns:
            True if successful, False if insufficient budget
        """
        if not self.can_afford(cost):
            return False
        
        self._remaining_budget -= cost
        self._total_spent += cost
        return True
    
    def get_stats(self) -> Dict:
        """Get budget statistics"""
        percentage = (self._total_spent / self._daily_budget * 100) if self._daily_budget > 0 else 0
        
        return {
            'daily_budget': self._daily_budget,
            'remaining': self._remaining_budget,
            'spent': self._total_spent,
            'percentage_used': percentage
        }
    
    def reset(self):
        """Reset budget (simulates new day)"""
        self._remaining_budget = self._daily_budget
        self._total_spent = 0.0
