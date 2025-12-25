# Xaman Production Best Practices

This lesson covers essential practices for production-ready Xaman integrations: status updates, rate limits, data storage, developer mode, and the integration checklist.

---

## Status Updates

When you create a payload, you need to know when it's signed, rejected, or expired. There are three methods:

### Webhooks (Recommended)

Register a webhook URL in the Developer Console. Xaman sends POST requests when status changes.

| Pros | Cons |
|------|------|
| No open connections to maintain | Requires reachable backend endpoint |
| Scales well | Single point of failure |
| Secure and reliable when verified | |

### WebSockets (Good for Frontends)

Subscribe to payload updates via SDK. Get live updates directly.

| Pros | Cons |
|------|------|
| Real-time feedback | Must keep connection open |
| Great for interactive UIs | Ties up resources |
| | Less suitable for backends |

### Polling (Avoid)

Repeatedly call API to check status.

| Pros | Cons |
|------|------|
| Easy to implement | Inefficient, wastes API calls |
| | Adds unnecessary delay |
| | **Actively discouraged by Xaman** |

### Recommendation

- **Production:** Webhooks
- **Frontend UX:** WebSockets + webhooks
- **Never:** Polling

---

## Rate Limits and Scaling

Understanding rate limits is critical for production. Exceeding them may throttle or block your requests.

### Key Points

- Limits are **averages**
- Can change **dynamically**
- **Higher limits** granted if you avoid polling and use webhooks/WebSockets

### Scaling Patterns

| Pattern | Description |
|---------|-------------|
| **Prefer webhooks** | Notify only on status change |
| **WebSocket subscriptions** | For real-time UIs, close when done |
| **Batching and queuing** | Smooth out spikes, prevent bursts |
| **Retry with backoff** | Respect headers, exponential backoff |
| **Stateless backends** | Store UUIDs in database/cache |
| **Monitoring alerts** | Track rate limit remaining |

### Best Practice

Avoid polling. Rely on webhooks. Use WebSockets only where needed (frontend).

---

## Submit Options

When creating a payload, you have two choices:

### Auto-Submit (Default)

Xaman signs AND submits the transaction to XRPL.

```javascript
// Default behavior, no options needed
const payload = await sdk.payload.create({
  TransactionType: 'Payment',
  Destination: 'rDest...',
  Amount: '1000000'
});
```

### Self-Submit

Xaman returns the signed blob for you to submit.

```javascript
const payload = await sdk.payload.create(
  {
    TransactionType: 'Payment',
    Destination: 'rDest...',
    Amount: '1000000'
  },
  {
    options: {
      submit: false // Return signed blob instead
    }
  }
);
```

The webhook includes the signed blob in the `hex` property.

### Submitting the Blob

```javascript
import { Client } from 'xrpl';

const client = new Client('wss://xrplcluster.com');
await client.connect();

const result = await client.submit(signedBlob);
```

### Comparison

| Auto-Submit | Self-Submit |
|-------------|-------------|
| Simplest UX | Full control over broadcast |
| Fewer moving parts | Custom node selection |
| Less control over node | Works with multi-sig flows |
| | More complex (you handle submission) |

### Use Cases for Self-Submit

- Multi-signature flows
- Custom node routing
- Policy checks before broadcast
- Consistent observability across all tx types

---

## Data Storage

Xaman provides two storage options for lightweight state.

### Backend Store

App-wide storage, single JSON blob per app.

| Property | Description |
|----------|-------------|
| Scope | Per app, shared across all users |
| Access | Requires API key and secret |
| Best for | Global config, feature flags, defaults |

```javascript
const sdk = new Xumm(apiKey, apiSecret);

// Set data
await sdk.backendStore.set({
  theme: 'dark',
  version: '1.0.0'
});

// Get data
const data = await sdk.backendStore.get();

// Delete all
await sdk.backendStore.delete();
```

**Note:** This is a single slot, not key-value. To add fields, get current values, append, and resave.

### User Store

Per-user key-value storage, tied to user token.

| Property | Description |
|----------|-------------|
| Scope | Per user |
| Access | Requires user token |
| Best for | User preferences, feature flags, small state |

```javascript
// Set value for user
await sdk.userStore.set(userToken, 'theme', 'dark');

// Get value
const theme = await sdk.userStore.get(userToken, 'theme');

// Delete key
await sdk.userStore.delete(userToken, 'theme');

// List all keys for user
const all = await sdk.userStore.list(userToken);
```

### Comparison

