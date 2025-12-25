# Payload Signing

In this lesson, we move beyond sign-in and start working with real XRPL transactions through Xaman. This is where things get powerful.

---

## SignIn vs Payload Signing

| SignIn | Payload Signing |
|--------|-----------------|
| Not an XRPL feature | Real XRPL transactions |
| Just proves identity | Affects ledger state |
| Off-chain only | Payments, trust lines, NFTs |

When we move into payload signing, we're talking about transactions that actually hit the ledger.

---

## What Is a Payload?

A payload is a JSON request sent to Xaman containing:
- Transaction type
- Transaction fields to be signed

Xaman presents this to the user, they approve it, and the transaction is signed and submitted to the XRP Ledger.

---

## The Payload Lifecycle

```
1. Create the payload (backend)
        ↓
2. User signs and submits (Xaman)
        ↓
3. Webhook notification (backend)
        ↓
4. Verify transaction (XRPL)
        ↓
5. Confirm to user (frontend)
```

---

## Security Is Critical

With real transactions, stakes are higher:

- **Never trust the frontend alone**
- **Validate payloads on backend**
- **Treat every response as untrusted until verified**
- **Use webhooks for production integrations**

---

## Building a Payment Flow

Let's build a complete XRP payment signing transaction.

### The Flow

1. User clicks "Pay" button
2. Frontend requests payment payload from backend
3. Backend creates payload and returns QR/deeplink
4. User scans QR and signs in Xaman
5. Xaman sends webhook to backend
6. Backend verifies payment on XRPL
7. WebSocket notifies frontend
8. Frontend requests confirmation
9. Backend returns success/failure

---

## Frontend Implementation

### State Setup

```jsx
const [paymentInProgress, setPaymentInProgress] = useState(false);
const [paymentSuccess, setPaymentSuccess] = useState(false);
```

### UI Changes

```jsx
{user && (
  <div>
    <p>Signed in as: {user.account}</p>
    <button onClick={handleSignOut}>Sign Out</button>
    <br />

    {paymentSuccess ? (
      <h3 style={{ color: 'green' }}>Payment Received!</h3>
    ) : (
      <div>
        <p>Pay your subscription</p>
        <button onClick={handlePayment}>Pay 0.0001 XRP</button>
      </div>
    )}

    {paymentInProgress && qr && (
      <div>
        <img src={qr} alt="Scan to pay" style={{ marginTop: 30 }} />
        <a href={deeplink} style={{ marginTop: 20 }}>
          Open in Xaman
        </a>
        <p>{status}</p>
      </div>
    )}
  </div>
)}
```

### Payment Handler

```jsx
const handlePayment = async () => {
  try {
    setQr(null);
    setDeeplink(null);
    setStatus(null);

    // Request payment payload from backend
    const { data } = await axios.post('/api/payment', null, {
      headers: {
        Authorization: `Bearer ${user.accessToken}`
      }
    });

    setQr(data.qr);
    setDeeplink(data.deeplink);
    setStatus('Scan the QR in Xaman to make payment');
    setPaymentInProgress(true);

    // Set up WebSocket listener
    const ws = new WebSocket(data.websocket);
    wsRef.current = ws;

    ws.onmessage = (event) => {
      const d = JSON.parse(event.data);

      if (d.opened) {
        setStatus('Waiting for payment approval...');
      }

      if (d.signed === true) {
        handlePaymentSuccess(data.uuid, ws);
      }

      if (d.signed === false) {
        ws.close();
        setStatus('Payment declined');
        setPaymentInProgress(false);
      }
    };

    ws.onclose = () => {
      setPaymentInProgress(false);
    };
  } catch (err) {
    setError('Payment failed');
    setPaymentInProgress(false);
  }
};
```

### Payment Confirmation

```jsx
const handlePaymentSuccess = async (uuid, ws) => {
  try {
    const { data } = await axios.get(`/api/payment-confirmation/${uuid}`, {
      headers: {
        Authorization: `Bearer ${user.accessToken}`
      }
    });

    if (data) {
      setPaymentInProgress(false);
      setPaymentSuccess(true);
    }
  } catch (err) {
    setError('Payment verification failed');
  } finally {
    ws.close();
  }
};
```

---

## Backend Implementation

### Setup

```javascript
import { Client } from 'xrpl';

// Payment store
const payments = {};

// Constants
const DESTINATION = 'rYourAppAddress...';
const AMOUNT = '100'; // drops (0.0001 XRP)
```

### Payment Endpoint

```javascript
app.post('/api/payment', async (req, res) => {
  try {
    // 1. Verify user
    const auth = req.headers.authorization;
    const token = auth?.split(' ')[1];
    const isValid = verifyBackendJWT(token);

    if (!isValid) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    // 2. Build payment transaction
    const txJson = {
      TransactionType: 'Payment',
      Destination: DESTINATION,
      Amount: AMOUNT
    };

    // 3. Create payload with Xaman SDK
    const payload = await sdk.payload.create(txJson);

    // 4. Return to frontend
    res.json({
      uuid: payload.uuid,
      qr: payload.refs.qr_png,
      deeplink: payload.next.always,
      websocket: payload.refs.websocket_status
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to create payment' });
  }
});
```

