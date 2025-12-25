# Xaman Webhook Authentication

In this lesson, we'll build a more advanced and secure authentication flow using webhooks and JWT. This approach gives your backend full control over the authentication process.

---

## Why Webhooks?

In the previous lesson, the frontend handled the signing flow and told the backend which user signed in. This works for basic authentication, but it isn't secure enough for:

- Managing user profiles
- Private data access
- Any feature requiring true session control

**Why?** Anyone who intercepts the success message could potentially impersonate a signed-in user.

### When Previous Method Is Fine

The previous method (Option 2) is appropriate when:
- Users must sign every critical action (like payments)
- You're only using sign-in to get an address for generating another payload

### When You Need Webhooks

Use this webhook approach when:
- Users can update data without signing each time
- You need persistent sessions
- You want full backend control over authentication

---

## The Secure Flow

Here's the pattern we'll build:

### 1. User Initiates Sign-In
- Frontend asks backend to start signing

### 2. Backend Creates Session
- Generates unique session ID linked to payload UUID
- Stores session in pending state
- **Web:** Sets secure HTTP-only cookie containing session ID
- **Mobile:** Returns session ID for secure storage (e.g., iOS Keychain)

### 3. Backend Creates Xaman Payload
- Frontend displays QR code or deep link
- UUID is embedded in the QR/deep link
- Session ID is never shown to user

### 4. User Signs with Wallet
- Xaman notifies backend via webhook
- Backend marks session as signed in
- Associates XRPL address with session

### 5. Frontend Gets Notified
- WebSocket notifies frontend of completed signing
- Frontend requests access token

### 6. Backend Issues JWT
- Verifies session is marked as signed in
- Issues access token (and optional refresh token)
- Destroys session (single-use)

### 7. Normal Auth Flow Begins
- Client uses access token for all API calls

---

## Why This Is Secure

| Option 2 | Option 3 (Webhook) |
|----------|-------------------|
| Frontend tells backend who signed in | Backend controls entire handshake |
| No guarantee it's the correct client | Only original client can complete signing |
| Vulnerable to interception | No token = no access |

Even if someone intercepts the QR code or payload, they can't log in without:
- **Web:** The HTTP-only cookie from the original browser
- **Mobile:** The session token from the app's secure storage

---

## Web vs Native Apps

### Web (Browser)
- Uses HTTP-only secure cookies
- Cookie binds session to the browser that started login
- Backend only issues JWT if correct cookie is sent

### Native Apps (iOS/Android)
- No cookies available
- Store session ID securely (iOS Keychain, Android Keystore)
- Present session token to redeem login

---

## Building the Implementation

We'll fork the previous project and add webhook support.

### Project Setup

```bash
cp -r xaman-signing-two xaman-signing-three
cd xaman-signing-three
code .
```

---

## Backend Changes

### Step 1: Session Store

Create an in-memory session store (use Redis in production):

```javascript
// Session store shape:
// {
//   [payloadUuid]: {
//     sessionId: string,
//     expiry: Date,
//     signedIn: boolean,
//     account?: string
//   }
// }
const sessions = {};

// User store shape:
// {
//   [rAddress]: {
//     userToken: string,
//     lastLogin: Date,
//     sessionId: string,
//     payloadUuid: string
//   }
// }
const users = {};
```

### Step 2: Generate Session IDs

```javascript
import crypto from 'crypto';

function generateSessionId() {
  return crypto.randomBytes(32).toString('hex');
}
```

### Step 3: Cookie Options

```javascript
function cookieOptions() {
  return {
    httpOnly: true,
    maxAge: 10 * 60 * 1000, // 10 minutes
    sameSite: 'lax',
    secure: false // Set to true in production (HTTPS required)
  };
}
```

### Step 4: Create Payload Endpoints

**For Web Apps:**

```javascript
app.get('/api/create-web-sign-payload', async (req, res) => {
  try {
    const signInTx = { TransactionType: 'SignIn' };
    const payload = await sdk.payload.create(signInTx);

    // Generate session
    const sessionId = generateSessionId();
    const expiry = new Date(Date.now() + 10 * 60 * 1000); // 10 minutes

    // Store session
    sessions[payload.uuid] = {
      sessionId,
      expiry,
      signedIn: false
    };

    // Set secure cookie
    res.cookie('session', sessionId, cookieOptions());

    res.json({
      uuid: payload.uuid,
      qr: payload.refs.qr_png,
      deeplink: payload.next.always,
      websocket: payload.refs.websocket_status
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to create payload' });
  }
});
```

