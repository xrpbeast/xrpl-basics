# xMagnetic Crash Game Monitor & Analyzer

Real-time WebSocket monitor and statistical analyzer for the xMagnetic crash game.

## What It Does

1. **Monitor** (`npm start`) - Connects to WebSocket feeds, logs all games and bets in real-time
2. **Bootstrap** (`npm run bootstrap`) - Pulls last 100 games from API for quick analysis
3. **Analyze** (`npm run analyze`) - Statistical tests on collected data
4. **Scrape** (`npm run scrape`) - Downloads ALL historical games (300k+) with full bet data
5. **Analyze Full** (`npm run analyze:full`) - Deep analysis with bet-level correlation tests

## Installation

```bash
npm install
```

## Usage

### Quick Analysis (100 games)
```bash
npm run bootstrap   # Pull 100 games from API
npm run analyze     # Run statistical analysis
```

### Full Historical Analysis (RECOMMENDED)
```bash
npm run scrape      # Download all 300k+ games (~30 min)
npm run analyze:full # Deep analysis with bet correlation
```

### Real-time Monitoring
```bash
npm start           # Run WebSocket monitor (keeps running)
```

## What the Full Analyzer Checks

| Test | What It Detects |
|------|-----------------|
| **Distribution Analysis** | Crash point distribution vs expected |
| **Runs Test** | Non-random streaks/patterns |
| **Autocorrelation** | Dependency between consecutive games |
| **Bet-Size Correlation** | 🚨 Whether high-bet games crash earlier |
| **Whale Analysis** | Win rates for big vs small bettors |
| **House Edge Calculation** | Actual vs stated edge |
| **Streak Analysis** | Probability after N consecutive lows |
| **Time Patterns** | Variations by hour |

## Key Finding: Bet-Crash Correlation

The most important test is bet-size correlation:
- **Negative correlation** = high-bet games crash earlier = manipulation
- **Zero correlation** = bet size doesn't affect crash = fair RNG

```
💰 BET-SIZE vs CRASH CORRELATION
   Total bet amount vs crash: -0.1234 🚨 SUSPICIOUS
   Q1 (lowest bets): avg crash 2.45x
   Q4 (highest bets): avg crash 1.89x
   🚨 HIGH-BET GAMES CRASH 0.56x EARLIER ON AVERAGE
```

## Data Files

- `data/games.jsonl` - One JSON record per line, each game
- `data/bets.jsonl` - One JSON record per line, each bet

## Example Output

```
📊 xMagnetic Crash Game Analysis
============================================================

📈 BASIC STATISTICS
   Games analyzed: 100
   Mean multiplier: 2.0543x
   Expected mean (1% edge): ~1.98x
   Deviation from expected: 0.0743 ✅ Normal

🎲 RUNS TEST (Randomness)
   Z-score: 0.421 ✅ Random

💰 BET-SIZE CORRELATION
   Correlation: -0.0234 ✅ No correlation
```

## Interpretation

| Indicator | Good | Suspicious |
|-----------|------|------------|
| Mean | 1.8-2.2x | <1.5x or >2.5x |
| Chi-squared | <15 | >25 |
| Runs Z-score | -1.96 to 1.96 | Outside range |
| Autocorrelation | <0.1 | >0.2 |
| Bet-size correlation | >-0.1 | <-0.2 (negative = crashes earlier with big bets) |

## Python Analyzer

The comprehensive statistical analyzer is now Python-based with enhanced features:

```bash
# Run full analysis with all 300k+ games
python analyze_games.py data/full_games.jsonl

# Analyze first 10k games only
python analyze_games.py data/full_games.jsonl --limit 10000

# Export detailed player stats
python analyze_games.py data/full_games.jsonl --export-players
```

### Current Analysis Features
- **9 Prediction Methods**: SMA, EMA, WMA, pattern-based, median, mode, trend-adjusted
- **Statistical Tests**: Runs test, autocorrelation, chi-square, volatility analysis
- **Pattern Detection**: 3-game sequences, streak analysis, transition probabilities
- **Player Analytics**: Win rates, profit/loss, behavior patterns
- **Economic Metrics**: House edge, fee analysis, payout ratios

