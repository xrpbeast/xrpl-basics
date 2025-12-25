# Core Concepts

Essential theoretical foundations for XRPL development.

## Infrastructure

Distributed network with no central authority. 600+ nodes worldwide (as of Oct 2023).

### rippled Server Roles

| Role | Purpose |
|------|---------|
| **Submission Node** | Handles transaction submission |
| **Validator** | Participates in consensus |
| **Full History** | Stores complete ledger history |

Operators can run rippled on own hardware or cloud. Requirements vary by role.

## Consensus

The XRP Ledger Consensus Protocol solves the **double-spend problem** without a central authority.

### Properties
- All participants agree on state and transaction order
- No central operator or single point of failure
- Network progresses even with some misbehaving nodes
- Fails safely rather than confirming invalid transactions
- No wasteful resource competition (unlike PoW)

### Process
- Series of consensus rounds
- Validators agree on transaction ordering
- New ledger finalized every 3-5 seconds

## Ledger Versions

> "Blocks" are called "ledger versions" (or just "ledgers") in XRPL

### Ledger States

| State | Description |
|-------|-------------|
| **Validated** | Consensus complete, immutable |
| **Open** | Actively being updated, subject to change |
| **Pending Closed** | No new txns, awaiting consensus |

### Ledger Structure
1. **Header** - Index, hash, parent hash
2. **Transaction Set** - All transactions + metadata
3. **State Data** - Snapshot of accounts, balances, settings

## Accounts

More than just an address - a complete identity on the ledger.

### Components
- **Address** - Public identifier
- **XRP Balance** - Required for all accounts
- **Sequence Number** - Ensures correct transaction order
- **Transaction History**
- **Authorization** - Master key, regular key, or multi-sig
- **Owned Objects** - NFTs, trust lines, offers, etc.

### Creating an Account
1. Generate master key pair
2. Send XRP to the address (from exchange, wallet, or faucet)
3. Account activates when base reserve is met

## Reserves (Spam Prevention)

| Type | Purpose |
|------|---------|
| **Base Reserve** | Minimum XRP to activate account |
| **Owner Reserve** | Additional XRP per owned object |

- Reserves are locked, not spent
- Amounts set by validator fee voting
- Adjust over time based on XRP price

## Transactions

**The only way to modify the ledger.**

### Required Fields
| Field | Purpose |
|-------|---------|
| `Account` | Sender address |
| `TransactionType` | What action to perform |
| `Fee` | Anti-spam cost (destroyed) |
| `Sequence` | Must be account's last sequence + 1 |

### Transaction Lifecycle
1. Sign transaction
2. Submit to network
3. Included in ledger
4. **Final only when in validated ledger**

### Result Codes
- `tesSUCCESS` - Transaction succeeded
- Various prefixes indicate different outcomes
- Failed transactions still pay fees (spam prevention)

## Fees

### Types
| Type | Description |
|------|-------------|
| **Neutral Fees** | Protocol-level, mandatory, XRP destroyed |
| **Optional Fees** | User-defined (transfer fees, trust line quality) |
| **Off-Ledger Fees** | Third-party charges (wallets, marketplaces) |

Set by validators through voting process.

## Role of XRP

### 1. Network Security
- Transaction fees have real-world cost
- Reserve requirements prevent spam
- Fee escalation during high load

### 2. Value Exchange
- Tradeable asset with market value
- Bridge currency for cross-border payments
- Used by Ripple for liquidity

## Amendments

Mechanism to upgrade rippled software.

### Process
1. **Proposal** - Discussion on GitHub, gets XLS number
2. **Feedback** - Community review and refinement
3. **Implementation** - Code developed and tested
4. **Voting** - Validators vote on activation
5. **Activation** - Requires 80% support for 2 weeks

### Amendment Blocking
- Nodes running old software become blocked
- Cannot participate in consensus
- Fix: Update to latest rippled version

## Client Libraries

SDKs that abstract raw API complexity.

| Language | Package |
|----------|---------|
| JavaScript | `xrpl` |
| Python | `xrpl-py` |
| Java | `xrpl4j` |
| C++ | `rippled` headers |
| PHP | `xrpl_php` |
| Ruby | `xrbp` |

This course uses JavaScript (`xrpl`).
