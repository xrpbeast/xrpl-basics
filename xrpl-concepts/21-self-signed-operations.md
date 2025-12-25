# Self-Signed Operations

It's time to look at the second type of integration: **self-signed operations**.

What do we mean by self-signed? It's where you, as the developer, sign the transaction directly in your code using a private key that you have access to. This type of integration is common in backend processes, where the application itself needs to interact with the XRP Ledger without user involvement.

---

## Real World Use Cases

Let's look at some practical scenarios where self-signed operations make sense.

### 1. Wallet Applications

First, let's not confuse this with user interaction via a third-party wallet SDK. This use case is where **you build an application that acts as a wallet**.

There are many reasons why an application developer may wish to provide users with an application that secures and uses their key directly.

The flow of this application would not be considered backend, but it is self-signed inasmuch as it's your code that is signing the transaction with a private key to which your code can access.

**Example flow:**
- User stores their private key in local storage
- The key remains in the user's custody
- Your code running on their device accesses the key
- Your code signs the transaction on their behalf

The key point is that no third-party wallet SDK is involved. Your application handles the entire signing process.

### 2. Data Integrity and Proof of Existence

Your application records data on the XRP Ledger to leverage its **immutability**. This could be anything from:

- Legal documents
- Contracts
- Sensor data
- Audit trails
- Certificates

The application signs and submits transactions containing hashes or other representations of the data, ensuring that the information is permanently and securely recorded on the ledger. This provides a **verifiable proof of existence** that can be independently validated.

### 3. Automated Recurring Payments

You may offer a service where users can schedule regular payments such as:

- Monthly subscriptions
- Rent payments
- Donations
- Scheduled transfers

The application automatically signs and submits payment transactions at the scheduled intervals, ensuring timely transfers without user intervention. Users set up the schedule once and the application handles the rest.

**Architectural options:**

| Approach | Description |
|----------|-------------|
| **Desktop application** | Keys stored locally, app installed on user's machine. Essentially an automated traditional wallet. |
| **SaaS product** | You custody the user's private key in your secure storage, with a task runner handling the signing. |

### 4. Batch Processing of Transactions

Your application needs to process multiple transactions at once, such as:

- Payroll distribution
- Bulk payments to suppliers
- Reward distributions
- Airdrop campaigns
- Dividend payments

The application compiles a batch of transactions, signs them using a private key, and submits them all. This method is efficient and reduces the operational overhead of handling many individual transactions separately.

---

## The Core Concept

These use cases illustrate what self-signed operations mean on the XRP Ledger:

> **Your code has access to the private key and you have no need to interact with a user wallet SDK.**

In this type of integration, you'll most likely be using something like the **xrpl.js SDK** to interact with the XRP Ledger directly.

---

## Self-Signed vs Wallet Integration

| Aspect | Self-Signed | Wallet Integration |
|--------|-------------|-------------------|
| **Key access** | Your code has the key | User's wallet has the key |
| **Signing location** | In your application | In the wallet app |
| **User involvement** | None or minimal | Required for each transaction |
| **SDK used** | xrpl.js (or similar) | Wallet provider's SDK |
| **Use case** | Backend, automation | User-facing transactions |

---

## Security Considerations

When your code has access to private keys, security becomes paramount:

- **Never expose keys** in client-side code (unless it's a wallet app)
- **Use secure storage** for keys (environment variables, secrets managers, HSMs)
- **Implement proper access controls** for who can trigger transactions
- **Audit logging** for all signed transactions
- **Key rotation** policies where applicable

---

## Summary

Self-signed operations are appropriate when:

1. **Building a wallet application** where your code manages the key
2. **Recording data** for proof of existence
3. **Automating payments** on a schedule
4. **Processing transactions in bulk** for efficiency

### Key Takeaways

1. **Self-signed** means your code has direct access to the private key
2. **No wallet SDK** is required for these operations
3. **Common in backend** processes and automation
4. **Use xrpl.js** or similar SDKs for direct ledger interaction
5. **Security is critical** when handling private keys
6. **Multiple architectures** are possible (desktop app, SaaS, backend service)

---

## What's Next

With an understanding of self-signed operations, we'll next explore the third integration type: querying the XRP Ledger for data without submitting transactions.