**For Native Apps:**

```javascript
app.get('/api/create-app-sign-payload', async (req, res) => {
  try {
    const signInTx = { TransactionType: 'SignIn' };
    const payload = await sdk.payload.create(signInTx);

    const sessionId = generateSessionId();
    const expiry = new Date(Date.now() + 10 * 60 * 1000);

    sessions[payload.uuid] = {
      sessionId,
      expiry,
      signedIn: false
    };

    // Return session ID for app to store securely
    res.json({
      uuid: payload.uuid,
      qr: payload.refs.qr_png,
      deeplink: payload.next.always,
      websocket: payload.refs.websocket_status,
      sessionId // App stores this in Keychain
    });
  } catch (error) {
    res.status(500).json({ error: 'Failed to create payload' });
  }
});
```

### Step 5: Webhook Endpoint

```javascript
import express from 'express';

app.use(express.json());

app.post('/api/xaman-webhook', async (req, res) => {
  const body = req.body;
  const uuid = body?.payloadResponse?.payload_uuidv4;

  if (!uuid) {
    return res.status(400).json({ error: 'Invalid payload' });
  }

  // Get full payload data
  const data = await sdk.payload.get(uuid);
  if (!data) {
    return res.status(400).json({ error: 'Payload not found' });
  }

  // Route based on transaction type
  const type = data.payload.request_json.TransactionType;

  switch (type) {
    case 'SignIn':
      await signInHandler(uuid, data);
      break;
    case 'Payment':
      // Handle payments...
      break;
    default:
      return res.status(400).json({ error: 'Unknown transaction type' });
  }

  res.status(200).json({ success: true });
});
```

### Step 6: Sign-In Handler

```javascript
async function signInHandler(uuid, data) {
  const session = sessions[uuid];

  // Check session exists and not expired
  if (!session || new Date() > session.expiry) {
    return;
  }

  const account = data.response.account;
  const userToken = data.application.issued_user_token;

  // Store/update user
  users[account] = {
    userToken,
    lastLogin: new Date(),
    sessionId: session.sessionId,
    payloadUuid: uuid
  };

  // Mark session as signed in
  session.signedIn = true;
  session.account = account;
}
```

### Step 7: Sign-In Verification Endpoint

```javascript
import cookieParser from 'cookie-parser';

app.use(cookieParser());

app.get('/api/sign-in/:uuid', async (req, res) => {
  const { uuid } = req.params;
  const sessionId = req.cookies.session;
  // For apps: const sessionId = req.headers.authorization?.replace('Bearer ', '');

  // 1. Get session
  const session = sessions[uuid];
  if (!session) {
    return res.status(400).json({ error: 'Session not found' });
  }

  // 2. Validate session ID matches
  if (session.sessionId !== sessionId) {
    return res.status(403).json({ error: 'Invalid session' });
  }

  // 3. Check expiry
  if (new Date() > session.expiry) {
    delete sessions[uuid];
    return res.status(403).json({ error: 'Session expired' });
  }

  // 4. Check signed in
  if (!session.signedIn) {
    return res.status(403).json({ error: 'Not signed in' });
  }

  // 5. Get account
  const account = session.account;

  // 6. Create JWT
  const accessToken = createBackendJWT(
    { account, iat: Date.now() },
    '24h'
  );

  // 7. Delete session (single-use)
  delete sessions[uuid];

  // 8. Return token
  res.json({
    accessToken,
    expiresIn: 24 * 60 * 60 * 1000,
    account
  });
});
```

### Step 8: JWT Utilities

Create `backend/utils.js`:

```javascript
import jwt from 'jsonwebtoken';

const PRIVATE_KEY = process.env.JWT_PRIVATE_KEY;

export function createBackendJWT(payload, expiresIn = '1h') {
  return jwt.sign(payload, PRIVATE_KEY, {
    algorithm: 'HS256',
    expiresIn
  });
}

export function verifyBackendJWT(token) {
  try {
    return jwt.verify(token, PRIVATE_KEY);
  } catch {
    return null;
  }
}
```

