# Installing rippled

In this lecture, we'll set up a rippled stock node from scratch on Ubuntu.

**Important:** Make sure you've completed all prerequisites from the previous lecture before proceeding.

---

## A Note on Permissions

You'll need root access for installation. You have two options:

1. **Use `sudo`** for each command (recommended, best practice)
2. **Elevate to root** with `sudo su` (easier but less secure)

Choose based on your comfort level with Linux.

---

## Installation Steps

We'll follow the [official Ubuntu installation guide](https://xrpl.org/docs/infrastructure/installation/install-rippled-on-ubuntu).

### 1. Install Prerequisites

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y apt-transport-https ca-certificates wget gnupg
```

### 2. Add Ripple's Package Signing Key

```bash
sudo mkdir -p /usr/local/share/keyrings/
wget -q -O - "https://repos.ripple.com/repos/api/gpg/key/public" | \
  gpg --dearmor | sudo tee /usr/local/share/keyrings/ripple.gpg > /dev/null
```

### 3. Verify the Key Fingerprint

```bash
gpg --show-keys /usr/local/share/keyrings/ripple.gpg
```

Look for fingerprint ending in: `...C001 0EC2 05B3 5A33 10DC 90DE 395F 97FF CCAF D9A2`

### 4. Add the Repository

**Important:** Replace the Ubuntu version codename to match your distribution!

| Ubuntu Version | Codename |
|----------------|----------|
| 20.04 | focal |
| 22.04 | jammy |
| 24.04 | noble |

Check your version:
```bash
lsb_release -cs
```

Add the repository (example for Ubuntu 22.04 Jammy):

```bash
echo "deb [signed-by=/usr/local/share/keyrings/ripple.gpg] \
  https://repos.ripple.com/repos/rippled-deb jammy stable" | \
  sudo tee /etc/apt/sources.list.d/ripple.list
```

### 5. Update and Install rippled

```bash
sudo apt update
sudo apt install -y rippled
```

---

## Verify Installation

### Check rippled Status

```bash
sudo systemctl status rippled
```

You should see: `Active: active (running)`

### Check Server Info

```bash
rippled server_info
```

**Important fields to check:**

| Field | What to Look For |
|-------|------------------|
| `server_state` | Should eventually show `full` (fully synced) |
| `peers` | Should be > 10 after firewall configuration |

**Note:** If you run this immediately after installation, `server_state` may show `connecting`. This is normal - it takes a few minutes to fully synchronize.

---

## Firewall Configuration

If your `peers` count is stuck at 10, you need to open port 51235 on your internal firewall.

### Using UFW (Uncomplicated Firewall)

```bash
sudo ufw allow 51235/tcp
sudo ufw status
```

### Using iptables

```bash
sudo iptables -A INPUT -p tcp --dport 51235 -j ACCEPT
```

After opening the port, wait a few minutes and check again:

```bash
rippled server_info
```

You should see the peer count increasing (21+).

---

## Success Indicators

Your rippled stock node is running correctly when:

- ✅ `systemctl status rippled` shows `active (running)`
- ✅ `server_state` shows `full`
- ✅ `peers` count is growing (21+ is good)

---

## Common Issues

### Server State Stuck on "connecting"

- **Normal** for the first few minutes after installation
- If it persists, check your internet connection and firewall rules

### Low Peer Count (≤10)

- Port 51235 is likely blocked
- Check both network firewall AND host firewall (UFW/iptables)
- Cloud providers (AWS, Azure) may have additional security groups to configure

### Installation Fails

- Verify you're using the correct Ubuntu version codename
- Ensure you have sufficient disk space and RAM
- Check that all prerequisite packages are installed

---

## What's Next

Rippled is now running as a stock node and participating in the network. In the next lecture, we'll walk through configuration changes needed to use this node for development.

---

## Resources

- [Install rippled on Ubuntu](https://xrpl.org/docs/infrastructure/installation/install-rippled-on-ubuntu)
- [rippled System Requirements](https://xrpl.org/docs/infrastructure/installation/system-requirements)
