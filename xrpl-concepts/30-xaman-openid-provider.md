# Xaman as OpenID Identity Provider

As we wrap up our exploration of Xaman integration options, this lesson covers a capability that is both technically impressive and, for most developers, an edge case: using Xaman as a standard OAuth2/OpenID Connect identity provider.

---

## What Does This Mean?

Xaman can act as a "Login with Xaman" button not just in your own apps, but in **any system that supports standard OAuth2 or OpenID Connect protocols**.

This includes enterprise single sign-on (SSO) environments like:
- Cloudflare Access
- Okta
- Auth0
- Azure AD
- Any OIDC-compliant platform

---

## How It Works

**It's configuration, not coding.**

Instead of writing custom authentication code, you configure your SSO provider to use Xaman as an identity provider:

1. Register your app in the Xaman Developer Portal
2. Copy credentials and URLs
3. Paste them into your SSO or access control platform
4. Done

### Example: Cloudflare Access

Cloudflare acts as the gatekeeper:

```
User tries to access your app
        ↓
Cloudflare redirects to Xaman for authentication
        ↓
User signs in with Xaman wallet
        ↓
Cloudflare allows access
```

No extra backend or frontend work on your part.

---

## When Is This Useful?

### Good Use Cases

- Building or securing **internal dashboards**
- Protecting **admin tools**
- **SaaS apps** wanting Xaman as the sole identity provider
- Integrating with **existing enterprise SSO**
- **Zero trust platforms** that support standard OAuth2/OIDC

### Real-World Example

The Xaman Developer Console itself uses this pattern. Signing in with Xaman is purely about identification.

---

## Is This Valuable for Most XRPL Projects?

**Probably not.**

The real value of Xaman for most developers is less about identifying users and more about:
- Getting their **r-address**
- Interacting with users **on the XRP Ledger**
- **Secure wallet signing** for transactions

### Identity vs Interaction

| Traditional SSO (Google, Microsoft) | Xaman |
|-------------------------------------|-------|
| Universal identity solution | Identity + on-chain interaction |
| Just verifying who someone is | Wallet signing, payments, NFTs |
| No blockchain component | Full XRPL integration |

Most of Xaman's unique power comes from **on-chain interaction and secure wallet signing**, not just identity verification.

---

## Should You Learn This in Detail?

### Yes, if:
- Targeting **enterprise deployments**
- Connecting with existing **SSO infrastructure**
- Building **internal tools** for blockchain companies
- Need **zero-trust access control** for XRPL apps

### Probably not, if:
- Building typical XRPL applications
- Focus is on **transactions and signing**
- Users interact primarily **on-chain**

---

## OpenID Connect Endpoints

Xaman provides standard OIDC endpoints:

| Endpoint | URL |
|----------|-----|
| Authorization | `https://oauth2.xaman.app/auth` |
| Token | `https://oauth2.xaman.app/token` |
| UserInfo | `https://oauth2.xaman.app/userinfo` |
| JWKS | `https://oauth2.xaman.app/.well-known/jwks.json` |
| Discovery | `https://oauth2.xaman.app/.well-known/openid-configuration` |

These endpoints are compatible with any OIDC-compliant system.

---

## Configuration Example

When setting up Xaman in an SSO provider, you typically need:

| Setting | Value |
|---------|-------|
| Client ID | Your Xaman API Key |
| Client Secret | Your Xaman API Secret |
| Authorization URL | `https://oauth2.xaman.app/auth` |
| Token URL | `https://oauth2.xaman.app/token` |
| Scopes | `openid` |
| Response Type | `code` |

The exact configuration varies by provider.

---

## Summary

| Aspect | Details |
|--------|---------|
| **What** | Xaman as standard OIDC identity provider |
| **How** | Configuration in SSO platforms, not coding |
| **Where** | Cloudflare, Okta, Auth0, any OIDC system |
| **For whom** | Enterprise, internal tools, SSO integration |
| **Not for** | Typical XRPL apps focused on transactions |

### Key Takeaways

1. **Xaman is standards-compliant** (OAuth2, OpenID Connect)
2. **Configuration over code** for SSO integration
3. **Works with enterprise platforms** (Cloudflare, Okta, etc.)
4. **Most XRPL developers** won't need this
5. **Real value** of Xaman is on-chain interaction, not just identity
6. **Good to know** it exists for when you need it

---

## Resources

- [Xaman OAuth2 and OpenID Connect](https://docs.xaman.dev/environments/identity-oauth2-openid#oauth2-and-openid-connect-endpoints)
- [Xaman Authorization Concepts](https://docs.xaman.dev/concepts/authorization#native-application)

---

## What's Next

With authentication covered comprehensively, we're ready to move on to building actual XRPL transactions with Xaman, including payments, NFT operations, and more.
