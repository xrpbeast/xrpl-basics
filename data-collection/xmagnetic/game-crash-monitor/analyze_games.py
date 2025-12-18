#!/usr/bin/env python3
"""
Game Crash Data Analyzer - Comprehensive Statistical Analysis & Predictions
===========================================================================

ARCHITECTURE OVERVIEW
--------------------
This analyzer processes JSONL game data to perform:
1. Basic statistics (mean, median, distributions)
2. Advanced statistical tests (runs test, autocorrelation)
3. Pattern detection (sequences, streaks, transitions)
4. Predictive modeling (9 different forecasting methods)
5. Player behavior analysis
6. Economic metrics (house edge, win rates)

ADDING NEW ANALYSIS METHODS
---------------------------
To add new analysis:
1. Create method in GameAnalyzer class: def analyze_your_feature(self) -> Dict[str, Any]
2. Add call in run_full_analysis() method around line 750
3. Follow existing patterns for error handling and empty data checks
4. Return dictionary with clear, descriptive keys

MODIFYING PREDICTIONS
--------------------
Prediction logic is in predict_next_outcome() starting at line 476:
- Add new prediction method by appending to predictions dict
- Consensus calculation uses median of values in 1.0-50.0x range
- Methods excluded from consensus: strings, booleans, values outside range

NAVIGATION MARKERS
-----------------
Search for these markers to jump to sections:
- # SECTION: Data Loading
- # SECTION: Basic Statistics
- # SECTION: Advanced Statistics
- # SECTION: Pattern Detection
- # SECTION: Predictions
- # SECTION: Player Analysis
- # SECTION: Display & Reporting

DATA FORMAT
----------
Input: JSONL file with game records, one JSON per line:
{
  "gameNumber": int,
  "currentCoef": float,  # Crash multiplier
  "totalBets": float,
  "totalWins": float,
  "bets": [{
    "wallet": str,
    "amount": float,
    "betResult": {"coef": float, "wonAmount": float, "result": bool}
  }],
  "timeStart": ISO8601,
  "timeEnd": ISO8601,
  ...
}

USAGE
-----
python analyze_games.py <jsonl_file> [--limit N] [--export-players]
"""

import json
import sys
import math
from datetime import datetime
from collections import defaultdict, Counter
from typing import Dict, List, Any, Tuple, Optional
import statistics


# =============================================================================
# SECTION: Core Analyzer Class
# =============================================================================

