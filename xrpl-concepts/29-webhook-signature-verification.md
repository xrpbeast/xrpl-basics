# Webhook Signature Verification

In this lesson, we'll add an important security measure to our webhook endpoint: **HMAC signature verification**. This proves that callbacks genuinely came from Xaman and haven't been tampered with.

---

## Why Verify Webhooks?

Without verification, anyone could send fake webhooks to your endpoint, potentially:
- Impersonating signed-in users
- Triggering unauthorized actions
- Corrupting your application state

HMAC verification ensures only Xaman can send valid webhooks to your backend.

---

## How It Works

Xaman signs every webhook with an HMAC:

1. Xaman computes: `HMAC(timestamp + body, your_api_secret)`
2. Sends the signature in a request header
3. Your backend recomputes the HMAC using the same formula
4. If values match, the webhook is authentic

**This works because only you and Xaman know your API secret.**

---

## Implementation

### Step 1: Extract Headers

Xaman sends four custom headers with each webhook:

| Header | Description |
|--------|-------------|
| `x-xaman-request-signature` | HMAC signature |
| `x-xaman-request-timestamp` | Unix timestamp |
| `x-xaman-payload-uuid` | Payload UUID (also in body) |
| `x-xaman-attempt-number` | Delivery attempt count |

We only need the signature and timestamp for verification.

```javascript
app.post('/api/xaman-webhook', async (req, res) => {
  // Extract signature and timestamp from headers
  const signature = req.headers['x-xaman-request-signature'];
  const timestamp = req.headers['x-xaman-request-timestamp'];

  // Validate headers exist
  if (!signature || !timestamp) {
    return res.status(400).json({ error: 'Missing signature headers' });
  }

  // Verify the webhook
  const isValid = verifyWebhook(
    JSON.stringify(req.body),
    signature,
    timestamp
  );

  if (!isValid) {
    return res.status(401).json({ error: 'Invalid webhook signature' });
  }

  // Continue with trusted webhook...
  const uuid = req.body?.payloadResponse?.payload_uuidv4;
  // ... rest of handler
});
```

### Step 2: Create Verification Function

```javascript
import crypto from 'crypto';

const API_SECRET = process.env.XAMAN_API_SECRET;

function verifyWebhook(bodyString, signature, timestamp) {
  // Create HMAC using SHA-1 algorithm
  // Note: Remove dashes from secret (they're just formatting)
  const hmac = crypto.createHmac('sha1', API_SECRET.replace(/-/g, ''));

  // Feed data: timestamp concatenated directly with body
  // No separator, no whitespace - just timestamp + JSON
  hmac.update(timestamp + bodyString);

  // Get hex digest (Xaman uses lowercase hex)
  const computed = hmac.digest('hex');

  // Compare computed value with received signature
  return computed === signature;
}
```

---

## Key Details

### Secret Formatting

Xaman formats the API secret with dashes (like a UUID) for readability:

```
xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
```

**Remove the dashes before using as HMAC key:**

```javascript
API_SECRET.replace(/-/g, '')
```

### Concatenation Format

The data fed into the HMAC is:

```
timestamp + bodyString
```

No separator, no whitespace. For example:

```
1703520000{"payloadResponse":{"payload_uuidv4":"..."}}
```

If your body string doesn't match exactly, the HMAC won't match.

### Digest Format

Request the digest as lowercase hexadecimal:

```javascript
hmac.digest('hex')
```

Xaman provides the signature as a lowercase hex string.

---

## Testing

### Valid Webhook

When signature matches:
1. `verifyWebhook()` returns `true`
2. Webhook processing continues normally

### Invalid Webhook

To simulate a fake webhook, change one character in the signature header:
- `verifyWebhook()` returns `false`
- Endpoint returns 401 Unauthorized
- Webhook is rejected

---

## Complete Webhook Endpoint

```javascript
import crypto from 'crypto';
import express from 'express';

const API_SECRET = process.env.XAMAN_API_SECRET;

function verifyWebhook(bodyString, signature, timestamp) {
  const hmac = crypto.createHmac('sha1', API_SECRET.replace(/-/g, ''));
  hmac.update(timestamp + bodyString);
  const computed = hmac.digest('hex');
  return computed === signature;
}

app.post('/api/xaman-webhook', async (req, res) => {
  // 1. Extract headers
  const signature = req.headers['x-xaman-request-signature'];
  const timestamp = req.headers['x-xaman-request-timestamp'];

  if (!signature || !timestamp) {
    return res.status(400).json({ error: 'Missing signature headers' });
  }

  // 2. Verify signature
  const isValid = verifyWebhook(
    JSON.stringify(req.body),
    signature,
    timestamp
  );

  if (!isValid) {
    console.warn('Invalid webhook signature detected');
    return res.status(401).json({ error: 'Invalid signature' });
  }

  // 3. Process trusted webhook
  const uuid = req.body?.payloadResponse?.payload_uuidv4;
  if (!uuid) {
    return res.status(400).json({ error: 'Invalid payload' });
  }

  // ... rest of your webhook handling logic

  res.status(200).json({ success: true });
});
```

---

## Security Considerations

### Keep Your Secret Private

The entire security model depends on your API secret remaining confidential:
- Never expose in frontend code
- Never commit to version control
- Use environment variables
- Rotate if compromised

### Timing Attacks

For production, consider using `crypto.timingSafeEqual()` instead of simple equality:

```javascript
function verifyWebhook(bodyString, signature, timestamp) {
  const hmac = crypto.createHmac('sha1', API_SECRET.replace(/-/g, ''));
  hmac.update(timestamp + bodyString);
  const computed = hmac.digest('hex');

  // Timing-safe comparison
  try {
    return crypto.timingSafeEqual(
      Buffer.from(computed, 'hex'),
      Buffer.from(signature, 'hex')
    );
  } catch {
    return false;
  }
}
```

### Timestamp Validation

Optionally, reject webhooks with old timestamps to prevent replay attacks:

```javascript
const MAX_AGE_SECONDS = 300; // 5 minutes

function isTimestampValid(timestamp) {
  const now = Math.floor(Date.now() / 1000);
  const webhookTime = parseInt(timestamp, 10);
  return Math.abs(now - webhookTime) < MAX_AGE_SECONDS;
}
```

---

## Summary

| Step | Action |
|------|--------|
| 1 | Extract signature and timestamp from headers |
| 2 | Remove dashes from API secret |
| 3 | Compute HMAC: `sha1(timestamp + body, secret)` |
| 4 | Compare computed value with received signature |
| 5 | Reject if mismatch, process if valid |

### Key Takeaways

1. **HMAC verification** proves webhooks came from Xaman
2. **Only you and Xaman** know the API secret
3. **Remove dashes** from secret before use
4. **Concatenate** timestamp directly with body (no separator)
5. **Use hex digest** for comparison
6. **Reject invalid webhooks** with 401 status
7. **Keep secret private** or security is compromised

---

## Resources

- [Xaman Webhook Signature Verification](https://docs.xaman.dev/concepts/payloads-sign-requests/status-updates/webhooks/signature-verification)

---

## What's Next

With webhook verification in place, your authentication system is now fully secure. In the next lessons, we'll explore additional Xaman features and transaction signing.
