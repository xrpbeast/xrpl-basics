# XRPL Development Guide

Comprehensive resources for building on XRP Ledger (XRPL). Includes tutorials, API references, and AI assistant integration.

---

## For AI Assistants

**Skill Available**: `.claude/skills/xrpl-dev-guide/SKILL.md`

This repo includes a comprehensive skill for AI assistants helping developers build XRPL applications. The skill provides:
- Standard transaction patterns (connect → autofill → sign → submit)
- Type-safe TypeScript examples
- Security best practices
- Error handling patterns
- 111+ curated resource links
- Dynamic sitemap integration (https://xrpl.org/sitemap.xml)

**Key Principles**:
- Always use official docs (https://js.xrpl.org/ for JS/TS)
- Never guess API methods - fetch docs when uncertain
- Default to testnet, type-safe code, `.env` for secrets
- Cite sources with specific URLs

## Getting Started

### Quick Setup (JavaScript/TypeScript)
```bash
# Install XRPL library
npm install xrpl

# Create .env file
echo "WALLET_SEED=your_seed_here" > .env

# Basic example
import { Client, Wallet } from 'xrpl'

const client = new Client('wss://s.altnet.rippletest.net:51233')
await client.connect()
const wallet = Wallet.fromSeed(process.env.WALLET_SEED!)
// ... your code
await client.disconnect()
```

### Get Test XRP
- [Testnet Faucet](https://xrpl.org/xrp-testnet-faucet.html) - Free testnet XRP

### Learn XRPL Basics
- [What is XRP Ledger?](https://xrpl.org/docs/introduction/what-is-the-xrp-ledger)
- [What is XRP?](https://xrpl.org/docs/introduction/what-is-xrp)
- [Crypto Wallets](https://xrpl.org/docs/introduction/crypto-wallets)
- [Software Ecosystem](https://xrpl.org/docs/introduction/software-ecosystem)
- [Transactions & Requests](https://xrpl.org/docs/introduction/transactions-and-requests)

## Core Concepts

### Accounts & Keys
- [Accounts Overview](https://xrpl.org/docs/concepts/accounts)
- [Addresses](https://xrpl.org/docs/concepts/accounts/addresses)
- [Cryptographic Keys](https://xrpl.org/docs/concepts/accounts/cryptographic-keys)
- [Multi-Signing](https://xrpl.org/docs/concepts/accounts/multi-signing)
- [Reserves](https://xrpl.org/docs/concepts/accounts/reserves)
- [Tickets](https://xrpl.org/docs/concepts/accounts/tickets)

### Transactions & Ledgers
- [Transactions](https://xrpl.org/docs/concepts/transactions)
- [Transaction Fees](https://xrpl.org/docs/concepts/transactions/fees)
- [Reliable Transaction Submission](https://xrpl.org/docs/concepts/transactions/reliable-transaction-submission)
- [Secure Signing](https://xrpl.org/docs/concepts/transactions/secure-signing)
- [Ledgers](https://xrpl.org/docs/concepts/ledgers)
- [Ledger Structure](https://xrpl.org/docs/concepts/ledgers/ledger-structure)

### Network & Consensus
- [Consensus Protocol](https://xrpl.org/docs/concepts/consensus-protocol)
- [Networks & Servers](https://xrpl.org/docs/concepts/networks-and-servers)

## Payment Types
- [Direct XRP Payments](https://xrpl.org/docs/concepts/payment-types/direct-xrp-payments)
- [Cross-Currency Payments](https://xrpl.org/docs/concepts/payment-types/cross-currency-payments)
- [Escrow](https://xrpl.org/docs/concepts/payment-types/escrow)
- [Payment Channels](https://xrpl.org/docs/concepts/payment-types/payment-channels)
- [Checks](https://xrpl.org/docs/concepts/payment-types/checks)

## Tokens & Digital Assets

### Fungible Tokens
- [Fungible Tokens Overview](https://xrpl.org/docs/concepts/tokens/fungible-tokens)
- [Trust Lines](https://xrpl.org/docs/concepts/tokens/fungible-tokens/trust-line-tokens)
- [Freezes](https://xrpl.org/docs/concepts/tokens/fungible-tokens/freezes)
- [Transfer Fees](https://xrpl.org/docs/concepts/tokens/fungible-tokens/transfer-fees)
- [Rippling](https://xrpl.org/docs/concepts/tokens/fungible-tokens/rippling)

### NFTs
- [NFTs Overview](https://xrpl.org/docs/concepts/tokens/nfts)
- [Dynamic NFTs](https://xrpl.org/docs/concepts/tokens/nfts/dynamic-nfts)
- [NFT Collections](https://xrpl.org/docs/concepts/tokens/nfts/collections)

### Decentralized Exchange (DEX)
- [DEX Overview](https://xrpl.org/docs/concepts/tokens/decentralized-exchange)
- [Offers](https://xrpl.org/docs/concepts/tokens/decentralized-exchange/offers)
- [Automated Market Makers (AMM)](https://xrpl.org/docs/concepts/tokens/decentralized-exchange/automated-market-makers)
- [Auto-Bridging](https://xrpl.org/docs/concepts/tokens/decentralized-exchange/autobridging)

## Tutorials

### JavaScript/TypeScript
- [JavaScript Tutorials](https://xrpl.org/docs/tutorials/javascript)
- [Create Accounts & Send XRP](https://xrpl.org/docs/tutorials/javascript/send-payments/create-accounts-send-xrp)
- [Create Trust Lines & Send Currency](https://xrpl.org/docs/tutorials/javascript/send-payments/create-trust-line-send-currency)
- [Create Offers](https://xrpl.org/docs/tutorials/javascript/send-payments/create-offers)
- [Mint & Burn NFTs](https://xrpl.org/docs/tutorials/javascript/nfts/mint-and-burn-nfts)
- [Transfer NFTs](https://xrpl.org/docs/tutorials/javascript/nfts/transfer-nfts)
- [AMM Tutorials](https://xrpl.org/docs/tutorials/javascript/amm)
- [Build Apps](https://xrpl.org/docs/tutorials/javascript/build-apps)
- [Compliance](https://xrpl.org/docs/tutorials/javascript/compliance)

### Python
- [Python Tutorials](https://xrpl.org/docs/tutorials/python)
- [Build Apps (Python)](https://xrpl.org/docs/tutorials/python/build-apps)
- [Send Payments (Python)](https://xrpl.org/docs/tutorials/python/send-payments)
- [NFTs (Python)](https://xrpl.org/docs/tutorials/python/nfts)

### Java
- [Java Tutorials](https://xrpl.org/docs/tutorials/java)
- [Build Apps (Java)](https://xrpl.org/docs/tutorials/java/build-apps)

### Go
- [Go Tutorials](https://xrpl.org/docs/tutorials/go)
- [Build Apps (Go)](https://xrpl.org/docs/tutorials/go/build-apps)

### HTTP/WebSocket APIs
- [API Tutorials](https://xrpl.org/docs/tutorials/http-websocket-apis)
- [Build Apps via APIs](https://xrpl.org/docs/tutorials/http-websocket-apis/build-apps)

## How-To Guides
- [Send XRP](https://xrpl.org/docs/tutorials/how-tos/send-xrp)
- [Manage Account Settings](https://xrpl.org/docs/tutorials/how-tos/manage-account-settings)
- [Use Tokens](https://xrpl.org/docs/tutorials/how-tos/use-tokens)
- [Use Batch Transactions](https://xrpl.org/docs/tutorials/how-tos/use-batch-transactions)
- [Use XRPL Sidechains](https://xrpl.org/docs/tutorials/how-tos/use-xrpl-sidechains)

## API References

### HTTP/WebSocket APIs
- [API Overview](https://xrpl.org/docs/references/http-websocket-apis)
- [Public API Methods](https://xrpl.org/docs/references/http-websocket-apis/public-api-methods)
- [Admin API Methods](https://xrpl.org/docs/references/http-websocket-apis/admin-api-methods)
- [Account Methods](https://xrpl.org/docs/references/http-websocket-apis/public-api-methods/account-methods)
- [Ledger Methods](https://xrpl.org/docs/references/http-websocket-apis/public-api-methods/ledger-methods)
- [Transaction Methods](https://xrpl.org/docs/references/http-websocket-apis/public-api-methods/transaction-methods)
- [Server Info Methods](https://xrpl.org/docs/references/http-websocket-apis/public-api-methods/server-info-methods)
- [Path & Order Book Methods](https://xrpl.org/docs/references/http-websocket-apis/public-api-methods/path-and-order-book-methods)

### Client Libraries & Data APIs
- [Client Libraries](https://xrpl.org/docs/references/client-libraries)
- [XRPL.js (JavaScript/TypeScript)](https://js.xrpl.org/)
- [XRP API](https://xrpl.org/docs/references/xrp-api)
- [Data API](https://xrpl.org/docs/references/data-api)

### Protocol & Data Formats
- [Protocol Reference](https://xrpl.org/docs/references/protocol)
- [Transaction Types](https://xrpl.org/docs/references/protocol/transactions)
- [Ledger Data Structures](https://xrpl.org/docs/references/protocol/ledger-data)
- [Data Types](https://xrpl.org/docs/references/protocol/data-types)
- [Binary Format](https://xrpl.org/docs/references/protocol/binary-format)

## Use Cases
- [Payments](https://xrpl.org/docs/use-cases/payments)
- [DeFi](https://xrpl.org/docs/use-cases/defi)
- [Tokenization](https://xrpl.org/docs/use-cases/tokenization)
- [NFT Marketplace Overview](https://xrpl.org/docs/use-cases/tokenization/nft-mkt-overview)

## Infrastructure & Operations
- [Installation](https://xrpl.org/docs/infrastructure/installation)
- [System Requirements](https://xrpl.org/docs/infrastructure/installation/system-requirements)
- [Configuration](https://xrpl.org/docs/infrastructure/configuration)
- [Server Modes](https://xrpl.org/docs/infrastructure/configuration/server-modes)
- [Peering](https://xrpl.org/docs/infrastructure/configuration/peering)
- [Testing & Auditing](https://xrpl.org/docs/infrastructure/testing-and-auditing)
- [Troubleshooting](https://xrpl.org/docs/infrastructure/troubleshooting)

## Tools & Explorers
- [XRP Ledger Explorer](https://livenet.xrpl.org/) - Mainnet explorer
- [XRPL Testnet Faucet](https://xrpl.org/xrp-testnet-faucet.html) - Get test XRP
- [WebSocket Tool](https://xrpl.org/websocket-api-tool.html) - Test API requests

## Community & Contribution
- [Contributing Guide](https://xrpl.org/contributing)
- [Code of Conduct](https://xrpl.org/code-of-conduct)
- [Contribute Code](https://xrpl.org/resources/contribute-code)
- [Contribute Documentation](https://xrpl.org/resources/contribute-documentation)
- [Contribute Blog Posts](https://xrpl.org/resources/contribute-blog)
- [Report a Scam](https://xrpl.org/community/report-a-scam)

## News & Updates
- [XRPL Blog](https://xrpl.org/blog) - Release notes, amendments, security updates

## Localized Resources
- [Spanish Documentation](https://xrpl.org/es-es/docs/introduction)
- [Japanese Documentation](https://xrpl.org/ja/docs/introduction)

