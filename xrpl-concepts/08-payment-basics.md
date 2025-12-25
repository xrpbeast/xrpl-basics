# Payment Basics

In the last lecture, we learned how to create accounts using a faucet and programmatically using the JavaScript SDK's `generate()` method. In this lecture, we will use a payment transaction to fund our as-yet-unactivated account.

As a side note, the SDK has a method called `fundWallet()` which you can use on the testnet to fund a wallet immediately after creating it. This is a nice feature when developing and you want to spin up a bunch of accounts with some XRP quickly.

---

## The Goal

We're going to activate an unfunded account by sending XRP from a funded account. To do this, we'll use a **payment transaction**.

While this is fairly straightforward, there are several important concepts to understand first.

---

## Understanding Transactions

In this lecture, we're using the JavaScript SDK, which is a layer on top of the XRP Ledger. You *could* make a payment by calling the rippled APIs directly using JSON-RPC, but the SDK does a lot of heavy lifting for you.

**Key insight**: Making a payment is just a type of transaction on the XRP Ledger. It's probably the most common, but ultimately it's just a transaction nonetheless.

All transactions have:
- **Common fields** - Some required, some optional (apply to ALL transactions)
- **Transaction-specific fields** - Some required, some optional (specific to each transaction type)

---

## The Payment Process

Sending a payment programmatically is a multi-step process, and the ordering is important:

1. **Create** the payment object with all required info
2. **Prepare** the transaction (fetch data from ledger, like sequence number)
3. **Sign** the transaction (offline cryptographic signing)
4. **Submit** and wait for the result

---

## Common Transaction Fields