### Sample Output (303,886 games analyzed)

<details>
<summary>Click to expand full analysis output</summary>

```
Loading data from data/full_games.jsonl...
✓ Loaded 303,886 games

============================================================
GAME CRASH DATA ANALYSIS
============================================================

📊 CRASH COEFFICIENT ANALYSIS
------------------------------------------------------------
mean                : 4.69
median              : 1.72
min                 : 1.00
max                 : 99.91
stdev               : 11.04
total_games         : 303,886

🎲 BETTING PATTERNS
------------------------------------------------------------
total_bets          : 180,514
games_with_bets     : 117,565
games_without_bets  : 186,321
avg_bets_per_game   : 1.54
avg_bet_amount      : 5.49
total_wagered       : 990,983.05
win_rate            : 48.64%

👥 PLAYER BEHAVIOR
------------------------------------------------------------
unique_players      : 2,213
avg_bets_per_player : 81.57
avg_wagered_per_player: 447.80
most_active_player_bets: 14,513

⏱️  GAME DURATION
------------------------------------------------------------
avg_duration_seconds: 13.95s (0.23m)
median_duration_seconds: 9.66s (0.16m)
min_duration_seconds: -0.14s (-0.00m)
max_duration_seconds: 128.03s (2.13m)

💰 ECONOMIC METRICS
------------------------------------------------------------
total_fees_collected: 10,009.89
total_mag_burned    : 0.00
total_wagered       : 990,983.05
total_paid_out      : 865,482.67
house_edge          : 12.66%
avg_fee_per_game    : 0.03

⏰ CASHOUT TIMING ANALYSIS
------------------------------------------------------------
total_cashouts      : 87,804
early_cashouts      : 86,903
late_cashouts       : 901
avg_cashout_ratio   : 57.49%
median_cashout_ratio: 63.24%

🎯 TOP 10 MOST ACTIVE PLAYERS (by total bets)
------------------------------------------------------------
 1. r9erBapqd1mjJG9XnXHWwdZs3qA8XmEYab: 14,513 bets | Win rate: 4.3% | Net: +64.38
 2. r3dHM1WEWbn8dXbtyiHwumMW2NsmxmoJL3: 5,955 bets | Win rate: 16.2% | Net: -819.37
 3. rPtiQk4NsUT1UcG9kgNA3phZm7jeSKbNcP: 4,774 bets | Win rate: 66.0% | Net: -501.02
 4. rs8H9yXmLoRCGPbKysSBSuEidBLf95eaem: 4,768 bets | Win rate: 40.2% | Net: -3454.28
 5. rRE2wh2SUotgtb552JcUxZLFpSjPh5sTy: 4,280 bets | Win rate: 77.7% | Net: -186.02
 6. rwuoLsxv9U4HNUnV2eZaKRLoB3LYYfDHq3: 4,234 bets | Win rate: 40.9% | Net: -683.06
 7. r4PcWuYwrHGLSngTmu7tWb4JLABeGyhzgu: 3,955 bets | Win rate: 78.1% | Net: -1922.80
 8. rHDkfmWKXbi6FFXs53V3j6kbJEnDCYj2S5: 3,118 bets | Win rate: 32.0% | Net: -5165.35
 9. rhZYVGxsrwRuWo2cXuU1ncVibfvt7kbbCA: 2,955 bets | Win rate: 4.3% | Net: -346.75
10. rN9otWWPVQfXxDR8nSxedQv4xDhau4JAHR: 2,922 bets | Win rate: 12.6% | Net: -406.66

💸 TOP 10 HIGHEST WAGERED (by total amount)
------------------------------------------------------------
 1. rMtB4Pdh72xNuYfJCf289Msx78vZHNuiDB: 52,871.94 wagered | 1,599 bets | Net: -20,592.38
 2. r4PcWuYwrHGLSngTmu7tWb4JLABeGyhzgu: 40,278.76 wagered | 3,955 bets | Net: -1,922.80
 3. rHDkfmWKXbi6FFXs53V3j6kbJEnDCYj2S5: 39,394.08 wagered | 3,118 bets | Net: -5,165.35
 4. rp1wJFbrK81xaGQ9Ktbpsi2TqfmG6eh4bE: 30,197.97 wagered | 303 bets | Net: +208.22
 5. rfe9VskBAdMqDsRsCQBmSEwSiGAtvz1dgk: 29,908.49 wagered | 335 bets | Net: +644.10
 6. rs8H9yXmLoRCGPbKysSBSuEidBLf95eaem: 24,772.50 wagered | 4,768 bets | Net: -3,454.28
 7. rwr4bm1jtYPRrvHVMvNqJhkLgBM7KQ3MKH: 23,677.71 wagered | 1,806 bets | Net: -1,177.03
 8. rE8hrmvfwrwauyhAeSvPmBVWBVCE4Y7UZr: 20,205.90 wagered | 195 bets | Net: -291.08
 9. r9erBapqd1mjJG9XnXHWwdZs3qA8XmEYab: 19,508.42 wagered | 14,513 bets | Net: +64.38
10. rfd1fmPLJg9i6kQGSMdVpXttq7rws82bgV: 17,437.86 wagered | 453 bets | Net: -1,274.06

🤑 TOP 10 BIGGEST WINNERS (by total won)
------------------------------------------------------------
 1. r4PcWuYwrHGLSngTmu7tWb4JLABeGyhzgu: 38,355.96 won | Wagered: 40,278.76 | Net: -1,922.80
 2. rHDkfmWKXbi6FFXs53V3j6kbJEnDCYj2S5: 34,228.73 won | Wagered: 39,394.08 | Net: -5,165.35
 3. rMtB4Pdh72xNuYfJCf289Msx78vZHNuiDB: 32,279.56 won | Wagered: 52,871.94 | Net: -20,592.38
 4. rfe9VskBAdMqDsRsCQBmSEwSiGAtvz1dgk: 30,552.59 won | Wagered: 29,908.49 | Net: +644.10
 5. rp1wJFbrK81xaGQ9Ktbpsi2TqfmG6eh4bE: 30,406.19 won | Wagered: 30,197.97 | Net: +208.22
 6. rwr4bm1jtYPRrvHVMvNqJhkLgBM7KQ3MKH: 22,500.68 won | Wagered: 23,677.71 | Net: -1,177.03
 7. rs8H9yXmLoRCGPbKysSBSuEidBLf95eaem: 21,318.22 won | Wagered: 24,772.50 | Net: -3,454.28
 8. rE8hrmvfwrwauyhAeSvPmBVWBVCE4Y7UZr: 19,914.82 won | Wagered: 20,205.90 | Net: -291.08
 9. r9erBapqd1mjJG9XnXHWwdZs3qA8XmEYab: 19,572.80 won | Wagered: 19,508.42 | Net: +64.38
10. rfd1fmPLJg9i6kQGSMdVpXttq7rws82bgV: 16,163.80 won | Wagered: 17,437.86 | Net: -1,274.06

📈 TOP 10 MOST PROFITABLE PLAYERS (by net profit)
------------------------------------------------------------
 1. rfe9VskBAdMqDsRsCQBmSEwSiGAtvz1dgk: +644.10 profit | Win rate: 84.2% | 335 bets
 2. rfpx6XkU3efku3XzD6FwvuLvhiYtru7fds: +428.17 profit | Win rate: 71.6% | 275 bets
 3. rfCHpFCwGtAa8zzUMDhD2YJvZCTxYEwBx1: +341.59 profit | Win rate: 64.2% | 318 bets
 4. rp1wJFbrK81xaGQ9Ktbpsi2TqfmG6eh4bE: +208.22 profit | Win rate: 70.6% | 303 bets
 5. rpfBxF99dcyYSBeGh6mk7T6QAz9CfQBWDs: +184.22 profit | Win rate: 75.9% | 336 bets
 6. rwxjuzL9Jp5WVbm9fDhsX2ofkRSLvrZpm9: +149.17 profit | Win rate: 47.1% | 87 bets
 7. rsSF2BWFVYaEaq7RUUWKibaDgg2BWeo6uQ: +112.18 profit | Win rate: 84.6% | 52 bets
 8. rhgwGyVc6dRjjv8VdEe3TJfSPuuAsWdwuM: +107.98 profit | Win rate: 75.4% | 276 bets
 9. rnuGNG48QV5RGuGHPFBujC93BfpFVo2CGk: +95.21 profit | Win rate: 38.5% | 26 bets
10. rGGNQ3BaKqjbG9oS4Br1jpUtowZ3KmYnGi: +90.68 profit | Win rate: 68.9% | 739 bets

🎲 TOP 10 BEST WIN RATES (min 10 bets)
------------------------------------------------------------
 1. r9LCHEKFUiBXvkeMG8DkYhLyfkSu9AwrQs: 100.0% | 17/17 wins | Net: +3.11
 2. r9TnYE9FWnMGQVVBVz7AAT2znUH3kCE7uJ: 100.0% | 14/14 wins | Net: +1.85
 3. rwXC6n8VGJqMyAjkqifLCUEC8ft58KZST9: 96.4% | 27/28 wins | Net: +1.88
 4. rU5fTUsJPyTt7sUiKj9HwV7gtD9yFJqZrR: 95.5% | 21/22 wins | Net: +13.01
 5. r9Ju8LbVnyRw1cJneUMP16WKtFQLQpa2wE: 95.5% | 21/22 wins | Net: -8.63
 6. rMJFJLxWR7Zx41oA4whYy1jSqJv2v4fyk7: 94.1% | 16/17 wins | Net: -1.24
 7. rQnjE8cuGomYh63HfgYhpwanth3g3gy3th: 93.8% | 15/16 wins | Net: -0.54
 8. rN3hJjFHETXbyCCRymxAC4UE7X8EVP1nga: 93.3% | 14/15 wins | Net: +0.14
 9. rPHWKEcmBvw3E3wUDu4dGXCk9AmPhu4928: 93.3% | 14/15 wins | Net: +1.74
10. rEC6jV8Kf7FpKr9PpD3USjk6Yb7pUWDkwq: 91.7% | 88/96 wins | Net: +1.15

🚀 TOP 10 HIGHEST CRASHES
------------------------------------------------------------
 1. Game #116: 99.91x
 2. Game #2,811: 98.92x
 3. Game #8,415: 98.92x
 4. Game #22,339: 98.92x
 5. Game #35,599: 98.92x
 6. Game #41,810: 98.92x
 7. Game #66,898: 98.92x
 8. Game #67,818: 98.92x
 9. Game #76,540: 98.92x
10. Game #78,238: 98.92x

🏆 TOP 10 BIGGEST WINS
------------------------------------------------------------
 1. 2578.95 (bet: 495.00 @ 5.21x)
    Wallet: rMtB4Pdh72xNuYfJCf289Msx78vZHNuiDB | Game #56805
 2. 1039.50 (bet: 495.00 @ 2.10x)
    Wallet: rMtB4Pdh72xNuYfJCf289Msx78vZHNuiDB | Game #59679
 3. 990.00 (bet: 495.00 @ 2.00x)
    Wallet: rDxDWhfNrCNsCgqNjrCdR43cZQT2ruRvJN | Game #4798
 4. 900.90 (bet: 495.00 @ 1.82x)
    Wallet: rff2mufA1sQ7Bg3Mjc4azgd2LhExjiSrrG | Game #99468
 5. 836.06 (bet: 148.50 @ 5.63x)
    Wallet: rpRLdCRgqywcgMaRbCBZQEKv1fk3ZsuDVU | Game #116722
 6. 801.90 (bet: 495.00 @ 1.62x)
    Wallet: rMtB4Pdh72xNuYfJCf289Msx78vZHNuiDB | Game #55138
 7. 801.90 (bet: 495.00 @ 1.62x)
    Wallet: rMtB4Pdh72xNuYfJCf289Msx78vZHNuiDB | Game #79882
 8. 792.00 (bet: 495.00 @ 1.60x)
    Wallet: rMtB4Pdh72xNuYfJCf289Msx78vZHNuiDB | Game #55144
 9. 772.20 (bet: 495.00 @ 1.56x)
    Wallet: rMtB4Pdh72xNuYfJCf289Msx78vZHNuiDB | Game #79899
10. 749.33 (bet: 430.65 @ 1.74x)
    Wallet: rff2mufA1sQ7Bg3Mjc4azgd2LhExjiSrrG | Game #99464

📐 ADVANCED STATISTICAL TESTS
------------------------------------------------------------
Runs Test:
  Total runs: 151,575
  Expected runs: 151943.98
  Z-score: -1.339
  Result: Random (passes test)
  Is random: ✅ YES

Autocorrelation (lag-1):
  Coefficient: 0.001
  Interpretation: Random

🔥 STREAKS ANALYSIS
------------------------------------------------------------
Median crash point: 1.72x
Longest high streak: 19 games
Longest low streak: 17 games
Average high streak: 2.01 games
Average low streak: 2.00 games
Current streak: 2 high games

📊 DISTRIBUTION ANALYSIS
------------------------------------------------------------
Crash ranges:
  10.0x+      : 23,821 games ( 7.84%)
  5.0-10.0x   : 15,012 games ( 4.94%)
  1.5-2.0x    : 86,366 games (28.42%)
  3.0-5.0x    : 21,697 games ( 7.14%)
  2.5-3.0x    : 22,393 games ( 7.37%)
  1.0-1.5x    : 111,140 games (36.57%)
  2.0-2.5x    : 23,457 games ( 7.72%)

Below 2.0x: 64.99%
Above 5.0x: 12.78%
Above 10.0x: 7.84%

📉 VOLATILITY ANALYSIS
------------------------------------------------------------
Average volatility: 8.754
Recent volatility: 15.087
Max volatility: 36.665
Min volatility: 0.248
Trend: Increasing

🎯 CONDITIONAL PROBABILITIES
------------------------------------------------------------
Median threshold: 1.72x
P(High | after Low): 49.9%
P(Low | after Low): 50.1%
P(High | after High): 50.1%
P(Low | after High): 49.9%

🔍 TOP 10 MOST COMMON PATTERNS (3-game sequences)
------------------------------------------------------------
Legend: VL=<1.5x, L=1.5-2x, M=2-3x, H=3-5x, VH=>5x
 1. VL-VL-VL     → 14,869 times (4.89%)
 2. VL-VL-L      → 11,580 times (3.81%)
 3. L-VL-VL      → 11,488 times (3.78%)
 4. VL-L-VL      → 11,440 times (3.76%)
 5. L-L-VL       → 8,979 times (2.95%)
 6. L-VL-L       → 8,931 times (2.94%)
 7. VL-L-L       → 8,926 times (2.94%)
 8. L-L-L        → 7,049 times (2.32%)
 9. M-VL-VL      → 6,196 times (2.04%)
10. VL-M-VL      → 6,149 times (2.02%)

============================================================
🔮 NEXT OUTCOME PREDICTIONS
============================================================

📍 RECENT CONTEXT
   Last game: 1.84x
   Recent 10 avg: 2.42x
   Recent 10 range: 1.25x - 7.23x
   Trend: Decreasing

📊 PREDICTION METHODS
------------------------------------------------------------
SMA (10 games):      2.42x
SMA (50 games):      7.04x
SMA (100 games):     6.01x
EMA (exponential):   2.78x
WMA (weighted):      3.51x
Pattern-based:       4.60x (9608 similar)
Historical median:   1.72x
Most common range:   1.20x
Trend-adjusted:      1.00x

============================================================
🎯 CONSENSUS PREDICTION: 2.78x
   Confidence: Low
   Std deviation: ±2.13x
============================================================
✅ Prediction suggests MEDIUM crash

⚠️  DISCLAIMER: Predictions are statistical estimates only.
    Past performance does not guarantee future results.
    This game has a house edge - you will lose money over time.

============================================================
ANALYSIS COMPLETE
============================================================
```

