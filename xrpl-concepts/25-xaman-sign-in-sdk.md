# Xaman Sign-In with SDK

In this lesson, we're going to build our first integration with Xaman: a simple native sign-in using the SDK. This is the easiest way to get started with Xaman authentication.

---

## Project Setup

Let's create a simple React application using Vite.

### Step 1: Create the Project

```bash
npm create vite@latest xaman-sign-in-one
# Select: React template

cd xaman-sign-in-one
git init
npm install
npm run dev
```

Verify it's running by loading the web page, then close it down and open VS Code.

### Step 2: Clean Up the Boilerplate

Remove unnecessary content from `App.jsx` and adjust the styling as needed. We want a clean starting point.

---

## Installing the SDK

Install the Xaman SDK:

```bash
npm install xumm
```

> **Note:** The package is still named `xumm` (the old name). This is a legacy thing that may or may not get updated.

If you prefer not to install a package, you can include the SDK script directly in your HTML for vanilla JavaScript workflows.

---

## Setting Up the SDK

Open `App.jsx` and clean it up:

```jsx
import { Xumm } from 'xumm';

const xumm = new Xumm(import.meta.env.VITE_XAMAN_API_KEY);

function App() {
  return (
    <div>
      <h1>Xaman Sign-In Integration</h1>
    </div>
  );
}

export default App;
```

### Environment Variables

Create a `.env` file with your API key from the previous lesson:

```bash
VITE_XAMAN_API_KEY=your-api-key-here
```

The SDK is now set up and ready to use.

---

## Building the UI

We need state to store the SDK response:

```jsx
import { useState } from 'react';
import { Xumm } from 'xumm';

const xumm = new Xumm(import.meta.env.VITE_XAMAN_API_KEY);

function App() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  return (
    <div>
      <h1>Xaman Sign-In Integration</h1>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {user ? (
        <div>
          <p>Signed in as: {user.account}</p>
          <button onClick={handleSignOut}>Sign Out</button>
        </div>
      ) : (
        <button onClick={handleSignIn}>Sign In with Xaman</button>
      )}
    </div>
  );
}
```

---

## Wiring Up the Handlers

### Sign In Handler

```jsx
const handleSignIn = async () => {
  // Clear previous state
  setUser(null);
  setError(null);

  try {
    const authResponse = await xumm.authorize();

    // Check for valid account
    if (authResponse?.me?.account) {
      setUser({ account: authResponse.me.account });
    } else {
      setError('Sign-in failed: No account returned');
    }
  } catch (err) {
    setError('Sign-in failed: ' + err.message);
  }
};
```

### Sign Out Handler

```jsx
const handleSignOut = async () => {
  await xumm.logout();
  setUser(null);
};
```

---

## Fixing the Port Issue

When you first try to sign in, you'll likely get an error. This is because of the origin URL we configured in the Developer Console.

Remember: we set the origin to `http://localhost:3000`, but Vite defaults to port 5173.

### Fix: Configure Vite to Use Port 3000

Edit `vite.config.js`:

```js
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 3000
  }
});
```

Restart the dev server. You should now see it running on port 3000.

> **Remember:** You'll need to update the origin URL in the Developer Console when you move to production.

---

## Testing the Sign-In Flow

1. Click "Sign In with Xaman"
2. The official Xaman login page appears (with your app name and logo)
3. Scan the QR code with your Xaman wallet
4. Swipe right to approve the sign-in request
5. The popup detects the signature via WebSocket and closes automatically
6. Your r-address is now displayed

Test sign-out by clicking the button. Your account info should be removed.

---

## Understanding What's Happening: PKCE Flow

When you call `xumm.authorize()`, the SDK handles the entire secure sign-in process using what's called a **PKCE flow** (Proof Key for Code Exchange). This is today's best practice for OAuth security.

### Two OAuth Flow Types

| Flow | How It Works | Security |
|------|--------------|----------|
| **Implicit** | Gets user info immediately in browser | Quick but less secure |
| **PKCE** | Gets temporary auth code, exchanges it securely | Much safer |

### The Magic of the SDK

Normally, PKCE requires a backend to exchange the authorization code for user info. But here's what makes the Xaman SDK special:

**Everything we did was in React (frontend), but we still got a fully verified user object.**

