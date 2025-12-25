# XRP Ledger Infrastructure: Introduction

Welcome to the section on XRP Ledger Infrastructure.

---

## Distributed by Design

The XRP Ledger has a **distributed design**, which means there is no single central authority governing the network. Instead, it relies on a distributed network of nodes that collaborate to maintain the ledger.

No company, government, or individual controls the XRP Ledger. It operates because thousands of participants around the world choose to run the software and follow the same rules.

---

## What Does "Running Infrastructure" Mean?

When we talk about running infrastructure, we're talking about running the **rippled** (pronounced "ripple-dee") core software.

Rippled is:
- A **daemon** (background service) that runs on Linux
- Responsible for **validating transactions**
- Responsible for **propagating transactions** across the network
- The core software that makes you a participant in the XRP Ledger network

By running rippled, you become an active part of the decentralized network rather than just a user of it.

---

## What We'll Cover in This Section

In this course section, we're going to:

1. **Dig deeper into the principles** of XRP Ledger infrastructure
2. **Discuss practical requirements** for running your own infrastructure
3. **Build a node together** from scratch
4. **Configure it** to run as both a submission node and a validator

By the end of this section, you'll have hands-on experience setting up and running your own XRP Ledger infrastructure.

---

## Why Run Your Own Infrastructure?

There are several reasons you might want to run your own rippled server:

**For Developers:**
- Direct access to the ledger without relying on third-party servers
- Lower latency for transaction submission
- Full control over your connection to the network
- Access to complete ledger history (if running a full history node)

**For Businesses:**
- Reliability and uptime guarantees
- Privacy (your queries don't go through third parties)
- Compliance requirements
- Part of your production infrastructure

**For the Network:**
- Contributing to decentralization
- Helping validate transactions (if running a validator)
- Supporting the health and resilience of the network

---

## What's Next?

In the next lecture, we'll answer the fundamental question: **What is rippled?**

We'll explore:
- The different roles a rippled server can perform
- How rippled fits into the broader XRP Ledger ecosystem
- What happens inside a rippled server

Let's get started!
