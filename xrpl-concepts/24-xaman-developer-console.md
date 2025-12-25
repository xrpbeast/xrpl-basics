# Xaman Developer Console

The Developer Console is the central dashboard for developers building on the Xaman platform. It's where you register your app, manage API credentials, set up webhooks, monitor usage, and access essential settings for integrating Xaman into your XRPL applications.

Whether you're integrating single sign-on or building a full-featured xApp, the Developer Console is your gateway to everything you need to connect your project to the Xaman ecosystem.

---

## Why Do You Need a Developer Account?

To use Xaman's API or SDK for wallet signing, transaction signing, or xApp integrations, you must first register a developer account and then create an app inside the Developer Console.

### What a Developer Account Gives You

| Feature | Description |
|---------|-------------|
| **API Credentials** | Required to authenticate your app and access Xaman's features |
| **App Management** | Configure callback URLs, webhooks, branding, and security settings |
| **Monitoring** | Track API usage, payloads, and app analytics |
| **Security** | Manage secrets, rotate keys, and keep your integration secure |

**Without a developer account, you cannot create payloads, sign requests, or go live with any Xaman-powered feature.**

---

## Getting a Xaman Developer Account

Let's walk through the setup process.

### Step 1: Visit the Developer Portal

Go to [apps.xaman.dev](https://apps.xaman.dev)

Xaman uses the Xaman sign-in feature for authentication. What you're about to experience is pretty much what we'll build in the next section once we've got a developer account.

### Step 2: Sign In with Xaman

1. Get your Xaman wallet ready
2. Click "Sign in with Xaman"
3. Scan the QR code with your wallet (or tap the deep link on mobile)
4. Approve the signing request in your wallet app

> **Note:** If you don't have a Xaman wallet yet, pause here and set one up first. There are many guides available, including [this short setup walkthrough](https://www.youtube.com/watch?v=mOHxLYMW5pk).

### Step 3: Create Your First Application

If you've never had an account before, you'll be presented with a request to create a new application.

1. Click the link to create a new application
2. Give your application a name and description (you can update these later)
3. You should see a success screen

### Step 4: Back Up Your API Keys

You'll receive two keys:

| Key | Purpose | Where to Use |
|-----|---------|--------------|
| **API Key** | Public key | Frontend application |
| **API Secret** | Private key | Backend only |

**Important:** Once you click the "Open" button, the API Secret will never be shown again. You'll have to create a new key pair if you lose it. Back it up immediately!

### Pro Tip: Create a .env File

Store your keys safely in an environment file:

```bash
# .env
XAMAN_API_KEY=your-api-key-here
XAMAN_API_SECRET=your-api-secret-here
```

This will become useful in the next lectures.

---

## Exploring the Developer Console

Once you're in, let's take a look around the interface.

### Top Right: App Switcher

You can have multiple apps registered against one XRPL address and switch between them easily with the toggle. There's also a profile section where you can log out (make this a habit after each session).

### Left Menu: Main Navigation

| Section | Description |
|---------|-------------|
| **Settings** | Configure your app's properties |
| **Rev Share** | Revenue sharing options (beyond this module's scope) |
| **Logs** | Useful for debugging (will populate as you build) |
| **Payloads** | Track payload activity |
| **xApps** | Build mini-apps that run inside Xaman |
| **Permissions** | Whitelist r-addresses to manage the application (for teams) |

### About xApps

xApps are simple websites that can be launched from within the Xaman app. They allow developers to extend features or provide different experiences to the user base.

Think of it like the iOS App Store:
- **xApp** = the app
- **Xaman** = the iPhone

**Important:** If you want to build an xApp, you must first be approved. Unless you're planning to build an xApp, there's little value in activating this feature right away.

---

## Configuring Your Application Settings

Before we can start building, we need to configure a few settings.

### Required Settings

| Setting | Description | For Development |
|---------|-------------|-----------------|
| **Project Home Page** | Your project's website | Can use placeholder for now |
| **Help Link** | Where users can get help | Can use placeholder for now |
| **Email Address** | Contact email | Your email |
| **Origin/Redirect** | Where to redirect after signing | `http://localhost:3000` |

### Optional Settings (Complete Before Production)

- Terms of Service URL
- Privacy Policy URL

### Webhook

Leave blank for now. We'll use webhooks later in more advanced flows.

### Origin/Redirect URL

This is important and needs to be completed now. For development, set it to:

```
http://localhost:3000
```

We'll discuss this more in future lectures. Don't forget to click "Update Application" when done.

---

## Summary

The Xaman Developer Console is your mission control for Xaman app integrations.

### Quick Setup Checklist

1. Sign in with your Xaman wallet at [apps.xaman.dev](https://apps.xaman.dev)
2. Register your app with a name and description
3. Back up your API Key and API Secret immediately
4. Configure required settings (home page, help link, email)
5. Set origin/redirect to `http://localhost:3000` for development
6. Click "Update Application"

### Key Takeaways

1. **Developer account required** to use Xaman API/SDK
2. **Sign in with Xaman** to access the console
3. **API Key** is public (frontend), **API Secret** is private (backend)
4. **Back up your secret immediately** as it won't be shown again
5. **Multiple apps** can be registered under one XRPL address
6. **xApps** require approval before you can build them
7. **Origin/redirect URL** is needed for signing flows

---

## Resources

- [Xaman Developer Portal](https://apps.xaman.dev)
- [Xaman Developer Documentation](https://xaman.app/developers)
- [Xaman Wallet Setup Guide](https://www.youtube.com/watch?v=mOHxLYMW5pk)

---

## What's Next

You've now got everything you need to move on to the next phase: building our first signing application.
