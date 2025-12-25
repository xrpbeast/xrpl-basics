# Xaman Custom Sign-In Integration

In this lesson, we'll build a custom sign-in integration with Xaman that gives you full control over the user experience. Unlike the SDK popup approach, this method uses a backend and WebSocket for real-time updates.

---

## Important Security Note

Before we build this, understand what this flow provides:

**This approach verifies that the user controls a particular XRPL account at the moment of signing. It does NOT create an ongoing authenticated session.**

### What This Flow Is Good For
- Wallet connection and signing
- Proving wallet ownership for one-time checks
- Actions that require a wallet signature

### What This Flow Is NOT For
- General website login or session management
- Updating user profiles
- Changing settings
- Authorizing actions that don't require a wallet signature

### Best Practice

For secure, persistent authentication:
1. Use your own web authentication system (JWT login)
2. Link the user's web account to their XRPL account after verifying ownership
3. Or use OAuth 2.0/OpenID flow which provides a verifiable JWT

---

## Project Setup: Monorepo Approach

We'll create a monorepo with both frontend and backend.

### Step 1: Initialize the Project

```bash
mkdir xaman-signing-two
cd xaman-signing-two
git init
echo "node_modules" > .gitignore
npm init -y
npm install concurrently
```

### Step 2: Create Frontend

```bash
npm create vite@latest frontend -- --template react
```

### Step 3: Create Backend

```bash
mkdir backend
cd backend
npm init -y
npm install -D nodemon dotenv
touch app.js
cd ..
```

### Step 4: Configure Workspaces

Update the root `package.json`:

```json
{
  "name": "xaman-signing-two",
  "workspaces": ["frontend", "backend"],
  "scripts": {
    "dev": "concurrently \"npm run dev:frontend\" \"npm run dev:backend\"",
    "dev:frontend": "npm run dev --workspace=frontend",
    "dev:backend": "npm run dev --workspace=backend"
  }
}
```

Add dev script to `backend/package.json`:

```json
{
  "type": "module",
  "scripts": {
    "dev": "nodemon app.js"
  }
}
```

---

## Building the Backend

### Step 1: Install Dependencies

```bash
cd backend
npm install xumm express cors
cd ..
```

### Step 2: Basic Express Setup

Create `backend/app.js`:

```javascript
import { XummSdk } from 'xumm-sdk';
import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';

dotenv.config();

const app = express();

// Configure CORS for frontend on port 3000
app.use(cors({
  origin: 'http://localhost:3000'
}));

// Health check endpoint
app.get('/api/health', (req, res) => {
  res.json({ status: 'ok' });
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Backend running on port ${PORT}`);
});
```

### Step 3: Initialize the SDK

```javascript
const API_KEY = process.env.XAMAN_API_KEY;
const API_SECRET = process.env.XAMAN_API_SECRET;

const sdk = new XummSdk(API_KEY, API_SECRET);
```

### Step 4: Create Sign-In Payload Endpoint

```javascript
app.get('/api/create-sign-payload', async (req, res) => {
  try {
    const signInTx = {
      TransactionType: 'SignIn'
    };

    const payload = await sdk.payload.create(signInTx);

    // Return only what the frontend needs
    res.json({
      uuid: payload.uuid,
      qr: payload.refs.qr_png,
      deeplink: payload.next.always,
      websocket: payload.refs.websocket_status
    });
  } catch (error) {
    console.error('Error creating payload:', error);
    res.status(500).json({ error: 'Failed to create sign-in payload' });
  }
});
```

### Step 5: Get User Endpoint

```javascript
app.get('/api/get-user/:uuid', async (req, res) => {
  try {
    const { uuid } = req.params;
    const payload = await sdk.payload.get(uuid);

    if (!payload) {
      throw new Error('Payload not found');
    }

    res.json({
      account: payload.response.account
    });
  } catch (error) {
    console.error('Error getting user:', error);
    res.status(500).json({ error: 'Failed to get user' });
  }
});
```

### Environment Files

Create `backend/.env`:

```bash
XAMAN_API_KEY=your-api-key
XAMAN_API_SECRET=your-api-secret
```

Create `frontend/.env`:

```bash
VITE_XAMAN_API_KEY=your-api-key
```

> **Important:** The backend needs both keys. The frontend only needs the public key (if at all for this implementation).

---

## Building the Frontend

### Step 1: Configure Vite

Update `frontend/vite.config.js`:

```javascript
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000,
    proxy: {
      '/api': {
        target: 'http://localhost:3001',
        changeOrigin: true
      }
    }
  }
});
```

The proxy allows us to use relative API URLs in frontend code.

### Step 2: Install Axios

```bash
cd frontend
npm install axios
cd ..
```

### Step 3: Create the Component

Create `frontend/src/CustomSignIn.jsx`:

```jsx
import { useState, useEffect, useRef } from 'react';
import axios from 'axios';

