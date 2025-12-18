# Game Data Analysis Guide

## Overview
`analyze_games.py` - comprehensive analysis tool for game crash data from `full_games.jsonl`

## Quick Start

```bash
# Analyze all games
python analyze_games.py data/full_games.jsonl

# Analyze first 10,000 games (faster for testing)
python analyze_games.py data/full_games.jsonl --limit 10000

# Export detailed player statistics
python analyze_games.py data/full_games.jsonl --export-players
```

## Features

### 1. Crash Coefficient Analysis
- Mean, median, min, max crash multipliers
- Standard deviation
- Distribution insights

### 2. Betting Patterns
- Total bets vs games without activity
- Average bets per game
- Average bet amounts
- Overall win rate
- Total wagered amount

### 3. Player Behavior
- Unique player count
- Average bets per player
- Most active players
- Player-specific win/loss records

### 4. Game Duration
- Average game length
- Duration distribution
- Min/max game times

### 5. Economic Metrics
- Total fees collected
- MAG tokens burned
- House edge calculation
- Total payouts vs wagers

### 6. Cashout Timing
- Early vs late cashouts
- Cashout coefficient ratios
- Player risk behavior patterns

### 7. Top Lists
- Highest crash multipliers
- Biggest individual wins
- Most profitable players (when exported)

## Output Files

### player_stats.json
When using `--export-players`, generates detailed per-wallet statistics:
- Total bets and wagered amounts
- Win/loss records
- Win rates
- Net profit/loss
- Sorted by total wagered (highest first)

## Data Structure

### Game Object
```json
{
  "gameNumber": 123,
  "timeStart": "2025-05-06T18:14:33.667Z",
  "timeEnd": "2025-05-06T18:15:20.906Z",
  "currentCoef": 19.54,
  "totalBets": 4.95,
  "totalFees": 0.05,
  "magBurned": 0,
  "totalWins": 6.63,
  "bets": [...],
  "gameEnded": true
}
```

### Bet Object
```json
{
  "wallet": "rpQwfZuqKAWWLLvXmSMWotWKbfrB68THm5",
  "hash": "E50C72FB13102FFE3C029C6F6D2DCDD6DBE57AB51290C8CB916C5B3F069DB7E4",
  "amount": 4.95,
  "fee": 0.05,
  "betTime": "2025-05-06T18:20:29.125Z",
  "autoEndCoef": -1,
  "betResult": {
    "result": true,
    "wonAmount": 6.63,
    "coef": 1.34,
    "timeLeft": "2025-05-06T18:21:04.148Z"
  }
}
```

## Performance

- Handles 300k+ games efficiently
- Memory-efficient line-by-line JSON parsing
- Use `--limit` for quick analysis during development
- Full analysis on 302k games: ~10-30 seconds (depends on hardware)

## Example Output

```
============================================================
GAME CRASH DATA ANALYSIS
============================================================

📊 CRASH COEFFICIENT ANALYSIS
------------------------------------------------------------
mean                : 5.67
median              : 3.21
min                 : 1.00
max                 : 1234.56
stdev               : 12.34
total_games         : 302,208

🎲 BETTING PATTERNS
------------------------------------------------------------
total_bets          : 45,678
games_with_bets     : 12,345
games_without_bets  : 289,863
avg_bets_per_game   : 3.70
avg_bet_amount      : 5.23
total_wagered       : 238,945.67
win_rate            : 45.23%
```

## Use Cases

1. **Performance Monitoring**: Track house edge and game fairness
2. **Player Analysis**: Identify VIP players and betting patterns
3. **Risk Assessment**: Analyze cashout timing and player behavior
4. **Economic Planning**: Monitor token burns and fee collection
5. **Game Balancing**: Understand crash coefficient distribution
