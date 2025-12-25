# Core Concepts

This is one of the most important sections to understand. It's longer and more theoretical than other sections, but taking the time to fully understand each concept before moving on will pay dividends as you progress through your XRP Ledger development journey.

Don't worry if some of these concepts feel a bit abstract at first. We'll revisit them throughout the course with practical examples that will make everything click.

---

## Infrastructure

The XRP Ledger has what we call a "distributed design." This means there's no single central authority governing the network - no company, government, or individual that controls everything. Instead, the XRP Ledger relies on a distributed network of computers (called "nodes") that collaborate to maintain the ledger.

As of October 2023, there are over 600 nodes located at different points all around the world. These nodes work together to process transactions, validate them, and keep the entire network running smoothly.

At the heart of XRP Ledger infrastructure is the **rippled** server software. This is the core software that anyone can download and run to become part of the XRP Ledger network. Yes, anyone - including you! If you wanted to, you could set up your own node and contribute to the network.

### The Different Roles a rippled Server Can Perform

Not all nodes do the same job. There are different roles a rippled server can perform:

**Submission Node**

A submission node handles the submission of transactions to the network for processing and inclusion in the ledger. Think of it like a post office - when you want to send a transaction, it's the submission node that accepts your transaction and passes it along to the network.

**Validator**