export default function CustomSignIn() {
  // User and error state
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  // Sign-in flow state
  const [signingIn, setSigningIn] = useState(false);
  const [qr, setQr] = useState(null);
  const [deeplink, setDeeplink] = useState(null);
  const [status, setStatus] = useState('');
  const [expires, setExpires] = useState('');

  // WebSocket ref for lifecycle management
  const wsRef = useRef(null);

  // Cleanup WebSocket on unmount
  useEffect(() => {
    return () => {
      if (wsRef.current) {
        wsRef.current.close();
      }
    };
  }, []);

  const handleSignIn = async () => {
    // Guard against multiple calls
    if (signingIn) return;

    // Reset state
    setSigningIn(true);
    setUser(null);
    setError(null);
    setQr(null);
    setDeeplink(null);
    setStatus('');
    setExpires('');

    try {
      // Get payload from backend
      const { data } = await axios.get('/api/create-sign-payload');

      setQr(data.qr);
      setDeeplink(data.deeplink);
      setStatus('Waiting for user to scan QR code...');

      // Close existing WebSocket if any
      if (wsRef.current) {
        wsRef.current.close();
      }

      // Create WebSocket connection
      const ws = new WebSocket(data.websocket);
      wsRef.current = ws;

      ws.onclose = () => {
        if (wsRef.current === ws) {
          wsRef.current = null;
        }
        setSigningIn(false);
      };

      ws.onmessage = (event) => {
        const d = JSON.parse(event.data);

        // Handle expiration countdown
        if (d.expires_in_seconds) {
          const seconds = d.expires_in_seconds === 86400
            ? 86399
            : d.expires_in_seconds;
          const t = new Date(seconds * 1000)
            .toISOString()
            .slice(11, 19);
          setExpires(`Expires in: ${t}`);
        }

        // Handle QR scanned / app opened
        if (d.opened) {
          setStatus('Waiting for you to approve the sign-in request...');
        }

        // Handle successful sign-in
        if (d.signed === true) {
          handleSigningSuccess(data.uuid, ws);
        }

        // Handle declined sign-in
        if (d.signed === false) {
          ws.close();
          setQr(null);
          setDeeplink(null);
          setStatus('You declined the signing request. Wallet connection failed.');
          setSigningIn(false);
        }
      };
    } catch (err) {
      setError('Error during sign-in');
      setSigningIn(false);
    }
  };

  const handleSigningSuccess = async (uuid, ws) => {
    try {
      const { data } = await axios.get(`/api/get-user/${uuid}`);
      setUser(data.account);
      setStatus('Successfully signed in!');
    } catch (err) {
      setError('Failed to get user info');
    } finally {
      ws.close();
      setSigningIn(false);
    }
  };

  const handleSignOut = () => {
    if (wsRef.current) {
      wsRef.current.close();
    }
    setUser(null);
    setQr(null);
    setDeeplink(null);
    setStatus('');
    setExpires('');
    setSigningIn(false);
  };

  return (
    <div>
      {error && <p style={{ color: 'red' }}>{error}</p>}

      {user ? (
        <div>
          <p>Signed in as: {user}</p>
          <button onClick={handleSignOut}>Sign Out</button>
        </div>
      ) : (
        <div>
          <p>Please click the sign-in button</p>
          <button onClick={handleSignIn} disabled={signingIn}>
            {signingIn ? 'Signing In...' : 'Sign In'}
          </button>

          {qr && (
            <div style={{ marginTop: 30 }}>
              <img src={qr} alt="Scan with Xaman" />
            </div>
          )}

          {deeplink && (
            <div style={{ marginTop: 20 }}>
              <a href={deeplink} target="_blank" rel="noopener noreferrer">
                Open in Xaman
              </a>
            </div>
          )}

          {status && (
            <div style={{ marginTop: 50, fontSize: '1.2em' }}>
              {status}
            </div>
          )}

          {expires && (
            <div style={{ marginTop: 50 }}>
              {expires}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
```

### Step 4: Update App.jsx

```jsx
import CustomSignIn from './CustomSignIn';

function App() {
  return (
    <div>
      <h1>Xaman Sign-In Integration (Custom UI)</h1>
      <CustomSignIn />
    </div>
  );
}

export default App;
```

---

## How It Works

### The Flow

1. User clicks "Sign In"
2. Frontend calls backend `/api/create-sign-payload`
3. Backend creates a `SignIn` payload with Xaman SDK
4. Backend returns: UUID, QR code URL, deeplink, WebSocket URL
5. Frontend displays QR code and connects to WebSocket
6. User scans QR with Xaman wallet
7. WebSocket sends `opened` event, UI updates
8. User approves in wallet
9. WebSocket sends `signed: true` event
10. Frontend calls backend `/api/get-user/:uuid`
11. Backend fetches user account from payload
12. Frontend displays user's r-address

### WebSocket Events

| Event | Description |
|-------|-------------|
| `expires_in_seconds` | Countdown until payload expires |
| `opened` | User scanned QR and opened Xaman |
| `signed: true` | User approved the sign-in |
| `signed: false` | User declined the sign-in |

---

## Why Use a Backend?

While the frontend could theoretically use the SDK directly, best practices dictate:

1. **API Secret stays on backend** (never expose in frontend)
2. **Additional business logic** can be added (logging, session management)
3. **More secure** validation of the signing response
4. **Flexibility** for custom authentication flows

---

## React WebSocket Considerations

React and WebSockets require careful lifecycle management:

1. **Use a ref** to hold the WebSocket instance
2. **Cleanup in useEffect** to close WebSocket on unmount
3. **Check for existing WebSocket** before creating new one
4. **Null the ref** when WebSocket closes

This prevents memory leaks and race conditions.

---

## The Expiration Time Challenge

The backend returns `expires_in_seconds` as 86400 (24 hours). There's a quirk when converting this:

```javascript
// 86400 seconds = exactly 24:00:00
// But we want to display 23:59:59 initially
const seconds = d.expires_in_seconds === 86400
  ? 86399
  : d.expires_in_seconds;
```

This prevents displaying "24:00:00" which would look incorrect.

---

## Summary

| Component | Responsibility |
|-----------|----------------|
| **Backend** | Creates payloads, fetches user, holds API secret |
| **Frontend** | Displays UI, manages WebSocket, handles state |
| **WebSocket** | Real-time updates on signing progress |
| **Xaman SDK** | Server-side payload creation and verification |

### Key Takeaways

1. **Custom UI** gives you full control over user experience
2. **Backend required** for secure API secret handling
3. **WebSocket** provides real-time feedback
4. **SignIn transaction type** is used for authentication
5. **Payload UUID** links the entire flow together
6. **React refs** help manage WebSocket lifecycle
7. **This is NOT a session** - just proof of wallet ownership

---

## What's Next

You now have a fully functional custom Xaman integration with a backend, giving you total control over the user experience. In the next lessons, we'll explore more advanced signing scenarios beyond simple authentication.