class GameAnalyzer:
    """Analyzes game crash data from JSONL file"""

    def __init__(self, filepath: str):
        """Initialize analyzer with path to JSONL data file"""
        self.filepath = filepath
        self.games: List[Dict[str, Any]] = []
        self.stats: Dict[str, Any] = {}

    # =========================================================================
    # SECTION: Data Loading
    # =========================================================================

    def load_data(self, limit: int = None) -> None:
        """Load games from JSONL file

        Args:
            limit: Maximum number of games to load (None = all)
        """
        print(f"Loading data from {self.filepath}...")
        count = 0

        with open(self.filepath, 'r') as f:
            for line in f:
                if limit and count >= limit:
                    break
                try:
                    game = json.loads(line.strip())
                    self.games.append(game)
                    count += 1
                except json.JSONDecodeError:
                    continue

        print(f"✓ Loaded {len(self.games):,} games")

    # =========================================================================
    # SECTION: Basic Statistics
    # =========================================================================

    def analyze_crash_coefficients(self) -> Dict[str, float]:
        """Analyze crash coefficient distribution"""
        coefs = [g['currentCoef'] for g in self.games if 'currentCoef' in g]

        if not coefs:
            return {}

        return {
            'mean': statistics.mean(coefs),
            'median': statistics.median(coefs),
            'min': min(coefs),
            'max': max(coefs),
            'stdev': statistics.stdev(coefs) if len(coefs) > 1 else 0,
            'total_games': len(coefs)
        }

    def analyze_bet_patterns(self) -> Dict[str, Any]:
        """Analyze betting patterns across all games"""
        games_with_bets = [g for g in self.games if g.get('totalBets', 0) > 0]
        all_bets = []

        for game in games_with_bets:
            all_bets.extend(game.get('bets', []))

        if not all_bets:
            return {'total_bets': 0, 'games_with_bets': 0}

        bet_amounts = [b['amount'] for b in all_bets if 'amount' in b]
        won_bets = [b for b in all_bets if b.get('betResult', {}).get('result', False)]

        return {
            'total_bets': len(all_bets),
            'games_with_bets': len(games_with_bets),
            'games_without_bets': len(self.games) - len(games_with_bets),
            'avg_bets_per_game': len(all_bets) / len(games_with_bets) if games_with_bets else 0,
            'avg_bet_amount': statistics.mean(bet_amounts) if bet_amounts else 0,
            'total_wagered': sum(bet_amounts) if bet_amounts else 0,
            'win_rate': len(won_bets) / len(all_bets) if all_bets else 0,
        }

    def analyze_player_behavior(self) -> Dict[str, Any]:
        """Analyze unique players and their behavior"""
        player_stats = defaultdict(lambda: {
            'total_bets': 0,
            'total_wagered': 0,
            'total_won': 0,
            'wins': 0,
            'losses': 0
        })

        for game in self.games:
            for bet in game.get('bets', []):
                wallet = bet.get('wallet')
                if not wallet:
                    continue

                amount = bet.get('amount', 0)
                player_stats[wallet]['total_bets'] += 1
                player_stats[wallet]['total_wagered'] += amount

                result = bet.get('betResult', {})
                if result.get('result', False):
                    player_stats[wallet]['wins'] += 1
                    player_stats[wallet]['total_won'] += result.get('wonAmount', 0)
                else:
                    player_stats[wallet]['losses'] += 1

        if not player_stats:
            return {'unique_players': 0}

        total_bets_list = [p['total_bets'] for p in player_stats.values()]
        wagered_list = [p['total_wagered'] for p in player_stats.values()]

        return {
            'unique_players': len(player_stats),
            'avg_bets_per_player': statistics.mean(total_bets_list),
            'avg_wagered_per_player': statistics.mean(wagered_list),
            'most_active_player_bets': max(total_bets_list),
            'player_stats': player_stats
        }

    def analyze_game_duration(self) -> Dict[str, float]:
        """Analyze game duration patterns"""
        durations = []

        for game in self.games:
            try:
                start = datetime.fromisoformat(game['timeStart'].replace('Z', '+00:00'))
                end = datetime.fromisoformat(game['timeEnd'].replace('Z', '+00:00'))
                duration = (end - start).total_seconds()
                durations.append(duration)
            except (KeyError, ValueError):
                continue

        if not durations:
            return {}

        return {
            'avg_duration_seconds': statistics.mean(durations),
            'median_duration_seconds': statistics.median(durations),
            'min_duration_seconds': min(durations),
            'max_duration_seconds': max(durations)
        }

    def analyze_economics(self) -> Dict[str, float]:
        """Analyze economic metrics (fees, burns, payouts)"""
        total_fees = sum(g.get('totalFees', 0) for g in self.games)
        total_mag_burned = sum(g.get('magBurned', 0) for g in self.games)
        total_bets = sum(g.get('totalBets', 0) for g in self.games)
        total_wins = sum(g.get('totalWins', 0) for g in self.games)

        return {
            'total_fees_collected': total_fees,
            'total_mag_burned': total_mag_burned,
            'total_wagered': total_bets,
            'total_paid_out': total_wins,
            'house_edge': ((total_bets - total_wins) / total_bets * 100) if total_bets > 0 else 0,
            'avg_fee_per_game': total_fees / len(self.games) if self.games else 0
        }

    def find_extreme_crashes(self, top_n: int = 10) -> List[Dict[str, Any]]:
        """Find games with highest crash coefficients

        Args:
            top_n: Number of top crashes to return

        Returns:
            List of games sorted by crash coefficient
        """
        sorted_games = sorted(
            self.games,
            key=lambda g: g.get('currentCoef', 0),
            reverse=True
        )
        return sorted_games[:top_n]

    def find_biggest_wins(self, top_n: int = 10) -> List[Tuple[Dict, Dict]]:
        """Find biggest individual bet wins

        Args:
            top_n: Number of top wins to return

        Returns:
            List of (game, bet) tuples sorted by win amount
        """
        all_wins = []

        for game in self.games:
            for bet in game.get('bets', []):
                result = bet.get('betResult', {})
                if result.get('result', False):
                    all_wins.append((game, bet))

        sorted_wins = sorted(
            all_wins,
            key=lambda x: x[1].get('betResult', {}).get('wonAmount', 0),
            reverse=True
        )

        return sorted_wins[:top_n]

    def analyze_cashout_timing(self) -> Dict[str, Any]:
        """Analyze when players cash out vs crash point"""
        early_cashouts = 0
        late_cashouts = 0
        total_cashouts = 0
        cashout_ratios = []

        for game in self.games:
            crash_coef = game.get('currentCoef', 0)
            for bet in game.get('bets', []):
                result = bet.get('betResult', {})
                if result.get('result', False):
                    total_cashouts += 1
                    cashout_coef = result.get('coef', 0)

                    if cashout_coef > 0 and crash_coef > 0:
                        ratio = cashout_coef / crash_coef
                        cashout_ratios.append(ratio)

                        if cashout_coef < crash_coef:
                            early_cashouts += 1
                        else:
                            late_cashouts += 1

        return {
            'total_cashouts': total_cashouts,
            'early_cashouts': early_cashouts,
            'late_cashouts': late_cashouts,
            'avg_cashout_ratio': statistics.mean(cashout_ratios) if cashout_ratios else 0,
            'median_cashout_ratio': statistics.median(cashout_ratios) if cashout_ratios else 0
        }

    def get_top_players(self, player_stats: Dict, metric: str, top_n: int = 10) -> List[Tuple[str, Dict]]:
        """Get top players by specific metric

        Args:
            player_stats: Dictionary of player statistics
            metric: Metric to sort by ('total_bets', 'total_wagered', 'total_won', 'win_rate', 'net_profit')
            top_n: Number of top players to return

        Returns:
            List of (wallet, stats) tuples
        """
        players_list = []
        for wallet, stats in player_stats.items():
            enriched_stats = stats.copy()
            enriched_stats['win_rate'] = stats['wins'] / stats['total_bets'] if stats['total_bets'] > 0 else 0
            enriched_stats['net_profit'] = stats['total_won'] - stats['total_wagered']
            players_list.append((wallet, enriched_stats))

        if metric == 'win_rate':
            # Filter out players with less than 10 bets for meaningful win rate
            players_list = [(w, s) for w, s in players_list if s['total_bets'] >= 10]

        sorted_players = sorted(players_list, key=lambda x: x[1][metric], reverse=True)
        return sorted_players[:top_n]

    # =========================================================================
    # SECTION: Advanced Statistics
    # =========================================================================

    def analyze_streaks(self) -> Dict[str, Any]:
        """Analyze streaks of consecutive high/low crashes"""
        coefs = [g['currentCoef'] for g in self.games if 'currentCoef' in g]

        if not coefs:
            return {}

        median_coef = statistics.median(coefs)
        current_streak = 0
        current_type = None
        streaks = {'high': [], 'low': []}

        for coef in coefs:
            is_high = coef >= median_coef
            streak_type = 'high' if is_high else 'low'

            if streak_type == current_type:
                current_streak += 1
            else:
                if current_type is not None:
                    streaks[current_type].append(current_streak)
                current_streak = 1
                current_type = streak_type

        if current_type is not None:
            streaks[current_type].append(current_streak)

        return {
            'median_crash': median_coef,
            'longest_high_streak': max(streaks['high']) if streaks['high'] else 0,
            'longest_low_streak': max(streaks['low']) if streaks['low'] else 0,
            'avg_high_streak': statistics.mean(streaks['high']) if streaks['high'] else 0,
            'avg_low_streak': statistics.mean(streaks['low']) if streaks['low'] else 0,
            'total_high_streaks': len(streaks['high']),
            'total_low_streaks': len(streaks['low']),
            'current_streak_type': current_type,
            'current_streak_length': current_streak
        }

    def analyze_autocorrelation(self, lag: int = 1) -> Dict[str, float]:
        """Calculate autocorrelation to detect dependencies between games

        Args:
            lag: Number of games to look back (default: 1 for adjacent games)

        Returns:
            Dictionary with autocorrelation coefficient
        """
        coefs = [g['currentCoef'] for g in self.games if 'currentCoef' in g]

        if len(coefs) < lag + 1:
            return {'autocorrelation': 0.0, 'lag': lag}

        mean_coef = statistics.mean(coefs)
        n = len(coefs) - lag

        numerator = sum((coefs[i] - mean_coef) * (coefs[i + lag] - mean_coef) for i in range(n))
        denominator = sum((coef - mean_coef) ** 2 for coef in coefs)

        autocorr = numerator / denominator if denominator != 0 else 0

        return {
            'autocorrelation': autocorr,
            'lag': lag,
            'interpretation': 'Random' if abs(autocorr) < 0.1 else ('Positive correlation' if autocorr > 0 else 'Negative correlation')
        }

    def runs_test(self) -> Dict[str, Any]:
        """Wald-Wolfowitz runs test for randomness"""
        coefs = [g['currentCoef'] for g in self.games if 'currentCoef' in g]

        if not coefs:
            return {}

        median = statistics.median(coefs)
        runs = []
        current_run = None
        run_count = 0

        n1 = sum(1 for c in coefs if c >= median)  # Above median
        n2 = len(coefs) - n1  # Below median

        for coef in coefs:
            above = coef >= median
            if current_run is None or current_run != above:
                if current_run is not None:
                    runs.append(run_count)
                current_run = above
                run_count = 1
            else:
                run_count += 1

        if run_count > 0:
            runs.append(run_count)

        r = len(runs)

        if n1 == 0 or n2 == 0:
            return {'total_runs': r, 'z_score': 0, 'interpretation': 'Insufficient data'}

        # Expected runs and standard deviation
        expected_runs = (2 * n1 * n2) / (n1 + n2) + 1
        std_runs = math.sqrt((2 * n1 * n2 * (2 * n1 * n2 - n1 - n2)) / ((n1 + n2) ** 2 * (n1 + n2 - 1)))

        # Z-score
        z_score = (r - expected_runs) / std_runs if std_runs != 0 else 0

        # Interpretation: |z| > 1.96 suggests non-randomness (95% confidence)
        if abs(z_score) < 1.96:
            interpretation = 'Random (passes test)'
        elif z_score > 1.96:
            interpretation = 'Too many runs (oscillating pattern)'
        else:
            interpretation = 'Too few runs (clustering pattern)'

        return {
            'total_runs': r,
            'expected_runs': expected_runs,
            'z_score': z_score,
            'interpretation': interpretation,
            'is_random': abs(z_score) < 1.96
        }

    def analyze_volatility(self, window: int = 20) -> Dict[str, Any]:
        """Analyze rolling volatility to detect variance clustering

        Args:
            window: Size of rolling window for volatility calculation
        """
        coefs = [g['currentCoef'] for g in self.games if 'currentCoef' in g]

        if len(coefs) < window:
            return {}

        volatilities = []
        for i in range(window, len(coefs)):
            window_data = coefs[i-window:i]
            vol = statistics.stdev(window_data)
            volatilities.append(vol)

        return {
            'avg_volatility': statistics.mean(volatilities) if volatilities else 0,
            'max_volatility': max(volatilities) if volatilities else 0,
            'min_volatility': min(volatilities) if volatilities else 0,
            'recent_volatility': volatilities[-1] if volatilities else 0,
            'volatility_trend': 'Increasing' if len(volatilities) > 1 and volatilities[-1] > statistics.mean(volatilities) else 'Stable/Decreasing'
        }

    def analyze_distribution(self) -> Dict[str, Any]:
        """Analyze crash coefficient distribution and compare to expected"""
        coefs = [g['currentCoef'] for g in self.games if 'currentCoef' in g]

        if not coefs:
            return {}

        # Create bins for distribution
        bin_ranges = [(1.0, 1.5), (1.5, 2.0), (2.0, 2.5), (2.5, 3.0), (3.0, 5.0), (5.0, 10.0), (10.0, float('inf'))]
        bin_labels = ['1.0-1.5x', '1.5-2.0x', '2.0-2.5x', '2.5-3.0x', '3.0-5.0x', '5.0-10.0x', '10.0x+']

        distribution = Counter()
        for coef in coefs:
            for i, (lower, upper) in enumerate(bin_ranges):
                if lower <= coef < upper:
                    distribution[bin_labels[i]] += 1
                    break
            else:
                # For values >= 10.0 (or any edge case)
                distribution[bin_labels[-1]] += 1

        # Calculate percentages
        total = len(coefs)
        dist_pct = {label: (count / total * 100) for label, count in distribution.items()}

        return {
            'distribution': dict(distribution),
            'distribution_pct': dist_pct,
            'below_2x': sum(1 for c in coefs if c < 2.0) / total * 100,
            'above_5x': sum(1 for c in coefs if c >= 5.0) / total * 100,
            'above_10x': sum(1 for c in coefs if c >= 10.0) / total * 100
        }

    # =========================================================================
    # SECTION: Pattern Detection
    # =========================================================================

    def find_patterns(self, pattern_length: int = 3, top_n: int = 10) -> List[Tuple[Tuple, int]]:
        """Find most common crash patterns (sequences)

        Args:
            pattern_length: Length of patterns to search for
            top_n: Number of top patterns to return
        """
        coefs = [g['currentCoef'] for g in self.games if 'currentCoef' in g]

        if len(coefs) < pattern_length:
            return []

        # Discretize coefficients into categories
        def categorize(coef):
            if coef < 1.5:
                return 'VL'  # Very Low
            elif coef < 2.0:
                return 'L'   # Low
            elif coef < 3.0:
                return 'M'   # Medium
            elif coef < 5.0:
                return 'H'   # High
            else:
                return 'VH'  # Very High

        patterns = []
        for i in range(len(coefs) - pattern_length + 1):
            pattern = tuple(categorize(coefs[i + j]) for j in range(pattern_length))
            patterns.append(pattern)

        pattern_counts = Counter(patterns)
        return pattern_counts.most_common(top_n)

    # =========================================================================
    # SECTION: Predictions
    # =========================================================================

    def predict_next_outcome(self, prediction_methods: Optional[List[str]] = None) -> Dict[str, Any]:
        """Predict next crash coefficient using multiple methods

        HOW TO EXTEND:
        --------------
        1. Add your prediction method within this function
        2. Store result in predictions dict with descriptive key
        3. Result will auto-include in consensus if 1.0 <= value <= 50.0
        4. Add display logic in run_full_analysis() around line 910

        Args:
            prediction_methods: List of methods to use (None = all)
                Available: 'sma', 'ema', 'wma', 'pattern', 'median', 'mode_range'

        Returns:
            Dictionary with prediction values and metadata:
            - Individual predictions (sma_10, ema, wma, etc.)
            - consensus: Median of valid predictions
            - confidence: 'High', 'Medium', or 'Low' based on std dev
            - trend: 'Increasing', 'Decreasing', or 'Stable'
            - recent_10_avg, recent_10_min, recent_10_max: Context
        """
        coefs = [g['currentCoef'] for g in self.games if 'currentCoef' in g]

        if len(coefs) < 10:
            return {'error': 'Insufficient data for prediction'}

        predictions = {}

        # Simple Moving Average (last 10, 50, 100 games)
        if not prediction_methods or 'sma' in prediction_methods:
            predictions['sma_10'] = statistics.mean(coefs[-10:])
            if len(coefs) >= 50:
                predictions['sma_50'] = statistics.mean(coefs[-50:])
            if len(coefs) >= 100:
                predictions['sma_100'] = statistics.mean(coefs[-100:])

        # Exponential Moving Average (more weight on recent)
        if not prediction_methods or 'ema' in prediction_methods:
            alpha = 0.2  # Smoothing factor
            ema = coefs[0]
            for coef in coefs[1:]:
                ema = alpha * coef + (1 - alpha) * ema
            predictions['ema'] = ema

        # Weighted Moving Average (linear decay)
        if not prediction_methods or 'wma' in prediction_methods:
            recent = coefs[-20:] if len(coefs) >= 20 else coefs
            weights = list(range(1, len(recent) + 1))
            wma = sum(c * w for c, w in zip(recent, weights)) / sum(weights)
            predictions['wma'] = wma

        # Pattern-based prediction (find similar recent sequences)
        if not prediction_methods or 'pattern' in prediction_methods:
            if len(coefs) >= 6:
                last_pattern = coefs[-5:]  # Last 5 games
                similar_outcomes = []

                for i in range(len(coefs) - 6):
                    pattern = coefs[i:i+5]
                    # Calculate similarity (inverse of mean squared difference)
                    diff = sum((a - b) ** 2 for a, b in zip(pattern, last_pattern))
                    if diff < 2.0:  # Similar patterns
                        similar_outcomes.append(coefs[i+5])

                if similar_outcomes:
                    predictions['pattern_based'] = statistics.mean(similar_outcomes)
                    predictions['pattern_matches'] = len(similar_outcomes)

        # Statistical measures
        if not prediction_methods or 'median' in prediction_methods:
            predictions['median'] = statistics.median(coefs)

        # Mode range (most common range)
        if not prediction_methods or 'mode_range' in prediction_methods:
            ranges = []
            for coef in coefs[-100:] if len(coefs) >= 100 else coefs:
                if coef < 1.5:
                    ranges.append(1.2)
                elif coef < 2.0:
                    ranges.append(1.7)
                elif coef < 3.0:
                    ranges.append(2.5)
                elif coef < 5.0:
                    ranges.append(4.0)
                else:
                    ranges.append(7.0)

            if ranges:
                predictions['mode_range'] = statistics.mode(ranges)

        # Trend-adjusted prediction
        if len(coefs) >= 20:
            recent_avg = statistics.mean(coefs[-10:])
            older_avg = statistics.mean(coefs[-20:-10])
            trend = recent_avg - older_avg
            trend_pred = recent_avg + (trend * 0.5)  # 50% trend continuation
            predictions['trend_adjusted'] = max(1.0, trend_pred)  # Never predict below 1.0x
            predictions['trend'] = 'Increasing' if trend > 0.1 else ('Decreasing' if trend < -0.1 else 'Stable')

        # Calculate consensus prediction (average of all methods, excluding outliers)
        valid_predictions = [v for v in predictions.values() if isinstance(v, (int, float)) and 1.0 <= v <= 50.0]
        if valid_predictions:
            # Use median for robustness against outliers
            predictions['consensus'] = statistics.median(valid_predictions)
            predictions['prediction_std'] = statistics.stdev(valid_predictions) if len(valid_predictions) > 1 else 0
            predictions['confidence'] = 'High' if predictions['prediction_std'] < 0.5 else ('Medium' if predictions['prediction_std'] < 1.5 else 'Low')

        # Recent statistics for context
        predictions['recent_10_avg'] = statistics.mean(coefs[-10:])
        predictions['recent_10_min'] = min(coefs[-10:])
        predictions['recent_10_max'] = max(coefs[-10:])
        predictions['last_game'] = coefs[-1]

        return predictions

    def analyze_conditional_probabilities(self) -> Dict[str, Any]:
        """Analyze conditional probabilities (e.g., P(high | after low))"""
        coefs = [g['currentCoef'] for g in self.games if 'currentCoef' in g]

        if len(coefs) < 2:
            return {}

        median = statistics.median(coefs)

        # Count transitions
        transitions = {
            'low_to_low': 0,
            'low_to_high': 0,
            'high_to_low': 0,
            'high_to_high': 0
        }

        for i in range(len(coefs) - 1):
            current_high = coefs[i] >= median
            next_high = coefs[i + 1] >= median

            if current_high and next_high:
                transitions['high_to_high'] += 1
            elif current_high and not next_high:
                transitions['high_to_low'] += 1
            elif not current_high and next_high:
                transitions['low_to_high'] += 1
            else:
                transitions['low_to_low'] += 1

        total_after_low = transitions['low_to_low'] + transitions['low_to_high']
        total_after_high = transitions['high_to_low'] + transitions['high_to_high']

        return {
            'prob_high_after_low': transitions['low_to_high'] / total_after_low if total_after_low > 0 else 0,
            'prob_low_after_low': transitions['low_to_low'] / total_after_low if total_after_low > 0 else 0,
            'prob_high_after_high': transitions['high_to_high'] / total_after_high if total_after_high > 0 else 0,
            'prob_low_after_high': transitions['high_to_low'] / total_after_high if total_after_high > 0 else 0,
            'median_threshold': median,
            'transitions': transitions
        }

    # =========================================================================
    # SECTION: Display & Reporting
    # =========================================================================

    def run_full_analysis(self) -> None:
        """Run complete analysis and display results"""
        print("\n" + "="*60)
        print("GAME CRASH DATA ANALYSIS")
        print("="*60)

        # Crash Coefficients
        print("\n📊 CRASH COEFFICIENT ANALYSIS")
        print("-"*60)
        crash_stats = self.analyze_crash_coefficients()
        for key, value in crash_stats.items():
            if key == 'total_games':
                print(f"{key:20}: {value:,}")
            else:
                print(f"{key:20}: {value:.2f}")

        # Betting Patterns
        print("\n🎲 BETTING PATTERNS")
        print("-"*60)
        bet_stats = self.analyze_bet_patterns()
        for key, value in bet_stats.items():
            if isinstance(value, float):
                if 'rate' in key:
                    print(f"{key:20}: {value:.2%}")
                else:
                    print(f"{key:20}: {value:,.2f}")
            else:
                print(f"{key:20}: {value:,}")

        # Player Behavior
        print("\n👥 PLAYER BEHAVIOR")
        print("-"*60)
        player_stats = self.analyze_player_behavior()
        for key, value in player_stats.items():
            if key == 'player_stats':
                continue
            if isinstance(value, float):
                print(f"{key:20}: {value:,.2f}")
            else:
                print(f"{key:20}: {value:,}")

        # Game Duration
        print("\n⏱️  GAME DURATION")
        print("-"*60)
        duration_stats = self.analyze_game_duration()
        for key, value in duration_stats.items():
            print(f"{key:20}: {value:.2f}s ({value/60:.2f}m)")

        # Economics
        print("\n💰 ECONOMIC METRICS")
        print("-"*60)
        econ_stats = self.analyze_economics()
        for key, value in econ_stats.items():
            if 'edge' in key or 'rate' in key:
                print(f"{key:20}: {value:.2f}%")
            else:
                print(f"{key:20}: {value:,.2f}")

        # Cashout Timing
        print("\n⏰ CASHOUT TIMING ANALYSIS")
        print("-"*60)
        cashout_stats = self.analyze_cashout_timing()
        for key, value in cashout_stats.items():
            if 'ratio' in key:
                print(f"{key:20}: {value:.2%}")
            else:
                print(f"{key:20}: {value:,}")

        # Top Players Sections
        player_behavior = self.analyze_player_behavior()
        player_stats_dict = player_behavior.get('player_stats', {})

        if player_stats_dict:
            # Most Active Players
            print("\n🎯 TOP 10 MOST ACTIVE PLAYERS (by total bets)")
            print("-"*60)
            top_active = self.get_top_players(player_stats_dict, 'total_bets', 10)
            for i, (wallet, stats) in enumerate(top_active, 1):
                print(f"{i:2}. {wallet}: {stats['total_bets']:,} bets | "
                      f"Win rate: {stats['win_rate']:.1%} | "
                      f"Net: {stats['net_profit']:+.2f}")

            # Highest Wagered
            print("\n💸 TOP 10 HIGHEST WAGERED (by total amount)")
            print("-"*60)
            top_wagered = self.get_top_players(player_stats_dict, 'total_wagered', 10)
            for i, (wallet, stats) in enumerate(top_wagered, 1):
                print(f"{i:2}. {wallet}: {stats['total_wagered']:,.2f} wagered | "
                      f"{stats['total_bets']:,} bets | "
                      f"Net: {stats['net_profit']:+,.2f}")

            # Biggest Winners
            print("\n🤑 TOP 10 BIGGEST WINNERS (by total won)")
            print("-"*60)
            top_winners = self.get_top_players(player_stats_dict, 'total_won', 10)
            for i, (wallet, stats) in enumerate(top_winners, 1):
                print(f"{i:2}. {wallet}: {stats['total_won']:,.2f} won | "
                      f"Wagered: {stats['total_wagered']:,.2f} | "
                      f"Net: {stats['net_profit']:+,.2f}")

            # Most Profitable
            print("\n📈 TOP 10 MOST PROFITABLE PLAYERS (by net profit)")
            print("-"*60)
            top_profit = self.get_top_players(player_stats_dict, 'net_profit', 10)
            for i, (wallet, stats) in enumerate(top_profit, 1):
                print(f"{i:2}. {wallet}: {stats['net_profit']:+,.2f} profit | "
                      f"Win rate: {stats['win_rate']:.1%} | "
                      f"{stats['total_bets']:,} bets")

            # Best Win Rates (min 10 bets)
            print("\n🎲 TOP 10 BEST WIN RATES (min 10 bets)")
            print("-"*60)
            top_winrate = self.get_top_players(player_stats_dict, 'win_rate', 10)
            for i, (wallet, stats) in enumerate(top_winrate, 1):
                print(f"{i:2}. {wallet}: {stats['win_rate']:.1%} | "
                      f"{stats['wins']}/{stats['total_bets']} wins | "
                      f"Net: {stats['net_profit']:+,.2f}")

        # Extreme Crashes
        print("\n🚀 TOP 10 HIGHEST CRASHES")
        print("-"*60)
        top_crashes = self.find_extreme_crashes(10)
        for i, game in enumerate(top_crashes, 1):
            print(f"{i:2}. Game #{game['gameNumber']:,}: {game['currentCoef']:.2f}x")

        # Biggest Wins
        print("\n🏆 TOP 10 BIGGEST WINS")
        print("-"*60)
        top_wins = self.find_biggest_wins(10)
        for i, (game, bet) in enumerate(top_wins, 1):
            result = bet['betResult']
            wallet = bet.get('wallet', 'Unknown')
            print(f"{i:2}. {result['wonAmount']:.2f} (bet: {bet['amount']:.2f} @ {result['coef']:.2f}x)")
            print(f"    Wallet: {wallet} | Game #{game['gameNumber']}")

        # Advanced Statistical Tests
        print("\n📐 ADVANCED STATISTICAL TESTS")
        print("-"*60)

        # Runs Test
        runs_stats = self.runs_test()
        if runs_stats:
            print(f"Runs Test:")
            print(f"  Total runs: {runs_stats.get('total_runs', 0):,}")
            print(f"  Expected runs: {runs_stats.get('expected_runs', 0):.2f}")
            print(f"  Z-score: {runs_stats.get('z_score', 0):.3f}")
            print(f"  Result: {runs_stats.get('interpretation', 'N/A')}")
            print(f"  Is random: {'✅ YES' if runs_stats.get('is_random', False) else '❌ NO'}")

        # Autocorrelation
        print(f"\nAutocorrelation (lag-1):")
        autocorr = self.analyze_autocorrelation(lag=1)
        print(f"  Coefficient: {autocorr.get('autocorrelation', 0):.3f}")
        print(f"  Interpretation: {autocorr.get('interpretation', 'N/A')}")

        # Streaks Analysis
        print("\n🔥 STREAKS ANALYSIS")
        print("-"*60)
        streak_stats = self.analyze_streaks()
        if streak_stats:
            print(f"Median crash point: {streak_stats.get('median_crash', 0):.2f}x")
            print(f"Longest high streak: {streak_stats.get('longest_high_streak', 0):,} games")
            print(f"Longest low streak: {streak_stats.get('longest_low_streak', 0):,} games")
            print(f"Average high streak: {streak_stats.get('avg_high_streak', 0):.2f} games")
            print(f"Average low streak: {streak_stats.get('avg_low_streak', 0):.2f} games")
            print(f"Current streak: {streak_stats.get('current_streak_length', 0)} {streak_stats.get('current_streak_type', 'N/A')} games")

        # Distribution Analysis
        print("\n📊 DISTRIBUTION ANALYSIS")
        print("-"*60)
        dist_stats = self.analyze_distribution()
        if dist_stats:
            print("Crash ranges:")
            for label, count in dist_stats.get('distribution', {}).items():
                pct = dist_stats.get('distribution_pct', {}).get(label, 0)
                print(f"  {label:12}: {count:6,} games ({pct:5.2f}%)")
            print(f"\nBelow 2.0x: {dist_stats.get('below_2x', 0):.2f}%")
            print(f"Above 5.0x: {dist_stats.get('above_5x', 0):.2f}%")
            print(f"Above 10.0x: {dist_stats.get('above_10x', 0):.2f}%")

        # Volatility Analysis
        print("\n📉 VOLATILITY ANALYSIS")
        print("-"*60)
        vol_stats = self.analyze_volatility(window=20)
        if vol_stats:
            print(f"Average volatility: {vol_stats.get('avg_volatility', 0):.3f}")
            print(f"Recent volatility: {vol_stats.get('recent_volatility', 0):.3f}")
            print(f"Max volatility: {vol_stats.get('max_volatility', 0):.3f}")
            print(f"Min volatility: {vol_stats.get('min_volatility', 0):.3f}")
            print(f"Trend: {vol_stats.get('volatility_trend', 'N/A')}")

        # Conditional Probabilities
        print("\n🎯 CONDITIONAL PROBABILITIES")
        print("-"*60)
        cond_prob = self.analyze_conditional_probabilities()
        if cond_prob:
            print(f"Median threshold: {cond_prob.get('median_threshold', 0):.2f}x")
            print(f"P(High | after Low): {cond_prob.get('prob_high_after_low', 0):.1%}")
            print(f"P(Low | after Low): {cond_prob.get('prob_low_after_low', 0):.1%}")
            print(f"P(High | after High): {cond_prob.get('prob_high_after_high', 0):.1%}")
            print(f"P(Low | after High): {cond_prob.get('prob_low_after_high', 0):.1%}")

        # Pattern Recognition
        print("\n🔍 TOP 10 MOST COMMON PATTERNS (3-game sequences)")
        print("-"*60)
        patterns = self.find_patterns(pattern_length=3, top_n=10)
        if patterns:
            pattern_legend = "VL=<1.5x, L=1.5-2x, M=2-3x, H=3-5x, VH=>5x"
            print(f"Legend: {pattern_legend}")
            for i, (pattern, count) in enumerate(patterns, 1):
                pattern_str = '-'.join(pattern)
                pct = (count / (len(self.games) - 2)) * 100 if len(self.games) > 2 else 0
                print(f"{i:2}. {pattern_str:12} → {count:5,} times ({pct:4.2f}%)")

        # PREDICTION SECTION
        print("\n" + "="*60)
        print("🔮 NEXT OUTCOME PREDICTIONS")
        print("="*60)

        predictions = self.predict_next_outcome()
        if 'error' not in predictions:
            # Show recent context
            print(f"\n📍 RECENT CONTEXT")
            print(f"   Last game: {predictions.get('last_game', 0):.2f}x")
            print(f"   Recent 10 avg: {predictions.get('recent_10_avg', 0):.2f}x")
            print(f"   Recent 10 range: {predictions.get('recent_10_min', 0):.2f}x - {predictions.get('recent_10_max', 0):.2f}x")
            if 'trend' in predictions:
                print(f"   Trend: {predictions['trend']}")

            # Show all prediction methods
            print(f"\n📊 PREDICTION METHODS")
            print("-"*60)

            if 'sma_10' in predictions:
                print(f"SMA (10 games):      {predictions['sma_10']:.2f}x")
            if 'sma_50' in predictions:
                print(f"SMA (50 games):      {predictions['sma_50']:.2f}x")
            if 'sma_100' in predictions:
                print(f"SMA (100 games):     {predictions['sma_100']:.2f}x")
            if 'ema' in predictions:
                print(f"EMA (exponential):   {predictions['ema']:.2f}x")
            if 'wma' in predictions:
                print(f"WMA (weighted):      {predictions['wma']:.2f}x")
            if 'pattern_based' in predictions:
                matches = predictions.get('pattern_matches', 0)
                print(f"Pattern-based:       {predictions['pattern_based']:.2f}x ({matches} similar)")
            if 'median' in predictions:
                print(f"Historical median:   {predictions['median']:.2f}x")
            if 'mode_range' in predictions:
                print(f"Most common range:   {predictions['mode_range']:.2f}x")
            if 'trend_adjusted' in predictions:
                print(f"Trend-adjusted:      {predictions['trend_adjusted']:.2f}x")

            # Consensus prediction
            if 'consensus' in predictions:
                print(f"\n{'='*60}")
                print(f"🎯 CONSENSUS PREDICTION: {predictions['consensus']:.2f}x")
                print(f"   Confidence: {predictions.get('confidence', 'Unknown')}")
                print(f"   Std deviation: ±{predictions.get('prediction_std', 0):.2f}x")
                print(f"{'='*60}")

                # Interpretation
                consensus = predictions['consensus']
                if consensus < 1.5:
                    print(f"⚠️  Prediction suggests VERY LOW crash (high risk)")
                elif consensus < 2.0:
                    print(f"⚠️  Prediction suggests LOW crash")
                elif consensus < 3.0:
                    print(f"✅ Prediction suggests MEDIUM crash")
                elif consensus < 5.0:
                    print(f"🚀 Prediction suggests HIGH crash")
                else:
                    print(f"🚀 Prediction suggests VERY HIGH crash")

                print(f"\n⚠️  DISCLAIMER: Predictions are statistical estimates only.")
                print(f"    Past performance does not guarantee future results.")
                print(f"    This game has a house edge - you will lose money over time.")
        else:
            print(f"\n⚠️  {predictions.get('error', 'Unable to generate predictions')}")

        print("\n" + "="*60)
        print("ANALYSIS COMPLETE")
        print("="*60 + "\n")

    def export_player_stats(self, output_file: str = 'player_stats.json') -> None:
        """Export detailed player statistics to JSON file

        Args:
            output_file: Path to output JSON file
        """
        player_stats = self.analyze_player_behavior()

        # Convert to serializable format
        export_data = []
        for wallet, stats in player_stats.get('player_stats', {}).items():
            export_data.append({
                'wallet': wallet,
                **stats,
                'win_rate': stats['wins'] / stats['total_bets'] if stats['total_bets'] > 0 else 0,
                'net_profit': stats['total_won'] - stats['total_wagered']
            })

        # Sort by total wagered
        export_data.sort(key=lambda x: x['total_wagered'], reverse=True)

        with open(output_file, 'w') as f:
            json.dump(export_data, f, indent=2)

        print(f"✓ Player statistics exported to {output_file}")


def main():
    """Main entry point"""
    if len(sys.argv) < 2:
        print("Usage: python analyze_games.py <jsonl_file> [--limit N] [--export-players]")
        print("\nOptions:")
        print("  --limit N         : Analyze only first N games (default: all)")
        print("  --export-players  : Export detailed player stats to player_stats.json")
        sys.exit(1)

    filepath = sys.argv[1]
    limit = None
    export_players = False

    # Parse arguments
    i = 2
    while i < len(sys.argv):
        if sys.argv[i] == '--limit' and i + 1 < len(sys.argv):
            limit = int(sys.argv[i + 1])
            i += 2
        elif sys.argv[i] == '--export-players':
            export_players = True
            i += 1
        else:
            i += 1

    # Run analysis
    analyzer = GameAnalyzer(filepath)
    analyzer.load_data(limit=limit)
    analyzer.run_full_analysis()

    if export_players:
        analyzer.export_player_stats()


if __name__ == '__main__':
    main()
