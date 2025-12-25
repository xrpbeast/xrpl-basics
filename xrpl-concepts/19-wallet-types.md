# Wallet Types

As a developer working on the XRP Ledger, it's important to understand the tools your users will be using to interact with your applications. One of the key tools is a wallet, which is where the user stores their private key for signing transactions.

While there are various types of wallets, the most crucial distinction you need to understand is the difference between **hot** and **cold** wallets.

---

## Hot Wallets

A hot wallet is any wallet that is **connected to the internet**.

This connection allows for quick and convenient access to assets, making hot wallets a popular choice for day-to-day transactions. However, this convenience comes with a trade-off: hot wallets are more vulnerable to online threats like hacking and malware.

**Characteristics:**
- Always or frequently connected to the internet
- Quick access for transactions
- Convenient for everyday use
- Higher exposure to online threats

---

## Cold Wallets

A cold wallet is any wallet that is **not connected to the internet**.

By being offline, cold wallets offer a higher level of security against online attacks. They are typically used for long-term storage of assets or when security is a top priority.

**Characteristics:**
- Disconnected from the internet
- Higher security against online threats
- Better suited for long-term storage
- Less convenient for frequent transactions

---

## The Classification Isn't Always Black and White

It's important to recognize that the distinction between hot and cold wallets depends on whether the wallet is connected to the internet **at a given moment**. A wallet that's usually cold can become hot when you connect it, and vice versa.

---

## Related Wallet Terms

### Hardware Wallets

Hardware wallets are often referred to as cold wallets, but it's important to recognize that it's not the physical device that determines the status. It's the connection (or lack of connection) to the internet.

Hardware wallets are physical devices that remain disconnected until you specifically connect them via a USB cable or Bluetooth.

**Popular hardware wallets on the XRP Ledger:**
- Ledger
- Trezor

When connected to sign a transaction, they temporarily become "hot" for that moment, but the private key never leaves the device.

### Software Wallets

Software wallets are applications that run on a computer or mobile device. They are usually connected to the internet, making them hot wallets in most cases. However, as with hardware wallets, it's the connection to the internet that determines the classification.

**Popular software wallets on the XRP Ledger:**
- Xaman (formerly XUMM)
- Crossmark

### Paper Wallets

A paper wallet represents a method of storing a private key on a rudimentary storage medium like a piece of paper, a metal plate, or some other durable mechanism.

**Considerations:**
- Not very practical for regular use
- Highly secure against hacking (completely offline)
- Vulnerable to physical threats like theft or fire
- Requires importing into another wallet type to use

---

## The Primary Purpose of Any Wallet

Just remember that while wallets come in all varieties and often have lots of flashy features, the primary purpose of a wallet is to **securely store a private key**.

Often, it's how you store and use your wallet that determines its security, not the wallet type itself.

---

## Why Should Developers Care?

As a developer, your main concern will be how to interact with users, enabling them to sign transactions securely and efficiently. Understanding that your users will likely have an array of different wallet types is an important point to grasp.

### Hot Wallets from a Developer Perspective

Hot wallets are great because they provide the best user experience, and the developer gets to interact with a powerful SDK that often simplifies the task of getting transactions signed. Better still:

- You don't touch key management
- The user remains in full control of their private key
- They follow a **pull transaction flow** (as discussed in the previous lesson)

### The Multi-Wallet Challenge

The unfortunate reality for you as a developer is that there are **multiple hot wallet providers** for XRP Ledger users. This means you face a decision: which wallets do you support?

When you opt not to support a wallet, you likely reduce your potential audience. As a rule, users won't change wallet providers just because you don't support their preferred wallet. This is something you need to seriously consider in your application design.

### Hardware Wallet Complexity

To complicate matters further, a significant number of users have hardware wallets like Ledger or Trezor. Integrating those wallets is often more complicated for developers, and the user experience typically involves additional steps:

1. Connecting the physical device
2. Confirming the transaction physically on the device

This introduces friction into the user journey.

---

## Summary

| Wallet Type | Internet Connection | Security Level | Convenience | Integration Complexity |
|-------------|---------------------|----------------|-------------|------------------------|
| **Hot (Software)** | Connected | Lower | High | Easier (SDK available) |
| **Cold (Hardware)** | Disconnected | Higher | Lower | More complex |
| **Paper** | Never connected | Highest | Lowest | Not practical |

### Key Takeaways

1. **Hot wallets** are connected to the internet, convenient but more vulnerable
2. **Cold wallets** are offline, more secure but less convenient
3. **Hardware wallets** are cold when disconnected, temporarily hot when in use
4. **Software wallets** like Xaman provide excellent developer SDKs
5. **Paper wallets** are impractical but maximally secure against online threats
6. **The classification** depends on internet connection at any given moment
7. **As a developer**, you need to carefully determine which wallets to support
8. **Each option** has pros and cons affecting user experience and technical complexity

---

## What's Next

In the next lesson, we'll dive into practical wallet integration, starting with how to implement Xaman (formerly XUMM) into your XRP Ledger applications.
