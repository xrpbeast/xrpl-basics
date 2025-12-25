# Maintaining rippled

In this lecture, we'll cover maintenance of your rippled instance and its infrastructure.

---

## Three Areas of Maintenance

1. **Server infrastructure** - The underlying system
2. **rippled daemon** - The software itself
3. **Upgrading rippled** - Keeping up to date

---

## 1. Server Infrastructure Maintenance

Rippled is just software running on your server. Standard server maintenance applies:

- **Logging and monitoring** - Ensure good health
- **Regular patching** - Keep the OS up to date
- **Security reviews** - Periodic policy reviews
- **Backup and recovery** - Have policies in place
- **Network configuration** - Regular audits
- **Cleanup tasks** - Disk space, logs
- **Performance improvements** - As needed

**Bottom line:** A healthy rippled instance requires a healthy, secure server.

---

## 2. rippled Daemon Maintenance

For complex setups (full history nodes, clusters), there's significant operational work. However, for most developers running a stock node or validator, day-to-day maintenance is minimal.

### Weekly Tasks for Node Operators

| Task | Description |
|------|-------------|
| **Monitor uptime** | Ensure your node is running |
| **Follow amendments** | Stay informed about proposed changes |
| **Contribute feedback** | Engage in discussions |
| **Keep updated** | Avoid amendment blocking |

---

## 3. Upgrading rippled

As a rippled admin, understanding the upgrade process is essential.

### Two Upgrade Methods

| Method | Pros | Cons |
|--------|------|------|
| **Automatic** | Less manual work | Still requires restart; not fully hands-off |
| **Manual** | Full control over timing | Requires monitoring for new releases |

### The Reality of "Automatic" Updates

Even with automatic updates enabled:
- You still need to **restart rippled** for changes to take effect
- This is by design to prevent too many nodes going offline simultaneously
- You still need to know when updates go live

Most infrastructure providers prefer manual updates for greater control.

---

## Manual Upgrade Process

### Step 1: Backup Your Config

**Always backup before upgrading!**

```bash
sudo cp /opt/ripple/etc/rippled.cfg /opt/ripple/etc/rippled.cfg.backup
```

### Step 2: Check Current Version

```bash
rippled server_info | grep build_version
```

### Step 3: Update Package List

```bash
sudo apt update
```

### Step 4: Perform Upgrade

```bash
sudo apt upgrade rippled
```

### Handling Config File Prompts

During upgrade, you may be prompted about a new config file version:

**Options:**
1. **Keep your existing config** - Then manually review new file for important changes
2. **Accept new config** - Then restore your customizations

**Recommendation:** Accept the new version, then add your customizations back. This ensures you don't miss important new settings.

### Step 5: Restart rippled

```bash
sudo systemctl daemon-reload
sudo systemctl restart rippled
```

### Step 6: Verify Upgrade

Check status:
```bash
sudo systemctl status rippled
```

Check version:
```bash
rippled server_info | grep build_version
```

---

## Setting Up Automatic Updates

A cron job is already prepared during installation. To enable it:

```bash
sudo ln -s /opt/ripple/etc/update-rippled-cron /etc/cron.d/update-rippled-cron
```

### How It Works

The cron job runs every 59 minutes, checking for and installing new releases.

View the job:
```bash
cat /opt/ripple/etc/update-rippled-cron
```

**Remember:** Updates are downloaded automatically, but rippled still needs a manual restart to apply them.

---

## Staying Informed

### Where to Monitor Updates

- [XRPL GitHub Releases](https://github.com/XRPLF/rippled/releases)
- [XRPL Developer Discord](https://discord.gg/xrpl)
- [Twitter/X XRPL Community](https://twitter.com/XRPLF)

### Amendment Awareness

New amendments require attention:
- Understand what's being proposed
- Ensure your rippled version supports it
- Avoid becoming amendment blocked

---

## Amendment Blocking Prevention

If your rippled version doesn't support an activated amendment:

1. Your node becomes **amendment blocked**
2. It can no longer participate in consensus
3. It can no longer process transactions properly

**Prevention:** Upgrade promptly when new versions are released, especially before amendment activation dates.

---

## Summary

| Area | Key Actions |
|------|-------------|
| **Server** | Standard maintenance, monitoring, patching |
| **rippled** | Monitor uptime, engage with community |
| **Upgrades** | Backup config, upgrade, restart, verify |

### Best Practices

1. **Always backup** your config before upgrading
2. **Monitor** for new releases and amendments
3. **Engage** with the developer community
4. **Choose** manual or automatic updates based on your preference
5. **Restart** rippled after updates (even with auto-updates)
6. **Verify** successful upgrades with `server_info`

---

## Resources

- [Update rippled Automatically on Linux](https://xrpl.org/docs/infrastructure/installation/update-rippled-automatically-on-linux)
- [rippled Releases](https://github.com/XRPLF/rippled/releases)
- [Known Amendments](https://xrpl.org/docs/references/protocol/transactions/pseudo-transaction-types/enableamendment)