</details>

---

## 🚀 Next Steps & Future Enhancements

### Analytics Enhancements
- [ ] **Machine Learning Models**
  - LSTM/GRU networks for time-series prediction
  - Random Forest for pattern classification
  - Ensemble methods combining multiple models
  - Feature engineering (moving averages, RSI, MACD-like indicators)

- [ ] **Advanced Statistical Tests**
  - Kolmogorov-Smirnov test for distribution comparison
  - Granger causality test (bet size → crash correlation)
  - Change point detection for RNG shifts
  - Bayesian analysis for probability estimation

- [ ] **Bet Pattern Analysis**
  - Identify coordinated betting (possible collusion)
  - Detect unusual betting patterns (potential insider info)
  - Analyze cashout timing strategies
  - Track wallet clustering and relationships

### Data & Storage
- [ ] **Database Integration**
  - PostgreSQL/TimescaleDB for time-series queries
  - Redis for real-time caching
  - GraphQL API for flexible data access
  - Indexed queries for player analysis

- [ ] **Data Pipeline**
  - Automated hourly scraping with cron
  - Incremental updates (delta only)
  - Data validation and cleaning
  - Backup and archival system

### Visualization & Reporting
- [ ] **Interactive Dashboard**
  - Real-time charts (Chart.js, D3.js, Plotly)
  - Live prediction updates
  - Historical trend visualization
  - Player leaderboards

