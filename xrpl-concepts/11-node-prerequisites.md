# Node Prerequisites

Before we set up our rippled node, there are some prerequisites to cover.

---

## Server Requirements

### Operating System

You'll need a **Linux server** with an **Ubuntu distribution**.

Hosting options:
- **Cloud providers**: AWS, Azure, Google Cloud, DigitalOcean, etc.
- **Local machine**: Your own hardware
- **VirtualBox**: For testing/learning purposes

### Minimum Hardware Specifications

| Resource | Minimum Requirement |
|----------|---------------------|
| **CPU** | 4 cores |
| **RAM** | 16 GB |
| **Storage** | SSD capable of sustaining **10,000 IOPS** |

**Note:** These are minimums. For production validators or full history nodes, you'll want significantly more resources.

---

## Pre-Setup Checklist

Before starting the rippled setup, ensure you have:

### 1. Updated System Packages

Upgrade all packages so your machine is up to date:

```bash
sudo apt update && sudo apt upgrade -y
```

### 2. Root Access

You'll need root or sudo access to the server for installation and configuration.

### 3. Open Firewall Ports

The following ports need to be opened on your network firewall:

| Port | Purpose |
|------|---------|
| **22** | SSH access |
| **80** | HTTP (for SSL certificate validation) |
| **443** | HTTPS |
| **51235** | Peer protocol (rippled peer-to-peer communication) |

Example using UFW (Ubuntu Firewall):

```bash
sudo ufw allow 22/tcp
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw allow 51235/tcp
sudo ufw enable
```

### 4. Domain Name with DNS

You'll need:
- Your own domain name (e.g., `xrpl-node.yourdomain.com`)
- DNS configured and pointing to your server's IP address

This is required for SSL certificates and secure connections.

---

## Quick Verification

Before proceeding, verify:

```bash
# Check Ubuntu version
lsb_release -a

# Check available disk space
df -h

# Check RAM
free -h

# Check CPU cores
nproc

# Verify ports are open (from another machine)
# nc -zv your-server-ip 51235
```

---

## What's Next

Once you have all prerequisites in place, we'll set up a rippled stock node together in the next lecture.
