# Configuring rippled

In this lecture, we'll configure the rippled node we built in the previous lecture to enable WebSocket access.

---

## The rippled Config File

The config file is located at:

```
/opt/ripple/etc/rippled.cfg
```

This file is an excellent learning resource. It contains extensive documentation explaining all the different settings and configuration options. Take time to scroll through and read the comments.

---

## Online Deletion Settings

This setting determines how much ledger history your node keeps:

```ini
[ledger_history]
512
```

| Value | Meaning |
|-------|---------|
| 256 | Minimum allowed |
| 512 | Recommended default |
| Higher | More history, more disk space |

The appropriate value depends on your use case. For most development purposes, the default of 512 is fine.

---

## WebSocket Access Options

There are multiple ways to configure WebSocket access:

### Option 1: Nginx Proxy (Recommended)

What we'll use:
- Traffic comes in via **WSS on port 443** (standard HTTPS port)
- Nginx terminates SSL and forwards to rippled on port 6005
- Domain with SSL certificate (Let's Encrypt)

**Benefits:**
- No need to open port 6005 on external firewall
- Let's Encrypt auto-renewal works seamlessly
- Easy to scale horizontally behind the proxy
- Standard port (443) for clients

### Option 2: Direct rippled SSL

- Open port 6005 on firewall
- Configure SSL certificates directly in rippled
- Requires rippled restart on certificate renewal

### Option 3: Direct Port Exposure

- Expose rippled directly on port 443 or 80
- Documented on the official installation page

---

## Configuring rippled for WebSocket

Edit the config file:

```bash
sudo nano /opt/ripple/etc/rippled.cfg
```

Find and modify the WebSocket section:

```ini
[port_ws_public]
port = 6005
ip = 127.0.0.1
protocol = ws
```

**Key settings:**

| Setting | Value | Notes |
|---------|-------|-------|
| `port` | 6005 | Default WebSocket port |
| `ip` | 127.0.0.1 | Localhost only (nginx will proxy) |
| `protocol` | ws | Not wss, since nginx handles SSL |

**Why `ws` instead of `wss`?**

Since nginx handles SSL termination, the internal traffic between nginx and rippled is over localhost HTTP. This is secure because it never leaves the machine.

Save and exit. We'll restart rippled after setting up nginx.

---

## Installing Nginx

```bash
sudo apt update
sudo apt install -y nginx
```

---

## Creating the Site Configuration

Create a config file for your domain:

```bash
sudo nano /etc/nginx/sites-available/xrpl-node.yourdomain.com
```

Basic configuration:

```nginx
server {
    listen 80;
    server_name xrpl-node.yourdomain.com;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }
}
```

Enable the site:

```bash
sudo ln -s /etc/nginx/sites-available/xrpl-node.yourdomain.com /etc/nginx/sites-enabled/
```

Open firewall ports:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

Restart nginx:

```bash
sudo systemctl restart nginx
```

Test by visiting `http://xrpl-node.yourdomain.com` in your browser.

---

## Setting Up SSL with Let's Encrypt

Install Certbot:

```bash
sudo apt install -y certbot python3-certbot-nginx
```

Obtain and install certificate:

```bash
sudo certbot --nginx -d xrpl-node.yourdomain.com
```

Follow the wizard. Certbot will:
1. Verify domain ownership
2. Obtain the certificate
3. Automatically configure nginx

Certificates are stored in `/etc/letsencrypt/live/xrpl-node.yourdomain.com/`

Restart nginx:

```bash
sudo systemctl restart nginx
```

Test by visiting `https://xrpl-node.yourdomain.com`

---

## Adding WebSocket Proxy Configuration

Edit your nginx config:

```bash
sudo nano /etc/nginx/sites-available/xrpl-node.yourdomain.com
```

Add WebSocket location inside the `server` block (the one listening on 443):

```nginx
location /ws {
    proxy_pass http://127.0.0.1:6005;
    proxy_http_version 1.1;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Connection "upgrade";
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
    proxy_set_header X-Forwarded-Proto $scheme;
    proxy_read_timeout 86400;
}
```

This configuration:
- Routes `/ws` path to rippled
- Upgrades connection for WebSocket protocol
- Forwards to localhost:6005 over HTTP (not HTTPS)

---

## Open Internal Port and Restart Services

Allow nginx to reach rippled:

```bash
sudo ufw allow 6005/tcp
```

Restart rippled to apply config changes:

```bash
sudo systemctl restart rippled
```

Verify rippled is running:

```bash
sudo systemctl status rippled
```

Restart nginx:

```bash
sudo systemctl restart nginx
```

---

## Testing the WebSocket

### Using Postman

1. Create new WebSocket request
2. URL: `wss://xrpl-node.yourdomain.com/ws`
3. Click Connect
4. Send a message:

```json
{
  "command": "server_info"
}
```

You should receive the same output as `rippled server_info`.

### Using JavaScript

```javascript
const socket = new WebSocket('wss://xrpl-node.yourdomain.com/ws');

socket.onopen = () => {
  socket.send(JSON.stringify({ command: 'server_info' }));
};

socket.onmessage = (event) => {
  console.log(JSON.parse(event.data));
};
```

---

## Complete Nginx Config Example

```nginx
server {
    listen 80;
    server_name xrpl-node.yourdomain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name xrpl-node.yourdomain.com;

    ssl_certificate /etc/letsencrypt/live/xrpl-node.yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/xrpl-node.yourdomain.com/privkey.pem;

    root /var/www/html;
    index index.html;

    location / {
        try_files $uri $uri/ =404;
    }

    location /ws {
        proxy_pass http://127.0.0.1:6005;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 86400;
    }
}
```

---

## Common Issues

### WebSocket Not Connecting

1. Did you restart rippled after config changes?
2. Is port 6005 open on internal firewall?
3. Check nginx error logs: `sudo tail -f /var/log/nginx/error.log`

### Certificate Issues

- Ensure DNS is properly pointing to your server
- Check certbot logs: `sudo certbot certificates`

---

## Key Takeaways

1. **Config file location**: `/opt/ripple/etc/rippled.cfg`
2. **Online deletion**: Controls ledger history retention (default 512)
3. **Nginx as proxy**: Handles SSL, forwards to rippled on 6005
4. **Let's Encrypt**: Free SSL with auto-renewal
5. **Protocol ws not wss**: Nginx terminates SSL, internal traffic is HTTP
6. **Always restart rippled** after config changes

---

## What's Next

You now have a fully configured rippled stock node with secure WebSocket access. In future lectures, we'll explore:
- Running as a validator
- Advanced configuration options
- Monitoring and maintenance
