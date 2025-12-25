# Account Generation

In the previous lecture, you learned that an r-address is 25 to 35 alphanumeric characters in length, case-sensitive, excludes the number zero, the uppercase O and I, and the lowercase l, and always starts with an 'r'. The r-address is the public address that represents the account on the XRP Ledger.

But as we've discussed, account creation is **not** performed by the XRP Ledger itself. In most traditional applications, you would call a function with some data and be returned an account. With the XRP Ledger, this is not the case.

---

## Two Parts to Generating an Account

### Part 1: Generate the Account Secret

This is a strictly mathematical process and can be performed **completely offline**. You don't need to connect to any network. Once you have the secret (also called the seed), you can derive the r-address from it.

### Part 2: Fund the Account

Send XRP to the newly created account's r-address using a payment transaction. When the XRP Ledger processes the payment, it attempts to assign the payment to the destination account. But in the case of a new account, it doesn't exist yet - so the XRP Ledger creates a new account object on the ledger and assigns the payment to its balance.

For the account to become active, it must receive and maintain a balance greater than the account base reserve (currently **2 XRP**).

---

## Using the Testnet Faucet

Before we can create accounts programmatically, we need some XRP to activate them. For development purposes, we can use the [XRP Testnet Faucet](https://xrpl.org/xrp-testnet-faucet.html) provided by xrpl.org.

The faucet will:
1. Generate an account mathematically
2. Fund it with 10,000 test XRP
3. Return the address and secret

These XRP are on the testnet, so they have no real value - but they're perfect for development and learning.

**Important Security Note**: If you ever create an account on the mainnet, you must immediately store the secret securely. Never share it, and never store it in plain text in a production environment.

---

## Generating Accounts with Code

### Setup

```bash
mkdir account-generation && cd account-generation
npm init -y
npm install xrpl
```

### The Simple Way: Wallet.generate()

The JavaScript SDK makes account generation incredibly easy:

```javascript
import { Wallet } from "xrpl";

// Generate a new wallet
const wallet = Wallet.generate();

console.log(wallet);
```

Output:
```javascript
{
  publicKey: 'ED...',           // Public key for verification
  privateKey: 'ED...',          // Private key (keep secret!)
  classicAddress: 'rN7n34...',  // The r-address
  seed: 'sEdV...'               // The seed (also keep secret!)
}
```

That's it! One line of code. The SDK has abstracted all the cryptographic complexity away.

### Understanding the Output

| Field | Description |
|-------|-------------|
| `publicKey` | Used to verify signatures. Can be shared. |
| `privateKey` | Used to create signatures. **Keep secret!** |
| `classicAddress` | The r-address - your public identifier on the ledger |
| `seed` | A compact representation of the private key. **Keep secret!** |

**Note**: You'll see "classic address" and "r-address" used interchangeably. This naming comes from when X-addresses were introduced - the original format became known as the "classic" address.

### Deriving an Address from a Seed

If you have a seed and need to get the address, use `Wallet.fromSeed()`:

```javascript
import { Wallet } from "xrpl";

// Generate a new wallet
const wallet = Wallet.generate();
console.log("Generated wallet:", wallet.classicAddress);

// Later, derive the same wallet from its seed
const derivedWallet = Wallet.fromSeed(wallet.seed);
console.log("Derived address:", derivedWallet.classicAddress);

// Both addresses will be identical!
```

This is useful when you've stored a seed and need to reconstruct the wallet object to sign transactions.

---

## Complete Example

```javascript
import { Wallet } from "xrpl";

// Function to generate a new wallet
const generateWallet = () => {
  const wallet = Wallet.generate();
  return wallet;
};

// Function to derive address from seed
const getAddressFromSeed = (seed) => {
  const wallet = Wallet.fromSeed(seed);
  return wallet.classicAddress;
};

// Generate a new wallet
const newWallet = generateWallet();
console.log("New Wallet:");
console.log("  Address:", newWallet.classicAddress);
console.log("  Seed:", newWallet.seed);

// Derive the address from the seed (should match)
const derivedAddress = getAddressFromSeed(newWallet.seed);
console.log("\nDerived from seed:", derivedAddress);
```

Run it:
```bash
node generate.js
```

---

## Checking Account Status

After generating a wallet, you can check its status on a block explorer:

- **Testnet**: https://testnet.xrpl.org
- **Mainnet**: https://xrpl.org

Search for your r-address. A newly generated (unfunded) account will show:
- Status: **Unactivated**
- Balance: **0 XRP**

The account won't appear as "active" until it receives at least the base reserve amount of XRP.

---

## What's Happening Under the Hood?

If you're curious about the cryptography, you can explore the [xrpl.js source code](https://js.xrpl.org/classes/Wallet.html#generate). The generation process:

1. Generates cryptographically secure random bytes
2. Creates an Ed25519 or secp256k1 key pair
3. Derives the r-address from the public key using Base58Check encoding

But even understanding all of this, you'll still use `Wallet.generate()` - there's no reason to reinvent the wheel!

---

## Next Steps

We've generated a wallet, but it's unactivated (zero balance). In the next lecture, we'll:
1. Fund our new wallet using XRP from our faucet account
2. Verify the activation on the testnet explorer

---

## Key Takeaways

- Account generation is a **two-step process**: generate keys, then fund
- Key generation is **purely mathematical** and can be done offline
- The XRP Ledger creates the account when it receives the first payment
- Use `Wallet.generate()` to create new wallets
- Use `Wallet.fromSeed(seed)` to reconstruct a wallet from a seed
- **Always store seeds securely** - there is no recovery if you lose them
- Testnet faucet provides free test XRP for development

---

## Resources

- [Wallet.generate() Documentation](https://js.xrpl.org/classes/Wallet.html#generate)
- [Wallet.fromSeed() Documentation](https://js.xrpl.org/classes/Wallet.html#fromSeed)
- [XRP Testnet Faucet](https://xrpl.org/xrp-testnet-faucet.html)
- [Testnet Explorer](https://testnet.xrpl.org)
