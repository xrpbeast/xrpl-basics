# Xaman OAuth2 PKCE Flow

In this lesson, we'll build a secure sign-in flow using Xaman's OAuth2 PKCE protocol. This provides standards-based authentication with full backend control.

---

## Comparing Authentication Options

| Option | Description | Use Case |
|--------|-------------|----------|
| **Option 1** | Frontend SDK only | Simple apps, no sensitive data |
| **Option 4** | OAuth2 PKCE with backend | Secure apps, user accounts, permissions |

### Option 1 Limitations
- Tokens exposed to browser
- No backend session control
- No protection for sensitive data

### When to Use Option 4
- Managing user accounts
- Handling private data
- Enforcing permissions
- Server-side session control

---

## OAuth2 vs Options 2 & 3

The key difference is that OAuth2 is a **standards-based flow** compatible with many identity providers. Options 2 and 3 rely on custom payload signing or webhooks specific to the Xaman ecosystem.

### Additional Benefits of OAuth2

With Xaman's access token, your backend can:
- Access Xaman API endpoints on behalf of the user
- Retrieve user profiles
- Create/manage sign requests tied to user accounts
- Store per-user app data on Xaman infrastructure

However, for most workflows, you'll still issue your own JWT and manage your own database.

---

## What We'll Build

### Frontend Responsibilities
1. Generate PKCE code verifier and code challenge
2. Redirect to Xaman's OAuth2 authorization page
3. Handle callback with authorization code
4. Send code and verifier to backend

### Backend Responsibilities
1. Exchange code + verifier for access token
2. Verify token authenticity using JWKS
3. Decode ID token for user info
4. Issue and manage own JWT sessions
5. Protect sensitive token data

---

## Frontend Implementation

### Step 1: Clean Setup

```jsx
import { useState, useEffect } from 'react';
import axios from 'axios';

const XAMAN_AUTH_URL = import.meta.env.VITE_XAMAN_AUTH_URL;
const API_KEY = import.meta.env.VITE_XAMAN_API_KEY;
const REDIRECT_URI = import.meta.env.VITE_REDIRECT_URI;

function App() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);
  const [accessToken, setAccessToken] = useState(null);
  const [stateInfo, setStateInfo] = useState(null);

  const handleSignIn = async () => {
    // Implementation below
  };

  const handleSignOut = () => {
    setUser(null);
    setAccessToken(null);
  };

  return (
    <div>
      <h1>Xaman OAuth2 PKCE Integration</h1>
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {user ? (
        <div>
          <p>Signed in as: {user.account}</p>
          {stateInfo && <p>{stateInfo}</p>}
          <button onClick={handleSignOut}>Sign Out</button>
        </div>
      ) : (
        <button onClick={handleSignIn}>Sign In</button>
      )}
    </div>
  );
}
```

### Step 2: Environment Variables

Create `frontend/.env`:

```bash
VITE_XAMAN_AUTH_URL=https://oauth2.xaman.app/auth
VITE_XAMAN_API_KEY=your-api-key
VITE_REDIRECT_URI=http://localhost:3000
```

### Step 3: Install PKCE Package

```bash
npm install pkce-challenge
```

### Step 4: Sign-In Handler

```jsx
import pkceChallenge from 'pkce-challenge';

const handleSignIn = async () => {
  setError(null);

  try {
    // Generate PKCE challenge
    const { code_verifier, code_challenge } = pkceChallenge();

    // Store code verifier securely (never send to OAuth provider!)
    sessionStorage.setItem('code_verifier', code_verifier);

    // Generate state for CSRF protection
    const randomUuid = crypto.randomUUID();
    const currentTime = new Date().toISOString();

    const stateObject = { randomUuid, currentTime };
    const state = btoa(JSON.stringify(stateObject))
      .replace(/\+/g, '-')
      .replace(/\//g, '_');

    // Store random UUID for validation
    sessionStorage.setItem('randomUuid', randomUuid);

    // Build authorization URL
    const params = new URLSearchParams({
      client_id: API_KEY,
      redirect_uri: REDIRECT_URI,
      response_type: 'code',
      scope: 'openid',
      code_challenge_method: 'S256',
      code_challenge: code_challenge,
      state: state
    });

    // Redirect to Xaman
    window.location.href = `${XAMAN_AUTH_URL}?${params.toString()}`;
  } catch (err) {
    setError('Failed to initiate sign-in');
  }
};
```

### Step 5: Handle Callback

