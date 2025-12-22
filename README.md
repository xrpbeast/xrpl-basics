# XRPL Basics

Practical tools, examples, and AI assistant integration for XRP Ledger (XRPL) development and data analysis.

## Repository Structure

```
xrpl-basics/
├── .claude/
│   ├── skills/xrpl-dev-guide/    # AI assistant skill for XRPL development
│   └── agents/                    # Custom agents
├── data-collection/
│   ├── xmagnetic/                 # xMagnetic crash game analytics
│   │   └── game-crash-monitor/    # Real-time monitor + statistical analyzer
│   └── first-ledger/              # Ledger data collection tools
├── examples/
│   └── javascript/                # XRPL code examples
├── XRPLMETA_DOCUMENTATION.md      # XRPL Meta API reference with real responses
└── README.md
```

---

## 🎰 xMagnetic Crash Game Monitor

**Location**: `data-collection/xmagnetic/game-crash-monitor/`

Real-time WebSocket monitor and comprehensive statistical analyzer for xMagnetic crash game.

### Features
- **Scraper**: Downloads all 300k+ historical games with bet data
- **Analyzer**: Advanced statistical analysis with pattern detection and predictions
- **Monitor**: Real-time WebSocket feed tracking

### Quick Start
```bash
cd data-collection/xmagnetic/game-crash-monitor
npm install

# Download historical data
npm run scrape

# Run comprehensive analysis with predictions
python analyze_games.py data/full_games.jsonl
```

### Analysis Capabilities
- **Statistical Tests**: Runs test, autocorrelation, chi-square
- **Pattern Detection**: Identifies common 3-game sequences
- **Volatility Analysis**: Rolling window variance tracking
- **Conditional Probabilities**: Transition matrix analysis
- **Predictions**: 9 forecasting methods with consensus model
  - Moving averages (SMA, EMA, WMA)
  - Pattern-based matching
  - Trend-adjusted predictions
  - Historical median/mode

See `data-collection/xmagnetic/game-crash-monitor/ANALYSIS_GUIDE.md` for detailed documentation.

---

## 📊 XRPL Meta API Documentation

**Location**: `XRPLMETA_DOCUMENTATION.md`

Comprehensive documentation for XRPL Meta API with real-world examples and actual API responses.

### Features
- **REST API**: Token data, server info, ledger queries
- **WebSocket API**: Real-time token subscriptions
- **Real Examples**: Actual $BUBBLES token responses included
- **Type-Safe**: Full TypeScript interfaces
- **Multi-Language**: JavaScript, TypeScript, Python, React examples

### Quick Example
```javascript
// Fetch token data
const identifier = '24425542424C4553000000000000000000000000:rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs';
const response = await fetch(`https://s1.xrplmeta.org/token/${identifier}`);
const token = await response.json();

console.log(`Price: $${token.metrics.price}`);
console.log(`Holders: ${token.metrics.holders}`);
console.log(`24h Volume: ${token.metrics.volume_24h} XRP`);
```

### API Endpoints
- `GET /server` - Server status and ledger ranges
- `GET /tokens` - List all 185K+ tokens with metrics
- `GET /token/{currency}:{issuer}` - Detailed token data
- `GET /token/{currency}:{issuer}/series/{metric}` - Time series data
- `wss://s1.xrplmeta.org` - WebSocket subscriptions

### Real Data Included
- $BUBBLES token: 296 holders, $0.000274 price, 58.9M supply
- SOLO token: 218K holders, $31.3M market cap
- Server info with full ledger ranges

See `XRPLMETA_DOCUMENTATION.md` for complete API reference with real responses.

---

## 🤖 For AI Assistants

**Skill Available**: `.claude/skills/xrpl-dev-guide/SKILL.md`

Comprehensive skill for AI assistants building XRPL applications:
- Standard transaction patterns (connect → autofill → sign → submit)
- Type-safe TypeScript examples
- Security best practices (testnet defaults, `.env` for secrets)
- Error handling patterns
- 111+ curated resource links
- Dynamic sitemap integration

