# Running a Validator

In this lecture, we'll convert our stock node into a validator.

---

## Stock Node vs Validator

A validator does everything a stock node does, **plus** participates in consensus.

| Node Type | Submits Txns | Ledger History | Consensus |
|-----------|--------------|----------------|-----------|
| Stock Node | Yes | Yes | No |
| Validator | Yes | Yes | **Yes** |

### When to Run Each

**Stock Node (Submission Node):**
- You want control and security of your own infrastructure
- You need reliable transaction submission
- You want to query the ledger directly

**Validator:**
- You want to contribute to network health and security
- You're running a commercial project and want to be a responsible participant
- Even without UNL inclusion, validators add value to the network

---

## Important: Validator Security

**Validators should NOT be publicly accessible.**

If you want both:
- A public submission endpoint, AND
- A validator contributing to consensus

You should run **two separate nodes**:
1. A stock server as public proxy
2. A validator on a private network, accessible only through the stock server

This protects the integrity of your validator.

---

## Step 1: Remove Public WebSocket Access

### Edit Nginx Config

```bash
sudo nano /etc/nginx/sites-available/xrpl-node.yourdomain.com
```

Remove the WebSocket forwarding location block.

### Edit rippled Config

```bash
sudo nano /opt/ripple/etc/rippled.cfg
```

Comment out the WebSocket public sections:

```ini
# [port_ws_public]
# port = 6005
# ip = 127.0.0.1
# protocol = ws
```

### Close Internal Port

```bash
sudo ufw deny 6005/tcp
sudo ufw status
```

### Restart Services

```bash
sudo systemctl restart nginx
sudo systemctl restart rippled
sudo systemctl status rippled
```

**Note:** Keep the website and SSL certificates. We'll need them for domain verification.

---

## Step 2: Generate Validator Keys

### Get the Validator Keys Tool

**Option 1:** Build from official repo (recommended for production)
- Follow the [official guide](https://xrpl.org/docs/infrastructure/configuration/server-modes/run-rippled-as-a-validator)

**Option 2:** Use portable version from XRPL Labs
- Available on GitHub (if you trust the source)

### Important Security Warning

**DO NOT generate keys on the validator server in production!**

Best practice:
1. Generate keys on an **offline machine**
2. Store in a secure, recoverable location (encrypted USB)
3. Only copy the token to the validator

### Upload Tool to Server

```bash
scp validator-keys-tool user@your-server:~/
```

### Make Executable

```bash
chmod +x validator-keys-tool
```

### Create Validator Keys

```bash
./validator-keys-tool create_keys
```

Keys are stored in `validator-keys.json`:

```json
{
  "key_type": "ed25519",
  "public_key": "nHU...",
  "secret_key": "p..."
}
```

| Field | Purpose |
|-------|---------|
| `public_key` | Identifies your validator on the network |
| `secret_key` | Signs transactions authorizing rippled to run as validator |

**Never share your secret key!**

---

## Step 3: Create Validator Token

```bash
./validator-keys-tool create_token --keyfile validator-keys.json
```

Output:

```
[validator_token]
eyJ2YWxpZGF0aW9uX3NlY3JldF9rZXkiOi...
```

Each new token invalidates all previous tokens for that public key.

---

## Step 4: Domain Verification (Optional but Recommended)

Required if you want a chance at UNL inclusion.

### Set Domain

```bash
./validator-keys-tool set_domain xrpl-node.yourdomain.com --keyfile validator-keys.json
```

This generates:
- A new token
- An attestation for your TOML file

### Create TOML File

Create the `.well-known` directory:

```bash
sudo mkdir -p /var/www/xrpl-node/.well-known
```

Create the TOML file:

```bash
sudo nano /var/www/xrpl-node/.well-known/xrp-ledger.toml
```

Content:

```toml
[[VALIDATORS]]
public_key = "nHU..."
attestation = "eyJ..."
```

### Update Nginx for TOML

Edit nginx config to serve TOML with correct headers:

```nginx
location /.well-known/xrp-ledger.toml {
    add_header Access-Control-Allow-Origin *;
    add_header Content-Type application/toml;
}
```

Restart nginx:

```bash
sudo systemctl restart nginx
```

### Verify TOML Access

Navigate to: `https://xrpl-node.yourdomain.com/.well-known/xrp-ledger.toml`

The file should download automatically.

---

## Step 5: Add Token to rippled

Edit the config:

```bash
sudo nano /opt/ripple/etc/rippled.cfg
```

Add at the bottom:

```ini
[validator_token]
eyJ2YWxpZGF0aW9uX3NlY3JldF9rZXkiOi...
```

Restart rippled:

```bash
sudo systemctl restart rippled
```

---

## Step 6: Verify Validator Status

Check server info:

```bash
rippled server_info
```

Look for:
- `pubkey_validator`: Your public validator key
- `server_state`: Should change from `connected` to `proposing`

**Note:** It may take a few minutes after restart to reach `proposing` state.

### Check on Live Explorer

Visit the [XRPL Validators page](https://livenet.xrpl.org/network/validators) and search for your public key.

---

## Step 7: Security Best Practices

### Lock Down Config File

Remove access for everyone except the rippled user:

```bash
sudo chmod 600 /opt/ripple/etc/rippled.cfg
sudo chown rippled:rippled /opt/ripple/etc/rippled.cfg
```

This applies to both validators AND stock nodes.

---

## Validator States

| State | Meaning |
|-------|---------|
| `connected` | Syncing with network |
| `proposing` | Actively participating in consensus |
| `full` | Fully synced (stock node) |

---

## Key Takeaways

1. **Validators participate in consensus** while stock nodes only submit/query
2. **Validators should not be publicly accessible** - run separate nodes if you need both
3. **Generate keys offline** for production validators
4. **Each token invalidates previous tokens** for that public key
5. **Domain verification** is required for UNL consideration
6. **Lock down config files** with proper permissions
7. **Even non-UNL validators** contribute to network health

---

## Resources

- [Run rippled as a Validator](https://xrpl.org/docs/infrastructure/configuration/server-modes/run-rippled-as-a-validator)
- [Domain Verification](https://xrpl.org/docs/infrastructure/configuration/server-modes/run-rippled-as-a-validator#6-provide-domain-verification)
- [XRPL Foundation Validator Guidelines](https://foundation.xrpl.org/)
- [Live Validators List](https://livenet.xrpl.org/network/validators)