```jsx
useEffect(() => {
  async function handleCallback() {
    const url = new URL(window.location.href);
    const returnedCode = url.searchParams.get('code');
    const returnedState = url.searchParams.get('state');
    const returnedError = url.searchParams.get('error');

    // Handle OAuth error
    if (returnedError) {
      setError(`OAuth error: ${returnedError}`);
      return;
    }

    // Validate state
    if (returnedState) {
      try {
        // Decode state
        const decodedState = JSON.parse(
          atob(returnedState.replace(/-/g, '+').replace(/_/g, '/'))
        );

        // Validate structure
        if (!decodedState?.randomUuid || !decodedState?.currentTime) {
          setError('Invalid state structure');
          return;
        }

        // Compare with stored UUID
        const expectedUuid = sessionStorage.getItem('randomUuid');
        if (decodedState.randomUuid !== expectedUuid) {
          throw new Error('State mismatch - possible CSRF attack');
        }

        // Display time info (demo purposes)
        setStateInfo(`State returned successfully. Login started at ${decodedState.currentTime}`);
      } catch (err) {
        setError('Failed to decode or validate state - possible tampering');
        return;
      }
    }

    // Exchange code for token
    if (returnedCode) {
      const codeVerifier = sessionStorage.getItem('code_verifier');

      if (!codeVerifier) {
        setError('Code verifier not found');
        return;
      }

      try {
        const result = await axios.post('/api/exchange', {
          code: returnedCode,
          code_verifier: codeVerifier,
          redirect_uri: REDIRECT_URI
        });

        setAccessToken(result.data.accessToken);

        // Clean up session storage
        sessionStorage.removeItem('code_verifier');
        sessionStorage.removeItem('randomUuid');
      } catch (err) {
        setError('Failed to exchange code for token');
      }
    }

    // Clean URL (remove code and state from address bar)
    if (window.location.search) {
      window.history.replaceState({}, document.title, window.location.pathname);
    }
  }

  handleCallback();
}, []);
```

### Step 6: Fetch User Data

```jsx
useEffect(() => {
  async function fetchUser() {
    if (!accessToken) return;

    try {
      const result = await axios.get('/api/me', {
        headers: {
          Authorization: `Bearer ${accessToken}`
        }
      });
      setUser(result.data);
    } catch (err) {
      setError('Failed to fetch user data');
    }
  }

  fetchUser();
}, [accessToken]);
```

---

## Backend Implementation

### Step 1: Clean Setup

```javascript
import express from 'express';
import cors from 'cors';
import axios from 'axios';
import jwt from 'jsonwebtoken';
import dotenv from 'dotenv';
import { createBackendJWT, verifyBackendJWT } from './utils.js';
import { verifyJWT } from './verify.js';

dotenv.config();

const app = express();
app.use(cors({ origin: 'http://localhost:3000' }));
app.use(express.json());

const TOKEN_URL = process.env.XAMAN_TOKEN_URL;
const API_KEY = process.env.XAMAN_API_KEY;
const API_SECRET = process.env.XAMAN_API_SECRET;

// In-memory user store (use database in production)
const users = {};

const PORT = 3001;
app.listen(PORT, () => console.log(`Backend on ${PORT}`));
```

### Step 2: Environment Variables

Create `backend/.env`:

```bash
XAMAN_TOKEN_URL=https://oauth2.xaman.app/token
XAMAN_API_KEY=your-api-key
XAMAN_API_SECRET=your-api-secret
JWT_PRIVATE_KEY=your-jwt-secret
```

### Step 3: Token Exchange Endpoint

```javascript
app.post('/api/exchange', async (req, res) => {
  try {
    const { code, code_verifier, redirect_uri } = req.body;

    // Validate input
    if (!code || !code_verifier || !redirect_uri) {
      return res.status(400).json({ error: 'Missing required fields' });
    }

    // Build form data for token request
    const params = new URLSearchParams();
    params.append('grant_type', 'authorization_code');
    params.append('code', code);
    params.append('code_verifier', code_verifier);
    params.append('redirect_uri', redirect_uri);
    params.append('client_id', API_KEY);
    params.append('client_secret', API_SECRET);

    // Exchange code for tokens
    const result = await axios.post(TOKEN_URL, params.toString(), {
      headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
      }
    });

    const { access_token: _accessToken, id_token: _idToken } = result.data;

    // Verify tokens (best practice even from trusted provider)
    try {
      await verifyJWT(_accessToken, API_KEY);
      await verifyJWT(_idToken, API_KEY);
    } catch (verifyError) {
      return res.status(500).json({ error: 'Token verification failed' });
    }

    // Decode ID token for user info
    const decodedUser = jwt.decode(_idToken);

    // Create user object
    const user = {
      account: decodedUser.sub, // r-address
      name: 'User Name', // From your database
      xamanAccessToken: _accessToken,
      xamanIdToken: _idToken
    };

    // Generate our own JWT
    const accessToken = createBackendJWT(
      { account: user.account, iat: Date.now() },
      '24h'
    );

    // Store user (keyed by our token)
    users[accessToken] = user;

    // Return only our token (never expose Xaman tokens)
    res.status(200).json({ accessToken });
  } catch (error) {
    console.error('Exchange error:', error);
    res.status(500).json({ error: 'Failed to exchange code' });
  }
});
```