The SDK handles:
- Initiating the PKCE flow
- Exchanging the authorization code
- Verifying everything with the Xaman API
- Returning a verified user object

You get all the security benefits of PKCE without writing any backend code.

---

## Pros and Cons

### Advantages

| Advantage | Description |
|-----------|-------------|
| **Easy** | Just use `xumm.authorize()` |
| **Secure** | Uses PKCE flow by default |
| **No backend needed** | SDK handles everything |
| **Modern standard** | Recommended for all new apps |

> **Tip:** If you need implicit flow for some reason, pass `{ implicit: true }` to authorize.

### Use Case Example

Building a simple frontend that queries the XRPL to show user activity:

1. Use this integration to securely get the user's r-address
2. Use xrpl.js to fetch their account history
3. Display it with filters, analytics, or export features

### Limitations

| Limitation | Description |
|------------|-------------|
| **Non-customizable UI** | Must use the popup flow |
| **Popup blockers** | May interfere with the flow |
| **No redirect flow** | This SDK implementation doesn't support it |
| **No auth code access** | Can't implement custom OAuth if needed |

**Bottom line:** If you want simple and don't need a backend, let the SDK handle it. For more complex needs, you'll need a custom OAuth implementation.

---

## Persisting User State

If you refresh the page, your React state is gone. But click "Sign In" again and you're logged in instantly without re-authenticating.

Why? The SDK caches user data in local storage.

### Rehydrating State on Load

For a better UX, we can rehydrate React state when the app loads:

```jsx
import { useState, useEffect } from 'react';

function App() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    // Listen for SDK ready event
    xumm.on('ready', (userFromCache) => {
      if (userFromCache?.account) {
        setUser({ account: userFromCache.account });
      }
    });
  }, []); // Only run once on first load

  // ... rest of component
}
```

Now when you reload the browser, if the user's JWT is still valid (less than 24 hours old), their state persists automatically.

### What logout() Does

When you call `xumm.logout()`, it removes the cached state from local storage. After signing out and refreshing, you won't be recognized and will need to re-authenticate.

---

## Complete Code

```jsx
import { useState, useEffect } from 'react';
import { Xumm } from 'xumm';

const xumm = new Xumm(import.meta.env.VITE_XAMAN_API_KEY);

function App() {
  const [user, setUser] = useState(null);
  const [error, setError] = useState(null);

  useEffect(() => {
    xumm.on('ready', (userFromCache) => {
      if (userFromCache?.account) {
        setUser({ account: userFromCache.account });
      }
    });
  }, []);

  const handleSignIn = async () => {
    setUser(null);
    setError(null);

    try {
      const authResponse = await xumm.authorize();

      if (authResponse?.me?.account) {
        setUser({ account: authResponse.me.account });
      } else {
        setError('Sign-in failed: No account returned');
      }
    } catch (err) {
      setError('Sign-in failed: ' + err.message);
    }
  };

  const handleSignOut = async () => {
    await xumm.logout();
    setUser(null);
  };

  return (
    <div>
      <h1>Xaman Sign-In Integration</h1>

      {error && <p style={{ color: 'red' }}>{error}</p>}

      {user ? (
        <div>
          <p>Signed in as: {user.account}</p>
          <button onClick={handleSignOut}>Sign Out</button>
        </div>
      ) : (
        <button onClick={handleSignIn}>Sign In with Xaman</button>
      )}
    </div>
  );
}

export default App;
```

---

## Summary

| Step | Action |
|------|--------|
| 1 | Create React app with Vite |
| 2 | Install `xumm` package |
| 3 | Initialize SDK with API key |
| 4 | Call `xumm.authorize()` for sign-in |
| 5 | Call `xumm.logout()` for sign-out |
| 6 | Use `xumm.on('ready')` to persist state |

### Key Takeaways

1. **Install with** `npm install xumm` (legacy package name)
2. **Initialize** with your API key from environment variables
3. **Port must match** the origin URL in Developer Console
4. **PKCE flow** is used by default for security
5. **No backend required** for basic authentication
6. **State persists** in local storage (24-hour JWT validity)
7. **Use `on('ready')`** to rehydrate state on page load

---

## What's Next

In the next lesson, we'll look at the second type of integration, which gives us a custom user interface instead of the popup flow.