A validator participates in the consensus process (which we'll explain next) to verify and agree upon the validity of transactions. Validators are like the judges of the network - they work together to decide which transactions are legitimate and in what order they should be processed.

**Full History Node**

A full history node holds a copy of the entire history of the XRP Ledger, providing a complete record of all transactions ever processed to anyone who needs it. This is like a complete archive or library of everything that has ever happened on the network.

Operators can host rippled on their own hardware or use cloud services like AWS or Google Cloud. The requirements for running a rippled server vary based on which role you want it to perform - a full history node needs much more storage space than a simple submission node, for example.

Running a rippled server also requires staying engaged with the community to keep up with software updates. These updates are called "amendments," which we'll discuss in more detail later in this section.

---

## Consensus

Now let's talk about one of the most important concepts: consensus.

In a traditional centralized payment system - like a bank - the bank is the administrator who gets the final say in how payments occur. The bank decides whether your transaction is valid, updates your balance, and maintains the official record.

The XRP Ledger is decentralized, so it doesn't have a bank or administrator to do that. Instead, all participants follow an agreed set of rules which ensures every participant can agree on the exact same series of events and their outcome at any point in time. We call this set of rules the **XRP Ledger Consensus Protocol**.

David Schwartz, one of the original developers of the XRP Ledger, describes the consensus protocol as simply being the solution to the "double-spend problem." The double-spend problem is the challenge of preventing someone from successfully spending the same digital money twice. Imagine if you could copy a digital dollar and spend it in two places at once - that would be a disaster for any payment system!

The hardest part about solving this problem is putting transactions in order, because there's no single authority we can rely on to say "this transaction happened first." The consensus protocol defines the rules of the system for everyone to follow, and through a series of "consensus rounds," the validators come to agreement on the correct ordering.

### The Important Properties of XRPL Consensus

The consensus protocol has several important properties that make the XRP Ledger reliable:

1. **Agreement**: Everyone who uses the XRP Ledger can agree on the latest state and which transactions have occurred in which order.

2. **No Central Point of Failure**: All valid transactions are processed without needing a central operator. There's no single point of failure that could bring down the entire network.

3. **Resilience**: The ledger can make progress even if some participants join, leave, or behave inappropriately. The network keeps working even when some nodes go offline or act maliciously.

4. **Safety Over Speed**: If too many participants are unreachable or misbehaving, the network fails to make progress rather than diverging or confirming invalid transactions. In other words, the network would rather pause than make a mistake.

5. **Energy Efficiency**: Confirming transactions does not require wasteful or competitive use of resources, unlike proof-of-work blockchain systems like Bitcoin that require enormous amounts of electricity.

### How Consensus Actually Works

Through a series of consensus rounds, the validators come to a consensus on the correct ordering of transactions. The time taken to achieve consensus varies due to the potential number of rounds that might be required, which is why the time quoted for a ledger to close with finality is stated as being between 3 to 5 seconds.

Don't worry if this is still a little foggy. We'll get into more detail later in the course. For now, the key takeaways are:

- Consensus is the XRP Ledger's solution to the double-spend problem
- Consensus is a set of rules which all participants must follow
- Consensus is achieved through a series of rounds where validators reach agreement
- A new ledger is finalized through consensus approximately every 3 to 5 seconds

---

## Ledger Versions (What Other Blockchains Call "Blocks")

The first thing to understand is that within the XRP Ledger, what other blockchains call "blocks" are referred to as "ledger versions" - usually shortened to just "ledgers." If you're coming from another blockchain like Ethereum or Bitcoin, this is worth making a mental note for when you dig into the documentation.

Every ledger version has two important identifiers:
- A **ledger index** (a number that identifies the correct order of the ledgers - like ledger #85,000,000)
- A unique **identifying hash** (a cryptographic fingerprint that uniquely identifies this exact ledger)

### The Three States a Ledger Can Be In

At any given time, ledgers can be in one of three states:

**Validated Ledger**

A validated ledger is one that has been through the consensus process and is therefore considered fully validated and immutable (meaning it cannot be changed). Once a ledger is validated, its contents - including all transactions and account balances - cannot be altered. This is the "official record" that everyone agrees on.

**Open Ledger**

The open ledger represents the most recent set of transactions and account balances. This ledger is actively being updated as new transactions are processed. It's called "open" because it's subject to change as more transactions are added. Think of it as a draft that's still being written.

**Pending Closed Ledger**

A pending closed ledger is in a state where new transactions can no longer be added, but consensus has not yet been reached. Therefore, it's not yet validated and immutable. Generally, there will be either zero or one ledger in this state at any time.

While in this state, nothing new can be added, but it's possible that the entire ledger could be replaced with a different version if the validators disagree about its contents. This is why, throughout this course, you'll learn about the importance of understanding ledger states and ensuring your code takes this into account.

What's interesting is that you can query the ledger to get transactions back in any of these states. There are reasons why this might be helpful, and we'll explore them as we progress through this course.

### The Structure of a Ledger

Each ledger consists of three main parts:

**1. Header**

The header contains the ledger index and its hash, plus the hash of its parent ledger (the ledger that came before it) and a few other pieces of metadata. This creates a chain where each ledger is linked to the one before it.

**2. Transaction Set**

The transaction set contains all the transactions that occurred within the ledger, along with metadata that shows exactly how each transaction was processed and how it affected the ledger. This is the record of everything that happened.

**3. State Data**

The state data represents a snapshot of all accounts, balances, settings, and other pertinent information as of this ledger version. Having the current state available in the last validated ledger allows a node to operate without knowing the entire history of the ledger - a concept that will become clearer when we discuss different types of node operation.

---

## Accounts

An account plays an important role within the XRP Ledger. It's much more than just an address to send or receive XRP - it's your complete identity on the ledger.

### What Makes Up an Account

Let's look at what makes up an account:

**Public Address**

This is referred to simply as an "address" and looks something like `rN7n3473SaZBCG4dFL83w7a1RXtXtbk2D9`. It's your unique identifier on the network that others use to send you XRP or tokens.

**XRP Balance**

Every account must have some XRP. This isn't optional - you cannot have an account with zero XRP (we'll explain why in the Reserves section).

**Sequence Number**

This ensures that transactions you send are applied in the correct order and only once. Every time you send a transaction, this number increases by one. This prevents someone from replaying your old transactions.

**Transaction History**

A record of all transactions that have affected the account and its balances over time.

**Authorization Method**

How the account proves ownership and authorizes transactions. This can be:
- A master key pair (the default)
- A regular key pair (an alternative key you can set up)
- A multi-signer list (requiring multiple people to authorize transactions)

**Owned Objects**

A list of other ledger objects that the account owns, such as NFTs, trust lines (connections to hold other tokens), open trade offers, and more.

### How to Get an Account

In the first instance, you get an account by generating a master key pair (a public address and private key) and then sending some XRP to that address. The XRP can come from:
- Another active wallet
- An exchange where you purchase XRP
- The testnet faucet (for testing purposes)
- Another participant of the network

An account must contain some XRP because having an account on the XRP Ledger has a real-world cost. This cost is known as a "reserve." Once you have an account with enough XRP to meet the account reserve requirement, your account is considered activated and ready for use.

---

## Reserves: How the XRP Ledger Prevents Spam

The XRP Ledger uses XRP reserves as a form of spam prevention. This is an elegant solution to a real problem: without some cost to creating accounts and objects, bad actors could flood the network with millions of fake accounts and junk data.

There are two types of reserves:

**Base Reserve**

The base reserve is the minimum amount of XRP that must be held in an account for it to be considered active and operational on the ledger. This reserve acts as a gatekeeper to prevent frivolous creation of accounts, since each new account must fund this base amount to exist on the ledger.

**Owner Reserve**

The owner reserve is an incremental amount of XRP that is required for each object that an account owns in the ledger. These objects include things like NFT pages, trust lines, open offers on the decentralized exchange, and more. The owner reserve grows with the number of objects, serving as a protective measure against ledger spam by making it costly to hold excessive numbers of objects.

### Important Things to Know About Reserves

Both types of reserves are **locked, not spent**. This is an important distinction! The XRP isn't gone - it's just locked up and unusable while you have the account or objects.

The reserves are released when:
- Objects are removed (in the case of owner reserves) - for example, if you close a trust line
- The account is deleted (in the case of the base reserve)

The exact amounts for the base and owner reserves are determined by network consensus and can change over time. Validators participate in a fee voting process to adjust these reserve requirements in response to changes in the network and the price of XRP. The goal is to balance accessibility (keeping it affordable for normal users) with protection against abuse (making spam attacks expensive).

---

## Transactions: The Only Way to Change the Ledger

A transaction is the only way to modify the XRP Ledger. This is a fundamental principle: if you want to change anything - send XRP, create an NFT, set up a trust line, change your account settings - you must submit a transaction.

Transactions are only considered final if they are:
1. Signed (with your private key)
2. Submitted (to the network)
3. Accepted into a validated ledger version (following the consensus process)

Some ledger rules also generate what are called "pseudo-transactions," which aren't signed or submitted by users but still must be accepted by consensus.

Here's something that surprises many newcomers: transactions that fail are also included in ledgers! Why? Because they still modify balances of XRP to pay for the anti-spam transaction cost, known as the fee. This prevents people from spamming the network with invalid transactions for free.

### What Can Transactions Do?

Transactions can do much more than just send XRP. You can:
- Make changes to account settings, such as rotating cryptographic keys
- Mint an NFT and then sell it
- Escrow your XRP (lock it up until certain conditions are met)
- Create a trust line to another account to hold an issued asset, such as a USD stablecoin or project token
- Place offers on the decentralized exchange
- And much more

We'll explore all the different types of transactions throughout this course.

### Understanding Transaction Structure

To put this in terms that might be more familiar: a transaction type is essentially a function of the ledger. You call the transaction, pass it some data, and expect a result.

Think of the XRP Ledger as an API with only one endpoint called "submit transaction." You can call that function no matter what type of transaction you want, so you need to tell it what type of transaction you're performing.

All transactions have their own defined payloads (the specific data they need), but there are a number of fields which are common to all transactions.

### The Four Mandatory Fields for Every Transaction

**Account**

This is the account submitting the transaction - your address.

**TransactionType**

This tells the network what kind of transaction you're performing, like "Payment," "NFTokenMint," "TrustSet," etc.

**Fee**

Every transaction has a fee. This is how the XRP Ledger protects itself against spam. The fee is a tiny amount of XRP that gets destroyed (not paid to anyone).

**Sequence**

This is the sequence number of the account sending the transaction. Remember that every account has a sequence number to prevent transactions from being applied in the wrong order or multiple times. A transaction is only valid if the sequence number provided is exactly one greater than the account's last recorded sequence number.

There is one exception to this rule involving "tickets" that was introduced with a later amendment, but that's beyond the scope of this section.

There are also optional common fields like Flags, Memos, and LastLedgerSequence, but we'll get to these along with the specific fields for each transaction type in due course.

### Transaction Results

Transactions always yield a result. The rippled server summarizes transaction results with result codes. These codes are grouped into several categories with different prefixes.

While we'll always want to write code that handles every one of these potential result codes, the one we want to see is `tesSUCCESS`.

**However** - and this is very important - if you recall when we talked about ledger states, a `tesSUCCESS` response only confirms the transaction succeeded at submission time. To know that it was actually applied and is permanent, it must be included in a validated ledger.

Along with the result code, you receive metadata which includes detailed information about how the transaction was processed:
- **Transaction ID**: A unique identifier for the transaction
- **Ledger Index**: The ledger number in which the transaction appears
- **Transaction Data**: Information specific to the transaction type
- **Affected Nodes**: A detailed list of ledger objects that were created, deleted, or modified as a result of the transaction

### Transaction Summary

Transactions are the sole means to alter the XRP Ledger. They include various types such as payments and account setting changes, each with a set of common and type-specific fields. They must be signed, submitted, and accepted in a validated ledger to be final, with the outcomes detailed in result codes and metadata.

---

## Fees: Protecting the Network

The XRP Ledger imposes fees to protect the network. These are small transaction costs that prevent spam by destroying a tiny amount of XRP with each transaction.

### The Three Classifications of Fees

**Neutral Fees**

These are charged by the protocol itself and are a cost of using the network. They're mandatory - you can't avoid them. The XRP paid in neutral fees is destroyed (removed from existence), not paid to anyone.

Neutral fees are set at the protocol level by validators through a voting process, which allows the network to adapt to changing conditions.

**Optional Fees**

The XRP Ledger also allows for optional fees that users can set for a variety of reasons, such as trust line quality or transfer fees. These optional fees are user-defined and are not required by the protocol itself.

For example, if you issue a token, you can set a transfer fee so that every time someone transfers your token to another person, a small percentage goes to you.

**Off-Ledger Fees**

These are fees applied to transactions by a third party, such as your wallet provider, marketplace, or financial services app. These aren't part of the XRP Ledger protocol at all - they're just business decisions made by companies building on top of the ledger.

### Understanding the Distinction

It's important to understand the difference:
- **Neutral fees** are mandatory - the protocol requires them
- **Optional fees** are implemented at the protocol level but can be set by users (like token issuers)
- **Off-ledger fees** may be charged by businesses who are using the ledger and charging you for the use of their application or service

Take a moment to let this distinction sink in before moving on.

---

## The Role of XRP

XRP performs a dual role within the XRP Ledger ecosystem.

### Role 1: Securing the Network

First, XRP helps secure the network by being used as a transaction fee and account reserve. This works because XRP has real-world value. Therefore, there's an actual real cost to each transaction or object that you hold on the ledger.

When you scale this and factor in fee escalation (a concept we'll dig into later in the course where fees increase during high network activity), you'll see how the fees play an important role in securing the network.

If XRP were worthless, anyone could spam the network for free. But because XRP has real value, attacking the network with spam would be prohibitively expensive.

### Role 2: A Means of Value Exchange

XRP is what we call a "volatile asset." In other words, its value is not pegged to any other asset - it fluctuates based on supply and demand. This means XRP can be traded for other things of value at both ends of a transaction.

There are a number of companies using XRP in their tech stack, with Ripple being the most prominent. Ripple uses XRP as a form of "bridge currency" for cross-border payments. By using XRP, their customers can move money from one side of the world to the other with finality in a matter of minutes, and for way less than the current financial system charges.

XRP can be used for:
- Being paid for work
- Buying goods and services
- Holding for speculative purposes
- Paying others
- Cross-border remittances
- Trading on exchanges

So to summarize: XRP performs a dual role of both securing the network (as a transaction fee and reserve) and as a means of value exchange.

---

## Amendments: How the XRP Ledger Evolves

Amendments are a mechanism used to enhance or fix issues in the core XRP Ledger software, rippled.

As you learned in the XRP Ledger history lecture, when the XRP Ledger launched, there was no formal method for making changes to the network. But in 2016, a new process called the "amendment process" was introduced, and it brought with it a much more formalized and democratic approach to upgrades.

### How the Amendment Process Works

**Step 1: Proposal**

An amendment usually starts off as a discussion on GitHub and will eventually turn into a formal proposal with an XLS number (like XLS-20 for NFTs). A proposal can come from anyone, but must include:
- A detailed specification of the proposed change
- Its rationale (why it's needed)
- Potential benefits

**Step 2: Discussion and Feedback**

The proposal enters a formal phase of discussion and feedback. Participants - including developers, validators, and community members - review the proposal, ask questions, and provide input to ensure a thorough evaluation of the proposed change.

**Step 3: Implementation**

After gathering feedback and refining the proposal, someone must create an actual implementation of the amendment in code. This implementation will then be thoroughly tested to ensure its compatibility with the existing codebase and to identify any potential issues or vulnerabilities.

**Step 4: Inclusion in rippled**

Eventually, with enough community support, the new feature will make its way into a new version of rippled and be put forward as an amendment to be activated on the network.

**Step 5: Validator Voting**

Once validators upgrade to the version of rippled that contains the amendment, they can vote on their support for it. Each new version of rippled comes with a list of known amendments, and operators of validators can configure their servers to vote for or against each amendment.

**Step 6: Sustained Support**

Amendments must maintain two weeks of continuous support from more than 80% of the trusted validators to be enabled. If support drops below 80% at any point, the amendment is temporarily rejected and the two-week countdown restarts once 80% support is reached again.

This high bar for activation ensures that changes to the network have overwhelming support from the validator community.

### Amendment Blocking

Amendment blocking is what happens when an amendment goes live, but a node is still running an older version of rippled that doesn't include it.

When a node becomes amendment blocked, it can no longer take part in consensus because its software is no longer compatible with the current version of the network. The node essentially gets left behind.

To fix a node that is amendment blocked, the operator simply needs to update to a version of rippled that contains the new amendment.

If you're running infrastructure, avoiding getting amendment blocked is important. Too many nodes being amendment blocked degrades the network's resilience and security.

### Where to Track Amendments

To see a list of all amendments, both past and present, you can review them on the xrpl.org website. If you're interested in seeing the current status of a live amendment that's being voted on, XRPScan offers this facility.

---

## Client Libraries: Making Development Easier

When building applications on the XRP Ledger, developers often leverage client libraries (also called SDKs - Software Development Kits) to interact with the network more efficiently and effectively.

### What Are Client Libraries?

Client libraries are packages or modules that abstract away the complexities of raw API calls into easy-to-use functions and methods that can be directly integrated into your application code.

In other words, instead of having to understand the exact format of every API request and response, you can just call simple functions like `client.submitTransaction()` or `wallet.getBalance()`. The library handles all the complicated stuff behind the scenes.

Generally, these libraries do this in a way that follows the native conventions of the respective programming language. So a Python library will feel natural to Python developers, and a JavaScript library will feel natural to JavaScript developers.

### Available Client Libraries

Currently, the XRP Ledger supports official or community-maintained client libraries for these languages:

| Language | Package Name |
|----------|--------------|
| JavaScript/TypeScript | `xrpl` |
| Python | `xrpl-py` |
| Java | `xrpl4j` |
| C++ | rippled headers |
| PHP | `xrpl_php` |
| Ruby | `xrbp` |

In this course, we're using the JavaScript SDK (`xrpl`), but the concepts you learn will transfer to any of these languages.

By using one of these libraries, you can focus more on building your application and less on the intricacies of directly interacting with the raw XRP Ledger API.

---

## Congratulations!

That was a long and heavy section, but you've now learned some essential concepts that will serve as the foundation for everything else in this course:

- **Infrastructure**: The distributed network of nodes running rippled
- **Consensus**: How the network agrees on the state of the ledger
- **Ledgers**: The "blocks" of the XRP Ledger and their three states
- **Accounts**: Your identity on the ledger
- **Reserves**: How spam is prevented through economic costs
- **Transactions**: The only way to modify the ledger
- **Fees**: The three types and how they protect the network
- **XRP's Dual Role**: Security and value exchange
- **Amendments**: How the network evolves democratically
- **Client Libraries**: Tools that make development easier

Take a moment to review any sections that weren't completely clear. These concepts will come up again and again as you progress through your XRP Ledger development journey.
