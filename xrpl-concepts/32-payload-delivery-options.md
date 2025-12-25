# Payload Delivery Options

In this lesson, we explore the various ways to deliver sign requests to users and configure payloads for better UX and tracking.

---

## Delivery Methods Overview

| Method | Best For | Fallback Needed |
|--------|----------|-----------------|
| **QR Code** | Desktop to mobile | No |
| **Deep Link** | Mobile-first apps | No (has built-in fallback) |
| **Push Notification** | Seamless UX | Yes (QR/deeplink) |

---

## Deep Linking

### The Mobile Problem

If you're on a mobile device viewing a QR code on screen, how do you scan it with a camera on the same device?

**Deep links solve this.**

### How It Works

**On Desktop:**
- Opens a Xaman-hosted page showing QR code and instructions
- Perfect for desktop-to-mobile workflows

**On Mobile:**
- Shows "Open in Xaman" button
- User taps, app opens directly to the signing request
- Fallback if app isn't installed

### One Link Works Everywhere

```javascript
const payload = await sdk.payload.create(txJson);

// Deep link is already in the response
const deeplink = payload.next.always;
```

### UX Best Practice

Detect device type and adapt:

| Device | Primary | Secondary |
|--------|---------|-----------|
| Desktop | QR Code | Deep link (fallback) |
| Mobile | Deep link | QR Code (accordion/backup) |

---

## Push Notifications

Push notifications deliver sign requests **directly to the user's device**. This is one of Xaman's standout features.

### Benefits

- Smoother, faster UX
- Works across devices (trigger from desktop, sign on mobile)
- Especially powerful for mobile-first apps

### User Tokens

Push is powered by **user tokens**:

| Property | Description |
|----------|-------------|
| **Unique** | Per user, per app |
| **Scoped** | Only your app can use it |
| **Expires** | After ~30 days of inactivity |
| **Refreshed** | On new sign-in |

### Collecting the Token

When a user signs in, you receive a user token in the payload result or webhook:

```javascript
async function signInHandler(uuid, data) {
  const account = data.response.account;
  const userToken = data.application.issued_user_token;

  // Store securely, linked to user
  users[account] = {
    ...users[account],
    userToken
  };
}
```

### Using Push for Payments

Include the user token when creating payloads:

```javascript
app.post('/api/payment', async (req, res) => {
  // Get user token from your store
  const user = findUserByAccessToken(token);
  const userToken = user?.userToken || '';

  const payload = await sdk.payload.create({
    TransactionType: 'Payment',
    Destination: DESTINATION,
    Amount: AMOUNT
  }, {
    user_token: userToken // Enables push delivery
  });

  // ...
});
```

### Token Validation

Verify tokens before use:

```javascript
// Batch check
POST https://xaman.app/api/v1/platform/user-tokens

// Single check
GET https://xaman.app/api/v1/platform/user-token/{token}
```

### Best Practices

1. **Always verify** payloads on backend
2. **Verify tokens** before use
3. **Don't spam** pushes
4. **Always offer fallback** (QR or deep link)
5. **Assume push succeeded** but provide QR option if needed

### Permission Categories

| Type | Description |
|------|-------------|
| **Payload pushes** | Enabled automatically with valid user token |
| **Custom app pushes** | Require explicit permission |

Users control whether your app can push. Tokens expire after 30 days unless refreshed.

---

## App Origin Metadata

App origin lets you brand and contextualize payload requests.

### Default Behavior

Your app's name, description, and icon from the Developer Console apply to all payloads.

### Per-Payload Override

```javascript
const payload = await sdk.payload.create(txJson, {
  options: {
    origin: {
      type: 'YOUR_APP_NAME',
      data: {
        name: 'Different Brand',
        description: 'White label context',
        icon: 'https://example.com/icon.png'
      }
    }
  }
});
```

### Use Cases

- White-label solutions
- Multi-tenant apps
- Different contexts within your app
- Developer mode vs production

---

## Custom Meta Identifiers

Attach your own tracking identifiers to payloads.

### Why Use Custom IDs?

- Tie Xaman flows to internal records
- Map payloads to orders, sessions, users
- Don't rely solely on payload UUID

### Implementation