Add to `backend/.env`:

```bash
JWT_PRIVATE_KEY=your-secret-key-here
```

---

## Frontend Changes

### Update Endpoint Call

```javascript
const { data } = await axios.get('/api/create-web-sign-payload');
```

### Add Credentials to Sign-In Request

```javascript
const handleSigningSuccess = async (uuid, ws) => {
  try {
    const { data } = await axios.get(`/api/sign-in/${uuid}`, {
      withCredentials: true // Sends HTTP-only cookie
    });

    setUser(data.account);
    setStatus('Successfully signed in!');
  } catch (err) {
    setError('Failed to get user info');
  } finally {
    ws.close();
    setSigningIn(false);
  }
};
```

### Add Delay for Webhook Processing

```javascript
// In WebSocket message handler
if (d.signed === true) {
  setTimeout(async () => {
    await handleSigningSuccess(data.uuid, ws);
  }, 2000); // Wait for webhook to process
}
```

---

## Webhook Configuration

### Development Setup

Since localhost isn't reachable from Xaman's servers, use [Webhook.site](https://webhook.site):

1. Go to the Xaman Developer Console
2. Navigate to Settings
3. Click the webhook.site link provided
4. Copy the unique URL generated
5. Paste it into the Webhook URL field
6. Save

### Testing with Webhook.site

1. Start your app and click Sign In
2. Scan QR and sign in with Xaman
3. Check webhook.site for the callback
4. Copy the raw JSON body
5. Use a REST client to POST it to your local `/api/xaman-webhook`

---

## Complete Backend Code

```javascript
import { XummSdk } from 'xumm-sdk';
import express from 'express';
import cors from 'cors';
import cookieParser from 'cookie-parser';
import crypto from 'crypto';
import dotenv from 'dotenv';
import { createBackendJWT } from './utils.js';

dotenv.config();

const app = express();
const sdk = new XummSdk(
  process.env.XAMAN_API_KEY,
  process.env.XAMAN_API_SECRET
);

// Stores
const sessions = {};
const users = {};

// Middleware
app.use(cors({ origin: 'http://localhost:3000', credentials: true }));
app.use(express.json());
app.use(cookieParser());

// Helpers
function generateSessionId() {
  return crypto.randomBytes(32).toString('hex');
}

function cookieOptions() {
  return {
    httpOnly: true,
    maxAge: 10 * 60 * 1000,
    sameSite: 'lax',
    secure: false
  };
}

// Endpoints
app.get('/api/create-web-sign-payload', async (req, res) => {
  // ... implementation above
});

app.post('/api/xaman-webhook', async (req, res) => {
  // ... implementation above
});

app.get('/api/sign-in/:uuid', async (req, res) => {
  // ... implementation above
});

const PORT = 3001;
app.listen(PORT, () => console.log(`Backend on ${PORT}`));
```

---

## Key Security Features

| Feature | Purpose |
|---------|---------|
| **HTTP-only cookies** | Prevents JavaScript access to session |
| **Session binding** | Only original client can complete sign-in |
| **Single-use sessions** | Prevents replay attacks |
| **Time-limited sessions** | 10-minute expiry limits attack window |
| **Backend verification** | Webhook confirms actual signature |
| **JWT access tokens** | Standard secure API authentication |

---

## Summary

### What We Built

1. Backend-controlled authentication flow
2. Secure session management with cookies
3. Webhook handler for signature verification
4. JWT-based access tokens
5. Support for both web and native apps

### Key Takeaways

1. **Backend controls the flow** for true security
2. **Session binding** ensures only the original client can complete login
3. **Webhooks** let Xaman notify your backend of signatures
4. **JWT access tokens** enable secure API calls without re-signing
5. **Single-use sessions** prevent replay attacks
6. **Platform flexibility** works for web and mobile
7. **Full UI control** unlike OAuth approaches

---

## What's Next

We have a working implementation, but there's one important question: **How can we be sure the webhook request actually came from Xaman?**

In the next lesson, we'll add HMAC verification to prove webhook authenticity.