### Webhook Handler Update

```javascript
app.post('/api/xaman-webhook', async (req, res) => {
  // ... signature verification ...

  const uuid = req.body?.payloadResponse?.payload_uuidv4;
  const data = await sdk.payload.get(uuid);
  const type = data.payload.request_json.TransactionType;

  switch (type) {
    case 'SignIn':
      await signInHandler(uuid, data);
      break;
    case 'Payment':
      await paymentHandler(uuid);
      break;
    default:
      return res.status(400).json({ error: 'Unknown type' });
  }

  res.status(200).json({ success: true });
});
```

### Payment Handler

```javascript
async function paymentHandler(uuid) {
  const client = new Client('wss://xrplcluster.com');

  try {
    // 1. Get authoritative payload data
    const data = await sdk.payload.get(uuid);
    const txid = data.response.txid;

    // 2. Connect to XRPL
    await client.connect();

    // 3. Fetch transaction from ledger
    const { result } = await client.request({
      command: 'tx',
      transaction: txid
    });

    // 4. Verify transaction is validated
    if (!result.validated) {
      throw new Error('Transaction not validated');
    }

    // 5. Verify transaction succeeded
    if (result.meta.TransactionResult !== 'tesSUCCESS') {
      throw new Error('Transaction failed');
    }

    // 6. Verify transaction type
    if (result.TransactionType !== 'Payment') {
      throw new Error('Not a payment transaction');
    }

    // 7. Verify amount
    const deliveredAmount = result.meta.delivered_amount;
    if (deliveredAmount !== AMOUNT) {
      throw new Error('Incorrect amount');
    }

    // 8. Verify sender is known user
    const account = result.Account;
    const user = users[account];
    if (!user) {
      throw new Error('Unknown sender');
    }

    // 9. Record payment
    payments[uuid] = { account };

  } catch (error) {
    console.error('Payment verification failed:', error.message);
    // Don't record payment - will show as failed
  } finally {
    await client.disconnect();
  }
}
```

### Confirmation Endpoint

```javascript
app.get('/api/payment-confirmation/:uuid', (req, res) => {
  try {
    const { uuid } = req.params;
    const isPaid = !!payments[uuid];
    res.status(200).json(isPaid);
  } catch (error) {
    res.status(404).json({ error: 'Unknown payload' });
  }
});
```

---

## Why Verify on XRPL?

Never blindly trust webhook data. By fetching from the ledger:

1. **Guaranteed authentic** data from XRPL
2. **Verify validation** status
3. **Check transaction result** (tesSUCCESS)
4. **Confirm amount** delivered
5. **Map sender** to known user

---

## Other Transaction Types

Once you know one, you know them all. Just swap the transaction JSON.

### Trust Line (TrustSet)

```javascript
const txJson = {
  TransactionType: 'TrustSet',
  LimitAmount: {
    currency: 'USD',
    issuer: 'rIssuerAddress...',
    value: '1000000'
  }
};
```

### NFT Mint (NFTokenMint)

```javascript
const txJson = {
  TransactionType: 'NFTokenMint',
  NFTokenTaxon: 0,
  Flags: 8, // tfTransferable
  URI: '68747470733A2F2F...' // Hex-encoded URI
};
```

### Webhook Handler Extension

```javascript
switch (type) {
  case 'SignIn':
    await signInHandler(uuid, data);
    break;
  case 'Payment':
    await paymentHandler(uuid);
    break;
  case 'TrustSet':
    await trustSetHandler(uuid);
    break;
  case 'NFTokenMint':
    await nftMintHandler(uuid);
    break;
  // Add more as needed
}
```

---

## The Universal Pattern

| Step | Same for All |
|------|--------------|
| Create payload | Yes (just different JSON) |
| Return QR/deeplink | Yes |
| User signs in Xaman | Yes |
| Webhook received | Yes |
| Verify on XRPL | Yes (different checks) |
| Confirm to user | Yes |

**The only things that change:**
1. Transaction JSON
2. Webhook handler logic
3. UI specifics

---

## Summary

| Component | Responsibility |
|-----------|----------------|
| **Frontend** | Display QR, handle WebSocket, confirm |
| **Backend** | Create payload, verify on XRPL, record |
| **Webhook** | Route by transaction type, trigger handlers |
| **XRPL** | Source of truth for verification |

### Key Takeaways

1. **Payload signing** is for real XRPL transactions
2. **Same flow** for all transaction types
3. **Backend creates** payment JSON with destination/amount
4. **Webhook receives** notification of signing
5. **Always verify** on XRPL, never trust webhook alone
6. **Check everything**: validated, result, type, amount, sender
7. **Once you know one**, you know them all

---

## What's Next

We'll explore features that enhance user experience: push notifications, app storage, and building polished, user-friendly XRPL applications.