### Step 4: Protected Me Endpoint

```javascript
app.get('/api/me', (req, res) => {
  const auth = req.headers.authorization;

  if (!auth || !auth.startsWith('Bearer ')) {
    return res.status(401).json({ error: 'No token provided' });
  }

  try {
    const token = auth.split(' ')[1];

    // Verify our JWT
    const verified = verifyBackendJWT(token);
    if (!verified) {
      return res.status(401).json({ error: 'Invalid token' });
    }

    // Find user
    const user = users[token];
    if (!user) {
      return res.status(404).json({ error: 'User not found' });
    }

    // Return user data (without sensitive tokens)
    res.json({
      account: user.account,
      name: user.name
    });
  } catch (error) {
    res.status(401).json({ error: 'Authentication failed' });
  }
});
```

### Step 5: JWT Verification Module

Create `backend/verify.js`:

```javascript
import jwt from 'jsonwebtoken';
import jwksRsa from 'jwks-rsa';

const jwksClient = jwksRsa({
  jwksUri: 'https://oauth2.xaman.app/.well-known/jwks.json',
  cache: true,
  rateLimit: true
});

function getKey(header, callback) {
  jwksClient.getSigningKey(header.kid, (err, key) => {
    if (err) {
      callback(err);
    } else {
      const signingKey = key.publicKey || key.rsaPublicKey;
      callback(null, signingKey);
    }
  });
}

export function verifyJWT(token, audience) {
  return new Promise((resolve, reject) => {
    jwt.verify(token, getKey, {
      audience: audience,
      algorithms: ['RS256']
    }, (err, decoded) => {
      if (err) {
        reject(err);
      } else {
        resolve(decoded);
      }
    });
  });
}
```

Install dependencies:

```bash
npm install jsonwebtoken jwks-rsa
```

---

## Understanding the Response

When you exchange the code, Xaman returns:

| Field | Description |
|-------|-------------|
| `access_token` | JWT for Xaman API calls |
| `id_token` | OpenID Connect ID token with user details |
| `expires_in` | Token lifetime in seconds |
| `refresh_token` | Placeholder (Xaman doesn't issue these) |
| `scope` | Granted scopes (openid) |
| `token_type` | Bearer |

The `sub` claim in the ID token contains the user's r-address.

---

## Why Verify Tokens?

Even tokens from trusted providers should be verified:

- Protects against token forgery
- Guards against replay attacks
- Catches misconfigurations
- Ensures only valid, untampered tokens are accepted

---

## Security Features

| Feature | Purpose |
|---------|---------|
| **PKCE** | Prevents authorization code interception |
| **State parameter** | Protects against CSRF attacks |
| **Code verifier in sessionStorage** | Kept private, never sent to OAuth provider |
| **Backend token exchange** | Secrets never exposed to frontend |
| **JWT verification** | Validates token authenticity |
| **Own JWT issuance** | Backend controls sessions |

---

## Summary

### Frontend Flow
1. Generate PKCE challenge and state
2. Redirect to Xaman OAuth2
3. Handle callback, validate state
4. Send code + verifier to backend
5. Use returned token for API calls

### Backend Flow
1. Exchange code for Xaman tokens
2. Verify tokens with JWKS
3. Decode ID token for user info
4. Issue own JWT
5. Protect endpoints with token validation

### Key Takeaways

1. **OAuth2 PKCE** is a standards-based secure flow
2. **Code verifier** stays in sessionStorage, never sent to OAuth provider
3. **State parameter** prevents CSRF attacks
4. **Backend exchanges code** for tokens (secrets stay server-side)
5. **Verify tokens** even from trusted providers
6. **Issue your own JWT** for session management
7. **Never expose Xaman tokens** to frontend

---

## What's Next

In the next lesson, we'll explore using Xaman as an OpenID identity provider.