- [ ] **Web Interface**
  - Flask/FastAPI backend
  - React/Vue frontend
  - WebSocket for live updates
  - Export reports (PDF, CSV, JSON)

- [ ] **Automated Reports**
  - Daily/weekly summary emails
  - Anomaly alerts (suspicious patterns)
  - Performance metrics tracking
  - Markdown report generation

### Real-time Features
- [ ] **Live Monitoring Dashboard**
  - Current game statistics
  - Running prediction accuracy
  - Alert on unusual patterns
  - Player activity tracking

- [ ] **Alerting System**
  - Telegram/Discord bot integration
  - Email notifications
  - Threshold-based alerts (high bets, unusual crashes)
  - Pattern match notifications

### Research & Analysis
- [ ] **Comparative Analysis**
  - Compare with other crash games
  - Industry standard fairness metrics
  - Cross-platform correlation

- [ ] **Provably Fair Analysis**
  - Implement hash verification (if available)
  - Compare with provably fair alternatives
  - Document fairness mechanisms

- [ ] **Economic Modeling**
  - Expected value calculations
  - Optimal betting strategies (theoretical)
  - Risk/reward analysis
  - Bankroll management simulation

### Code Quality & Testing
- [ ] **Testing Suite**
  - Unit tests for all analysis methods
  - Integration tests for scraper
  - Performance benchmarks
  - Mock data generators

