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