Every transaction on the XRP Ledger shares [common fields](https://xrpl.org/docs/references/protocol/transactions/common-fields). Only four are required:

| Field | Description |
|-------|-------------|
| `Account` | The r-address of the sending account |
| `TransactionType` | The type of transaction (e.g., "Payment") |
| `Fee` | The transaction cost in drops |
| `Sequence` | Must be exactly one greater than the account's last transaction |

### About Fees

Every transaction has a fee - it's a cost of using the ledger and a form of spam prevention. Important notes:
- Different transaction types can have different fees
- Fees can change based on network conditions
- The SDK's `autofill()` method determines the correct fee for you automatically

### About Sequence Numbers

When a transaction is submitted, it's only valid if the sequence number is exactly one greater than the previous transaction from that account. Think of it as an ordering system - the order of transactions matters, and sequence numbers enforce this.

**Good news**: The SDK's `autofill()` method handles this for you by fetching the current sequence number from the ledger.

---

## Payment-Specific Fields

The [Payment transaction](https://xrpl.org/docs/references/protocol/transactions/types/payment#payment) has its own required fields:

| Field | Description |
|-------|-------------|
| `Amount` | How much to send (in drops for XRP, or an object for tokens) |
| `Destination` | The r-address to send to |

### Specifying the Amount

This is important - you can send XRP or issued tokens, and the format differs:

**For XRP:**
```javascript
Amount: "1000000"  // 1 XRP in drops, as a STRING
```

**For issued tokens:**
```javascript
Amount: {
  value: "100",
  currency: "USD",
  issuer: "rIssuerAddress..."
}
```

Remember: 1 XRP = 1,000,000 drops. The SDK provides `xrpToDrops()` helper:

```javascript
import { xrpToDrops } from "xrpl";

Amount: xrpToDrops("20")  // Converts "20" XRP to "20000000" drops
```

---

## Complete Code Example

```javascript
import { Client, Wallet, xrpToDrops } from "xrpl";

// Step 1: Get wallet from stored seed
const wallet = Wallet.fromSeed("sEdYourSeedHere");

// Destination (unfunded account we want to activate)
const destinationAddress = "rDestinationAddressHere";

// Connect to testnet
const client = new Client("wss://s.altnet.rippletest.net:51233");

try {
  await client.connect();

  // Step 2: Create the payment object
  const payment = {
    TransactionType: "Payment",
    Account: wallet.classicAddress,
    Amount: xrpToDrops("20"),  // 20 XRP
    Destination: destinationAddress,
  };

  // Step 3: Prepare (autofill adds Fee, Sequence, etc.)
  const prepared = await client.autofill(payment);

  // Step 4: Sign the transaction
  const signed = wallet.sign(prepared);

  // Step 5: Submit and wait for validation
  const result = await client.submitAndWait(signed.tx_blob);

  console.log("Result:", result);

} catch (error) {
  console.error("Error:", error);
} finally {
  await client.disconnect();
}
```

---

## Understanding Transaction Results

Here's something crucial that surprises many developers: **a successful response does NOT mean the transaction succeeded**.

The XRP Ledger returns the transaction result in the response, but it's not thrown as an error. A failed payment is not considered an exception - you get a "200 OK" type response regardless.

### Checking the Result

You must manually check the transaction result:

```javascript
const result = await client.submitAndWait(signed.tx_blob);

if (result.result.meta.TransactionResult === "tesSUCCESS") {
  console.log("Payment succeeded!");
} else {
  console.log("Payment failed:", result.result.meta.TransactionResult);
}
```

### Transaction Result Codes

There are [six types of transaction results](https://xrpl.org/docs/references/protocol/transactions/transaction-results):

| Prefix | Meaning |
|--------|---------|
| `tes` | **Success** - Transaction succeeded |
| `tec` | **Claimed cost** - Transaction failed but fee was claimed |
| `tef` | **Failure** - Transaction failed, fee not claimed |
| `tem` | **Malformed** - Transaction was malformed |
| `ter` | **Retry** - Might succeed if retried |
| `tel` | **Local error** - Local server error |

**Anything other than `tesSUCCESS` means you'll likely need to handle the failure.**

---

## A Deliberate Failure Example

Let's see what happens when we try to send only 1 XRP to an unactivated account:

```javascript
Amount: xrpToDrops("1"),  // Only 1 XRP
```

**Result**: The transaction fails with `tecNO_DST_INSUF_XRP`

Why? Because the base reserve is 10 XRP. An account can only be activated if it receives at least 10 XRP. Sending 1 XRP isn't enough to create the account.

What happens:
- The sending account's balance stays the same (minus the fee)
- The destination account still doesn't exist
- The transaction is recorded as failed
- You can see the failed transaction in the explorer

**Fix**: Send at least 10 XRP (we used 20 to have some spending power):

```javascript
Amount: xrpToDrops("20"),  // 20 XRP - enough to activate!
```

Now the transaction succeeds with `tesSUCCESS`, and the destination account is activated with a 20 XRP balance.

---

## Verifying on the Explorer

After a successful payment:

**Sending account**:
- Balance decreased by 20 XRP + fee
- Transaction shows as successful

**Destination account**:
- Now exists and is activated
- Balance shows 20 XRP

You can check accounts at:
- Testnet: https://testnet.xrpl.org
- Mainnet: https://xrpl.org

---

## Key Takeaways

1. **Payments are transactions** with common fields + payment-specific fields
2. **Use `autofill()`** - It handles Fee and Sequence for you
3. **Use `xrpToDrops()`** - Correctly formats XRP amounts
4. **Sign before submitting** - `wallet.sign(prepared)`
5. **Use `submitAndWait()`** - Waits for validation
6. **Always check the result** - Success response ≠ successful transaction
7. **Know the result codes** - `tesSUCCESS` is what you want
8. **Remember the reserve** - New accounts need at least 10 XRP to activate

---

## What's Next

We've covered creating and activating accounts. The final topic in this section is **deleting an account** - which we'll cover in the next lecture.

---

## Resources

- [Client Libraries](https://xrpl.org/docs/references/client-libraries) - Official SDKs
- [Public Servers](https://xrpl.org/docs/tutorials/public-servers) - WebSocket endpoints
- [Common Transaction Fields](https://xrpl.org/docs/references/protocol/transactions/common-fields)
- [Payment Transaction](https://xrpl.org/docs/references/protocol/transactions/types/payment#payment)
- [Transaction Results](https://xrpl.org/docs/references/protocol/transactions/transaction-results)
