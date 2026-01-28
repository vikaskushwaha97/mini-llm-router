"""
Logger Module
Handles structured, color-coded logging output
"""

import json
from typing import Dict
from . import config


class Logger:
    """Handles structured logging with color-coded output"""

    # ANSI color codes
    COLORS = {
        'RESET': '\033[0m',
        'RED': '\033[91m',
        'GREEN': '\033[92m',
        'YELLOW': '\033[93m',
        'BLUE': '\033[94m',
        'MAGENTA': '\033[95m',
        'CYAN': '\033[96m',
        'WHITE': '\033[97m',
        'BOLD': '\033[1m',
    }

    @staticmethod
    def _colorize(text: str, color: str) -> str:
        """Add ANSI color to text"""
        return f"{Logger.COLORS.get(color, '')}{text}{Logger.COLORS['RESET']}"

    @staticmethod
    def print_header():
        """Print CLI header"""
        print("\n" + "=" * 70)
        print(Logger._colorize("🚀 MINI LLM ROUTING ENGINE - REQUEST LOG", 'BOLD'))
        print("=" * 70 + "\n")

    @staticmethod
    def print_log(log_data: Dict):
        """Print structured request log"""

        status = log_data.get('status', 'UNKNOWN')

        # Status color
        if status == config.STATUS_SUCCESS:
            color, icon = 'GREEN', '✅'
        elif status == config.STATUS_WARNING:
            color, icon = 'YELLOW', '⚠️'
        elif status == config.STATUS_REJECTED:
            color, icon = 'RED', '❌'
        else:
            color, icon = 'WHITE', 'ℹ️'

        print(Logger._colorize(
            f"\n{icon} REQUEST #{log_data['request_id']} - {status}",
            'BOLD'
        ))
        print(Logger._colorize("-" * 70, color))

        # Basic info
        print(f"⏰ Timestamp: {log_data['timestamp']}")
        print(f"📝 Prompt: {log_data['prompt']}")

        # Classification
        classification_color = {
            config.CLASSIFICATION_SIMPLE: 'CYAN',
            config.CLASSIFICATION_COMPLEX: 'MAGENTA',
            config.CLASSIFICATION_LONG: 'YELLOW',
            config.CLASSIFICATION_EMPTY: 'RED',
            config.CLASSIFICATION_GARBAGE: 'RED'
        }.get(log_data['classification'], 'WHITE')

        print(
            f"🏷️  Classification: "
            f"{Logger._colorize(log_data['classification'], classification_color)}"
        )

        # Decision
        decision = log_data['decision']
        print(f"⚖️  Decision: {Logger._colorize(decision, color)}")

        # Cache info
        if log_data.get('cache_hit'):
            saved = f"${log_data.get('cost_saved', 0):.6f}"
            print(Logger._colorize(f"💾 Cache: HIT (saved {saved})", 'GREEN'))
        else:
            print("💾 Cache: MISS")

        # Token & model
        print(f"🔢 Tokens Estimated: {log_data['tokens_estimated']}")
        print(f"🤖 Model Selected: {log_data['model_selected']}")

        # Cost info
        cost = log_data.get('cost_estimated', 0)
        if cost > 0:
            print(f"💰 Cost Estimated: ${cost:.6f}")
            print(f"💵 Remaining Budget: ${log_data.get('remaining_budget', 0):.4f}")
        elif log_data.get('cache_hit'):
            print(Logger._colorize("💰 Cost: $0.00 (Cache Hit!)", 'GREEN'))
            print(
                f"💵 Total Cache Savings: "
                f"${log_data.get('total_cache_savings', 0):.4f}"
            )

        # Reason
        if 'selection_reason' in log_data:
            print(f"📋 Reason: {log_data['selection_reason']}")
        elif 'rejection_reason' in log_data:
            print(f"📋 Reason: {log_data['rejection_reason']}")
        elif 'warning_reason' in log_data:
            print(f"📋 Reason: {log_data['warning_reason']}")

        # Model changed
        if 'model_changed' in log_data:
            if log_data['model_changed']:
                print(Logger._colorize("🔄 Model Changed: YES", 'YELLOW'))
            else:
                print("🔄 Model Changed: NO")

        print(Logger._colorize("-" * 70, color))

    @staticmethod
    def print_stats(stats: Dict):
        """Print system-level statistics"""

        print("\n" + "=" * 70)
        print(Logger._colorize("📊 SYSTEM STATISTICS", 'BOLD'))
        print("=" * 70)

        # Requests
        print(f"\n📈 Total Requests: {stats['total_requests']}")

        # Budget
        budget = stats['budget']
        pct = budget['percentage_used']
        budget_color = 'GREEN' if pct < 50 else ('YELLOW' if pct < 80 else 'RED')

        print("\n💰 Budget Information:")
        print(f"   Daily Budget: ${budget['daily_budget']:.2f}")
        print(f"   Spent: ${budget['spent']:.4f}")

        remaining_str = f"${budget['remaining']:.4f}"
        print(
            f"   Remaining: "
            f"{Logger._colorize(remaining_str, budget_color)}"
        )

        usage_str = f"{pct:.1f}%"
        print(
            f"   Usage: "
            f"{Logger._colorize(usage_str, budget_color)}"
        )

        # Cache
        cache = stats['cache']
        total = cache['hits'] + cache['misses']
        hit_rate = (cache['hits'] / total * 100) if total > 0 else 0

        print("\n💾 Cache Information:")
        print(f"   Cache Size: {cache['cache_size']} entries")
        print(f"   Cache Hits: {cache['hits']}")
        print(f"   Cache Misses: {cache['misses']}")

        hit_rate_str = f"{hit_rate:.1f}%"
        print(
            f"   Hit Rate: "
            f"{Logger._colorize(hit_rate_str, 'GREEN' if hit_rate > 30 else 'YELLOW')}"
        )

        print(f"   Tokens Saved: {cache['tokens_saved']}")

        cost_saved_str = f"${cache['cost_saved']:.4f}"
        print(
            f"   Cost Saved: "
            f"{Logger._colorize(cost_saved_str, 'GREEN')}"
        )

        print("\n" + "=" * 70 + "\n")

    @staticmethod
    def print_json(data: Dict):
        """Print JSON-formatted output"""
        print(json.dumps(data, indent=2))
