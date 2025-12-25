# Integration Types

Now that you understand transaction flow and querying options, it's time to explore how these elements fit into various use cases. Understanding the different types of integrations is crucial for designing applications that effectively interact with the XRP Ledger.

---

## Three Key Integration Types

### 1. Wallet Integration

The most common integration type. Your application facilitates transactions where **users sign and submit transactions themselves** using their wallet.

**Use cases:**
- E-commerce payments
- NFT purchases
- Token swaps
- Any user-initiated transaction

### 2. Self-Signed Operations

Your application performs operations on the XRP Ledger **without user involvement**. The application signs and submits transactions either on behalf of itself or a third party.

**Use cases:**
- Automated payments (payroll, subscriptions)
- Bot operations
- Backend processes
- Custodial services

### 3. Querying

Retrieving data from the XRP Ledger **without initiating transactions**. No signing involved, just data retrieval.

**Use cases:**
- Monitoring activity
- Reporting and analytics
- Price feeds
- Account balance displays

---

## The Wallet Integration Problem

Let's explore wallet integration through a real scenario.

### The Watch Store Example

You're asked to integrate the XRP Ledger into an e-commerce store selling luxury watches. You need to:
1. Take a payment from the user
2. Create and transfer an NFT as proof of purchase

Following the transaction flow: you create the transaction sending payment from the user's account to the shop owner. The user is on the checkout page. Now they need to **sign that transaction**.

**The problem:** How do you get them to sign it?

### Why You Can't Just Ask for the Key

You could flash up a box asking the user to paste their secret key...

**Good luck with that.**

You can't:
- Sign for them (you don't have their key)
- Ask them to expose their private key on your website

So how do you do it?

---

## Push vs Pull Transactions

### Traditional Push Flow (User-Initiated)

In the early days, transactions were "push" based:
1. User opens their wallet
2. User enters destination and amount
3. User submits the transaction

**Problems with push for e-commerce:**
- Merchant provides payment details, hopes user pays correctly
- Merchant must monitor for incoming transactions
- Must somehow map payments to orders
- High risk of user error and lost funds
- Increased risk of phishing attacks
- Poor user experience

### Modern Pull Flow (Merchant-Initiated)

Think of how credit card payments work:
- Vendor asks for your card number
- Giving the number is your authorization
- Vendor "pulls" the payment from you

**The vendor doesn't give you their account details and ask you to send payment.**

What we need:
1. Generate the transaction with correct values
2. Request the user authorize it (like a credit card)
3. But without exposing their secret key

---

## The Solution: Wallet SDKs

The developers of XUMM (now **Xaman**) recognized this problem was holding back XRP Ledger adoption. They developed a solution that:

- **Doesn't change the user journey** they're comfortable with
- **Adapts the tech** to meet user expectations
- Keeps the **private key sacrosanct** and secure

### How It Works

Xaman provides an SDK that allows developers to:
1. **Create the transaction** in your application
2. **Submit it for user review** via the SDK
3. User **signs in a safe, familiar interface** (the wallet app)
4. You receive the **signed transaction** to submit

The flow mirrors what users experience today:
- Banking app approvals
- One-time codes
- Mobile payment confirmations

### The Impact

This seemingly obvious solution (in hindsight) was a major step forward in 2018. It enabled an entire ecosystem of applications to be built on the XRP Ledger.

---

## Benefits of Wallet Integration

### For Users
- Secure, familiar experience
- Same flow across all integrated sites
- Private key never leaves their wallet
- Full control over transaction approval

### For Developers
- No key management complexity
- No custody of user funds
- Simple SDK integration
- Focus on your application logic

---

## Visual Comparison

### Push Flow (Old Way)
```
User → Opens Wallet → Enters Details → Submits → Hopes Merchant Receives
                                                        ↓
                                               (Merchant monitors)
```

### Pull Flow (Modern Way)
```
Merchant → Creates Transaction → Sends to Wallet SDK
                                        ↓
                                User Reviews in Wallet
                                        ↓
                                User Approves/Signs
                                        ↓
                                Merchant Submits Signed Tx
```

---

## Key Takeaways

1. **Three integration types**: Wallet, Self-Signed, Querying
2. **Wallet integration** is most common for user-facing apps
3. **Push transactions** have poor UX for e-commerce
4. **Pull transactions** (merchant-initiated) mirror credit card flows
5. **Wallet SDKs** solve the signing problem without exposing keys
6. **Xaman** pioneered this approach in 2018
7. **You don't handle private keys** in wallet integrations

---

## What's Next

In the next lecture, we'll review the different types of wallets before diving into what wallet integration looks like in practice.
