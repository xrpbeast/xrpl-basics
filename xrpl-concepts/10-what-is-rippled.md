# What is rippled?

Rippled (pronounced "ripple-dee") is the software that powers the XRP Ledger. It runs as part of a network of peers that relay cryptographically signed transactions between each other and maintains a local copy of the shared global ledger.

---

## Running Modes

Rippled can be run in several different modes:

### Daemon Mode (Default)

The default mode and the one you're most likely to use. Rippled runs silently as a background process, continuously participating in the network.

### Standalone Mode

Used primarily for testing. You invoke rippled in standalone mode by passing the `--standalone` option on launch. This lets you run a private instance without connecting to the network.

### Client Mode

Allows you to call API methods on another rippled server using a JSON-RPC client. For example, you could look up the server status if the executable is already running in another process.

### Other Options

Rippled has many command-line options you can pass on launch. These can sometimes be useful for diagnostics and debugging. For more details, see the [command line usage documentation](https://xrpl.org/docs/infrastructure/commandline-usage).

For most developers, all you really need is a server you can connect to for accessing the ledger.

---

## Three Types of Nodes

### 1. Stock Server (Submission Node)

The most basic configuration. A stock server:

- **Submits transactions** to the XRP Ledger
- **Accesses ledger history** (limited by storage)
- **Connects client applications** via WebSocket or JSON-RPC
- **Maintains shared state** of the ledger
- **Does NOT participate in consensus** - that's the validator's job

This is what most developers run when they need their own infrastructure.

### 2. Validating Server (Validator)

A validator does everything a stock server does, **plus** participates in the consensus process.

**Requirements for validators:**
- Strive for **100% uptime**
- Have **high-performance hardware**
- Be **clearly identifiable** (who operates it)

Every validator issues **validation messages** - sets of candidate transactions for evaluation by the network during consensus.

**Important:** Issuing validation messages does NOT automatically give your validator a say in consensus. That privilege is reserved for validators on the **Unique Node List (UNL)**.

### 3. Full History Server (Full History Node)

A rippled instance configured to store the **complete history** of all transactions and ledger states ever recorded on the XRP Ledger.

**The scale of full history (as of late 2023):**
- Approximately **27TB** of disk space
- Stored on commercial-grade solid-state drives
- Grows by an average of **12GB per day**

Running a full history node carries significant cost and requires experienced system administrators.

**Why not everyone needs full history:**
- Most transactions only require knowledge of the **current ledger state**
- When a stock node receives a query it can't answer due to lack of history, it falls back on a full history node and relays the response
- This separation allows efficient transaction processing without massive storage requirements

---

## The Unique Node List (UNL)

The UNL is one of the most important concepts in XRP Ledger infrastructure.

### What is the UNL?

The UNL is a **list of trusted validators**. Each validator has its own UNL - in other words, each validator has its own list of other validators that it trusts.

Most validators in the wild use a **default UNL (dUNL)** - a predefined list distributed with rippled.

### Published Default UNLs

There are two main published dUNLs:
1. **XRP Ledger Foundation** dUNL
2. **Ripple** dUNL

The theory: These entities provide a reliable list of trustworthy validators. Because you trust the publisher, you can trust their list as a starting point for your own UNL.

There's also a **Negative UNL** - a list of nodes considered untrustworthy by the publisher.

### Purpose of the UNL

**1. Authoritative Transaction Validation**
- Validators on the UNL are considered authoritative sources
- They determine the final state of the XRP Ledger
- Consensus is reached when a **supermajority** (80%+) of UNL validators agree

**2. Security Against Attacks**
- Guards against malicious actors and **Sybil attacks**
- Bad actors would need to gain trust and approval to be included
- Makes the XRP Ledger resistant to takeover attempts

**3. Network Reliability**
- Ensures validators are reputable and operate reliably
- Validators must adhere to network rules
- Minimizes risk of disruptions from unreliable or adversarial validators

**4. Amendment Voting**
- UNL validators vote on protocol amendments
- For rippled to be updated in production, amendments must be passed by a supermajority of UNL validators

### Becoming a Trusted Validator

Getting on the UNL involves gaining trust and approval from the entities that maintain a dUNL. The XRP Ledger Foundation has published [general guidelines for inclusion](https://foundation.xrpl.org/).

**Note:** Even if your validator isn't on the UNL, it still plays an important role in overall network health.

---

## History Management

### Automatic Online Deletion

Rippled features automatic online deletion - a disk space management tool that automatically removes older ledger versions.

**Default configuration:**
- Deletes history older than the most recent **2000 ledger versions**
- Keeps approximately **15 minutes** of ledger history
- Prevents excessive disk usage

When we configure our rippled node later, we'll look at how to configure online deletion for your needs.

### History Sharding

Sharding is a technique for efficiently managing and distributing the extensive historical transaction data of the ledger.

**How it works:**
- Divides the ledger's history into smaller, manageable pieces called **shards**
- Shards are distributed across network nodes configured to support sharding
- Improves **scalability** and **accessibility** of complete history

This allows the network to maintain full history collectively without every node needing to store everything.

---

## Summary

| Node Type | Submits Txns | Maintains History | Consensus | Requirements |
|-----------|--------------|-------------------|-----------|--------------|
| **Stock Server** | Yes | Limited | No | Basic server |
| **Validator** | Yes | Limited | Yes (if on UNL) | High uptime, performance |
| **Full History** | Yes | Complete (27TB+) | Optional | Significant storage, cost |

**Key Takeaways:**

- **rippled** is the core software of the XRP Ledger
- Three types of node configuration: stock, validator, full history
- Stock servers submit transactions and maintain limited history
- Validators participate in consensus but need UNL inclusion for influence
- Full history nodes are resource-intensive but vital for historical queries
- The **UNL** guards against attacks, ensures reliability, and determines final ledger state
- rippled supports advanced features like automatic online deletion and history sharding

---

## What's Next

In the next lecture, we'll prepare to build our first rippled stock node.

---

## Resources

- [Command Line Usage](https://xrpl.org/docs/infrastructure/commandline-usage)
- [Run rippled as a Validator](https://xrpl.org/docs/infrastructure/configuration/server-modes/run-rippled-as-a-validator)
- [XRP Ledger Foundation - Validator Guidelines](https://foundation.xrpl.org/)