- [ ] **Documentation**
  - API documentation (docstrings → Sphinx)
  - Jupyter notebooks with examples
  - Video tutorials
  - Architecture diagrams

- [ ] **Performance Optimization**
  - Parallel processing for large datasets
  - Caching frequently accessed data
  - Streaming analysis for real-time data
  - Memory-efficient data structures

### Deployment & Operations
- [ ] **Containerization**
  - Docker images for scraper & analyzer
  - Docker Compose for full stack
  - Kubernetes for scaling

- [ ] **CI/CD Pipeline**
  - GitHub Actions for testing
  - Automated deployment
  - Version management

---

## Important Notes

⚠️ **Statistical analysis cannot prove manipulation** - it can only detect patterns inconsistent with fair RNG.

⚠️ **The game has NO provably fair mechanism** - the server has complete control over outcomes.

⚠️ **Even "fair" RNG has a house edge** - you will lose money over time regardless of analysis.

⚠️ **Educational purposes only** - This tool is for research and learning. Do not use for gambling decisions.

---

## Contributing

Contributions welcome! Priority areas:
1. Machine learning prediction models
2. Interactive visualization dashboard
3. Real-time alerting system
4. Database integration
5. Additional statistical tests

See `analyze_games.py` header for code structure and extension guidelines.

---

## License

MIT - Use at your own risk. This is for educational purposes only.