| Backend Store | User Store |
|---------------|------------|
| App-wide | Per user |
| Single JSON blob | Key-value pairs |
| Global configs | User preferences |
| Managed from backend | Requires user token |

**Important:** These are not database replacements. Use for lightweight state only.

---

## Developer Mode

Test safely without risking real funds or cluttering mainnet.

### Why Use Dev Mode?

- **Safety:** Build and QA without mainnet funds
- **Early features:** Devnet gets new amendments first
- **Realistic testing:** End-to-end flows on testnet
- **Team parity:** Force or detect networks from your app

### Setup Steps

1. Open Xaman
2. Go to **Settings > Advanced**
3. Enable **Developer Mode**
4. Go home, tap network switch (top right)
5. Choose **XRPL Testnet**
6. Tap **Activate your account** for faucet funds

### Force Network in Payloads

```javascript
const payload = await sdk.payload.create(
  { TransactionType: 'Payment', ... },
  {
    options: {
      force_network: 'TESTNET'
    }
  }
);
```

### Verify Network in Results

```javascript
const result = await sdk.payload.get(uuid);
const network = result.response.network;

if (network !== 'MAINNET') {
  throw new Error('Transaction not on mainnet');
}
```

### Testnet vs Devnet

| Network | Use For |
|---------|---------|
| **Testnet** | Stable testing, production simulation |
| **Devnet** | Latest features, but subject to resets |

---

## Integration Checklist

Must-do practices for production-ready integrations.

### Webhook Handling

- [ ] **Verify signatures** on incoming webhooks
- [ ] **Process server-side** as source of truth
- [ ] **Idempotency**: Design handlers for safe re-runs

### Payload Lifecycle

- [ ] **Track full lifecycle**, never trust frontend alone
- [ ] **Confirm resolution** against Xaman API
- [ ] **Use custom meta identifiers** for internal records

### Return URLs

- [ ] **Configure where appropriate** (essential for mobile/native)
- [ ] **Treat as fresh entry**, rebuild state from backend

### Rate Limits

- [ ] **Respect limits**, don't poll
- [ ] **Prefer webhooks** or WebSockets
- [ ] **Queue spikes**, use backoff retries

### Development

- [ ] **Enable developer mode**
- [ ] **Test on testnet/devnet** before going live
- [ ] **Force network** in payloads
- [ ] **Verify network** in results

### Data Storage

- [ ] **Backend store** for app-wide config
- [ ] **User store** for per-user preferences
- [ ] **Don't use as database**, lightweight state only

---

## Documentation Reference

The [Xaman Documentation](https://docs.xaman.dev/) is excellent:

- Detailed and well-structured
- Covers far more than any course can
- Kept up to date
- Examples in multiple languages
- Definitive guide for edge cases

**Bookmark it. Refer to it often.**

---

## Summary

| Topic | Key Points |
|-------|------------|
| **Status Updates** | Webhooks > WebSockets > Polling |
| **Rate Limits** | Avoid polling, use backoff, queue spikes |
| **Submit Options** | Auto (default) vs Self (multi-sig, custom) |
| **Backend Store** | App-wide JSON blob |
| **User Store** | Per-user key-value pairs |
| **Developer Mode** | Testnet for safe development |
| **Checklist** | Security, correctness, reliability |

### Key Takeaways

1. **Webhooks are the gold standard** for status updates
2. **Never poll**, it's discouraged and inefficient
3. **Respect rate limits** with queues and backoff
4. **Self-submit** gives control for multi-sig and custom flows
5. **Storage is for small state**, not a database replacement
6. **Always test on testnet** before mainnet
7. **Force and verify networks** in your payloads
8. **Follow the checklist** for production readiness
9. **Xaman docs** are your definitive reference

---

## Resources

- [Status Updates](https://docs.xaman.dev/concepts/payloads-sign-requests/status-updates)
- [Rate Limits](https://docs.xaman.dev/concepts/limitations/rate-limits)
- [User Store](https://docs.xaman.dev/js-ts-sdk/sdk-syntax/xumm.userstore)
- [Backend Store](https://docs.xaman.dev/js-ts-sdk/sdk-syntax/xumm.backendstore)
- [Debugging / Dev Mode](https://docs.xaman.dev/environments/xapps-dapps/debugging)
- [Xaman Documentation](https://docs.xaman.dev/)

---

## What's Next

You now have a comprehensive foundation for building production-ready Xaman integrations. Continue exploring the documentation and building real applications on the XRP Ledger.
