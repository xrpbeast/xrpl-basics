# XRPL Features Overview

## Payments

Core functionality - transfer XRP or issued assets between accounts.
- 3-5 second confirmation
- Transaction finality (irreversible once confirmed)

## Issued Assets

Custom tokens representing any form of value:
- Traditional currencies (USD, EUR)
- Real-world asset tokens
- Can be sent, received, and traded like XRP

## Trust Lines

Establish trust relationships between accounts to enable issued asset exchange.
- Required for holding any non-XRP asset
- Defines credit limits between parties

## Decentralized Exchange (DEX)

Native on-ledger exchange for trading XRP and issued assets.
- **First blockchain with built-in DEX**
- Instant asset swapping
- No centralized intermediary

## Payment Channels

Off-chain mechanism for high-frequency transactions.
- Reduced fees
- Ideal for: micropayments, gaming, subscriptions

## Escrow

Lock XRP until conditions are met or time elapses.
- Condition-based or time-based release
- Currently XRP-only (amendment proposed for issued assets)

## NFTs

Non-fungible tokens for unique digital ownership.
- Added via amendment (Oct 2022)
- Minting, trading, burning on-ledger

## Cheques

Deferred payment promises.
- Sender creates cheque with amount and expiry
- Recipient must cash before expiration

## Tickets

Reserve transaction sequence numbers for future use.
- Ensures processing during congestion
- Enables out-of-order transaction submission

## Multi-Signature

Enhanced account security requiring multiple signatures.
- Up to 32 signers
- Configurable signature weights

## Pathfinding

Optimizes cross-currency payment routing.
- Connects sender/receiver through DEX orders
- Single payment can use multiple liquidity paths

## Sidechains

Parallel networks extending XRPL ecosystem:

| Sidechain | Features |
|-----------|----------|
| **Xahau** (2023) | Smart contracts, issued asset escrow, lightweight NFTs |
| **Root Network** | EVM compatibility (planned) |
