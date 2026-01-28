"""
Configuration Module
Contains all costs, limits, and thresholds for the routing engine
"""

# Model configurations
CHEAP_MODEL = {
    'name': 'gpt-3.5-turbo',
    'cost_per_1k': 0.0005,  # $0.0005 per 1K tokens
    'type': 'cheap'
}

STRONG_MODEL = {
    'name': 'gpt-4',
    'cost_per_1k': 0.003,   # $0.003 per 1K tokens
    'type': 'strong'
}

# Budget settings
DAILY_BUDGET = 10.0  # $10 daily budget limit

# Token estimation settings
TOKEN_MULTIPLIER = 1.3  # Heuristic: tokens ≈ 1.3 × words
MAX_TOKENS = 2000  # Maximum safe token threshold for LONG classification

# Classification thresholds
GARBAGE_THRESHOLD = 2  # Characters <= this are GARBAGE
SIMPLE_THRESHOLD = 10  # Word count <= this is SIMPLE
GARBAGE_THRESHOLD = 2        # Characters <= this are GARBAGE
SIMPLE_THRESHOLD = 10        # Word count <= this is SIMPLE
MIN_ALPHA_RATIO = 0.3        # At least 30% alphabetic characters


# Request classifications
CLASSIFICATION_EMPTY = 'EMPTY'
CLASSIFICATION_GARBAGE = 'GARBAGE'
CLASSIFICATION_SIMPLE = 'SIMPLE'
CLASSIFICATION_COMPLEX = 'COMPLEX'
CLASSIFICATION_LONG = 'LONG'

# Decision types
DECISION_PROCESSED = 'PROCESSED'
DECISION_PROCESSED_WITH_WARNING = 'PROCESSED_WITH_WARNING'
DECISION_REJECTED = 'REJECTED'
DECISION_CACHE_HIT = 'CACHE_HIT'

# Status types
STATUS_SUCCESS = 'SUCCESS'
STATUS_WARNING = 'WARNING'
STATUS_REJECTED = 'REJECTED'