```javascript
const payload = await sdk.payload.create(txJson, {
  custom_meta: {
    identifier: 'order-12345',
    blob: JSON.stringify({ orderId: '12345', userId: 'user-789' })
  }
});
```

### Receiving in Webhook

The custom identifier comes back in the webhook payload:

```javascript
app.post('/api/xaman-webhook', async (req, res) => {
  const customId = req.body?.custom_meta?.identifier;
  // Use to look up your internal records
});
```

---

## Return URLs

Return URLs control where users go after signing.

### When Are They Needed?

| Flow Type | Return URL Value |
|-----------|------------------|
| Custom QR in your UI | Optional (websockets handle it) |
| Deep link / OAuth | Brings user back to your app |
| Native mobile apps | Essential for polished UX |

### Configuration

**Global:** Set in Developer Console

**Per-Payload:**

```javascript
const payload = await sdk.payload.create(txJson, {
  options: {
    return_url: {
      app: 'https://yourapp.com/callback?id={id}',
      web: 'https://yourapp.com/callback?id={id}'
    }
  }
});
```

### Replacement Variables

| Variable | Description |
|----------|-------------|
| `{id}` | Payload UUID |
| `{cid}` | Your custom identifier |
| `{txid}` | XRPL transaction hash (if submitted) |
| `{txblob}` | Signed blob (if submit=false) |

### Handling Different Outcomes

| Outcome | Available Variables |
|---------|---------------------|
| Approved & submitted | `{id}`, `{cid}`, `{txid}` |
| Approved, not submitted | `{id}`, `{cid}`, `{txblob}` |
| Rejected / Closed | `{id}`, `{cid}` |

### Mobile Considerations

iOS and Android don't guarantee returning to the same browser tab:

1. **Treat return URL as fresh entry**
2. **Rebuild state** using UUID or custom ID
3. **Confirm status via backend**
4. **Never trust URL params alone**

### Best Practices

```javascript
// Return page handler
app.get('/callback', async (req, res) => {
  const { id, cid, txid } = req.query;

  // Always verify with backend
  const status = await verifyPayloadStatus(id);

  // Show appropriate UI based on actual status
  res.render('callback', { status, txid });
});
```

### Value by Platform

| Platform | Return URL Value |
|----------|------------------|
| Desktop web | Low (popup stays on site) |
| Responsive web | Medium (tab issues on mobile) |
| Native apps | High (deep link to right screen) |

---

## Complete Payload Options

```javascript
const payload = await sdk.payload.create(
  {
    TransactionType: 'Payment',
    Destination: 'rDestination...',
    Amount: '1000000'
  },
  {
    // Push notification
    user_token: userToken,

    // Custom tracking
    custom_meta: {
      identifier: 'order-12345'
    },

    // Options
    options: {
      // Return URLs
      return_url: {
        app: 'https://app.com/done?id={id}',
        web: 'https://app.com/done?id={id}'
      },

      // App origin override
      origin: {
        type: 'CUSTOM',
        data: {
          name: 'Custom Name'
        }
      }
    }
  }
);
```

---

## Summary

| Feature | Purpose |
|---------|---------|
| **Deep Links** | Mobile-friendly delivery |
| **Push Notifications** | Seamless, direct delivery |
| **App Origin** | Branding per payload |
| **Custom Meta** | Internal tracking |
| **Return URLs** | Post-signing navigation |

### Key Takeaways

1. **One payload supports multiple delivery methods**
2. **Push requires user tokens** collected at sign-in
3. **Always provide fallbacks** for push (QR/deeplink)
4. **Tokens expire** after 30 days of inactivity
5. **Custom identifiers** help track internal state
6. **Return URLs** are essential for native apps
7. **Never trust URL params** as source of truth
8. **Confirm status via backend** always

---

## Resources

- [Deep Linking](https://docs.xaman.dev/concepts/payloads-sign-requests/delivery/deeplink)
- [Push Notifications](https://docs.xaman.dev/concepts/payloads-sign-requests/delivery/push)
- [Return URLs](https://docs.xaman.dev/concepts/payloads-sign-requests/payload-return-url)

---

## What's Next

With delivery methods covered, we'll explore more advanced Xaman features like xApps and building polished user experiences.