**Key Principles**:
- Always use official docs (https://js.xrpl.org/ for JS/TS)
- Never guess API methods - fetch docs when uncertain
- Cite sources with specific URLs

---

## 🚀 Getting Started with XRPL

### Quick Setup (JavaScript/TypeScript)
```bash
# Install XRPL library
npm install xrpl

# Create .env file for secrets
echo "WALLET_SEED=your_seed_here" > .env
```

```typescript
import { Client, Wallet } from 'xrpl'

// Connect to testnet
const client = new Client('wss://s.altnet.rippletest.net:51233')
await client.connect()

// Load wallet from seed
const wallet = Wallet.fromSeed(process.env.WALLET_SEED!)

// ... your transaction code here

await client.disconnect()
```

### Essential Resources
- **[Testnet Faucet](https://xrpl.org/xrp-testnet-faucet.html)** - Get free testnet XRP
- **[XRPL.js Docs](https://js.xrpl.org/)** - Official TypeScript/JavaScript library
- **[XRPL.org](https://xrpl.org/docs)** - Complete documentation
- **[WebSocket Tool](https://xrpl.org/websocket-api-tool.html)** - Test API requests

---

## 📚 XRPL Key Topics

### Core Concepts
- **[Accounts](https://xrpl.org/docs/concepts/accounts)** - Addresses, keys, reserves, multi-signing
- **[Transactions](https://xrpl.org/docs/concepts/transactions)** - Fees, reliable submission, secure signing
- **[Ledgers](https://xrpl.org/docs/concepts/ledgers)** - Structure and consensus protocol
- **[Consensus](https://xrpl.org/docs/concepts/consensus-protocol)** - How XRPL reaches agreement

### Payment Types
- **[XRP Payments](https://xrpl.org/docs/concepts/payment-types/direct-xrp-payments)** - Send XRP between accounts
- **[Cross-Currency](https://xrpl.org/docs/concepts/payment-types/cross-currency-payments)** - Multi-hop payments
- **[Escrow](https://xrpl.org/docs/concepts/payment-types/escrow)** - Time or condition-based releases
- **[Payment Channels](https://xrpl.org/docs/concepts/payment-types/payment-channels)** - High-throughput micropayments
- **[Checks](https://xrpl.org/docs/concepts/payment-types/checks)** - Deferred payments

### Tokens & Assets
- **[Fungible Tokens](https://xrpl.org/docs/concepts/tokens/fungible-tokens)** - Trust lines, freezes, transfer fees
- **[NFTs](https://xrpl.org/docs/concepts/tokens/nfts)** - Mint, transfer, collections
- **[DEX](https://xrpl.org/docs/concepts/tokens/decentralized-exchange)** - Built-in decentralized exchange
- **[AMM](https://xrpl.org/docs/concepts/tokens/decentralized-exchange/automated-market-makers)** - Automated market makers

### Tutorials by Language
- **[JavaScript/TypeScript](https://xrpl.org/docs/tutorials/javascript)** - Payments, NFTs, AMM, apps
- **[Python](https://xrpl.org/docs/tutorials/python)** - Build apps, payments, NFTs
- **[HTTP/WebSocket APIs](https://xrpl.org/docs/tutorials/http-websocket-apis)** - Direct API access

### API References
- **[HTTP/WebSocket APIs](https://xrpl.org/docs/references/http-websocket-apis)** - Public & admin methods
- **[XRPL.js Docs](https://js.xrpl.org/)** - TypeScript/JavaScript library
- **[Protocol Reference](https://xrpl.org/docs/references/protocol)** - Transaction types, data structures
- **[Data API](https://xrpl.org/docs/references/data-api)** - Historical data queries

---

## 🛠️ Tools & Explorers
- **[XRP Ledger Explorer](https://livenet.xrpl.org/)** - Mainnet blockchain explorer
- **[Testnet Explorer](https://testnet.xrpl.org/)** - Testnet blockchain explorer
- **[XRPL Meta](https://xrplmeta.org/)** - Token metadata & analytics API (185K+ tokens)
- **[WebSocket Tool](https://xrpl.org/websocket-api-tool.html)** - Interactive API testing

---

## 🤝 Contributing
Contributions welcome! See [XRPL Contributing Guide](https://xrpl.org/contributing) for guidelines.

---

## 📰 Stay Updated
- **[XRPL Blog](https://xrpl.org/blog)** - Release notes, amendments, security updates
- **[XRPL Foundation](https://foundation.xrpl.org/)** - Ecosystem news

