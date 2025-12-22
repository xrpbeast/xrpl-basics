# XRPL Meta API Documentation

XRPL Meta provides real-time and historical data for XRPL tokens through REST and WebSocket APIs.

## Base URLs

- **Primary Node**: `https://s1.xrplmeta.org` / `wss://s1.xrplmeta.org`
- **Full History**: `https://s2.xrplmeta.org` / `wss://s2.xrplmeta.org`
- **NFT Support**: `https://sx.xrplmeta.org` / `wss://sx.xrplmeta.org`

---

## REST API

### 1. Server Info

```bash
GET https://s1.xrplmeta.org/server
```

**Response**: Server status, sync state, ledger index

**Example**:
```javascript
const response = await fetch('https://s1.xrplmeta.org/server');
const data = await response.json();
console.log(data);
```

---

### 2. Ledger Data

```bash
GET https://s1.xrplmeta.org/ledger
```

**Response**: Current ledger information

---

### 3. List All Tokens

```bash
GET https://s1.xrplmeta.org/tokens
```

**Response**: Array of available tokens with metadata

**Example**:
```javascript
const response = await fetch('https://s1.xrplmeta.org/tokens');
const tokens = await response.json();
console.log(`Found ${tokens.length} tokens`);
```

---

### 4. Get Specific Token

```bash
GET https://s1.xrplmeta.org/token/{identifier}
```

**Identifier formats**:
- Currency code + Issuer: `USD+rN7n7otQDd6FczFgLdlqtyMVrn3HMfXEUD`
- Hex currency + Issuer: `24425542424C4553000000000000000000000000+rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs`

**Response**: Token metadata, supply, holders, trustlines, volume, price data

#### Example: $BUBBLES Token

```javascript
// Using issuer and currency hash
const issuer = 'rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs';
const currencyHex = '24425542424C4553000000000000000000000000'; // $BUBBLES
const identifier = `${currencyHex}+${issuer}`;

const response = await fetch(`https://s1.xrplmeta.org/token/${identifier}`);
const bubbles = await response.json();

console.log({
  name: bubbles.meta?.name,
  supply: bubbles.supply,
  holders: bubbles.holders,
  trustlines: bubbles.trustlines,
  price: bubbles.metrics?.price,
  volume24h: bubbles.metrics?.volume_24h
});
```

#### TypeScript Example

```typescript
interface TokenMetrics {
  price?: number;
  volume_24h?: number;
  volume_7d?: number;
  price_change_24h?: number;
  market_cap?: number;
}

interface TokenData {
  currency: string;
  issuer: string;
  meta?: {
    name?: string;
    symbol?: string;
    description?: string;
    website?: string;
  };
  supply?: number;
  holders?: number;
  trustlines?: number;
  metrics?: TokenMetrics;
}

async function getTokenData(currencyHex: string, issuer: string): Promise<TokenData> {
  const identifier = `${currencyHex}+${issuer}`;
  const response = await fetch(`https://s1.xrplmeta.org/token/${identifier}`);

  if (!response.ok) {
    throw new Error(`Failed to fetch token: ${response.statusText}`);
  }

  return await response.json();
}

// Usage
const bubbles = await getTokenData(
  '24425542424C4553000000000000000000000000',
  'rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs'
);
```

---

### 5. Get Time Series Data

```bash
GET https://s1.xrplmeta.org/token/{identifier}/series/{metric}
```

**Available metrics**: `price`, `volume`, `holders`, `trustlines`, `supply`

**Query parameters**:
- `period`: `1h`, `4h`, `1d`, `1w`, `1m`
- `limit`: Number of data points (default: 100)

#### Example: $BUBBLES Price History

```javascript
const issuer = 'rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs';
const currencyHex = '24425542424C4553000000000000000000000000';
const identifier = `${currencyHex}+${issuer}`;

// Get daily price data for last 30 days
const response = await fetch(
  `https://s1.xrplmeta.org/token/${identifier}/series/price?period=1d&limit=30`
);
const priceHistory = await response.json();

priceHistory.forEach(point => {
  console.log(`${point.timestamp}: $${point.value}`);
});
```

#### Example: Volume Tracking

```javascript
const identifier = '24425542424C4553000000000000000000000000+rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs';

async function getVolumeStats() {
  const response = await fetch(
    `https://s1.xrplmeta.org/token/${identifier}/series/volume?period=1h&limit=24`
  );
  const hourlyVolume = await response.json();

  const total24h = hourlyVolume.reduce((sum, point) => sum + point.value, 0);
  console.log(`24h volume: ${total24h.toFixed(2)} XRP`);

  return hourlyVolume;
}
```

---

## WebSocket API

### Connection

```javascript
const ws = new WebSocket('wss://s1.xrplmeta.org');

ws.onopen = () => {
  console.log('Connected to XRPL Meta');
};

ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  console.log('Received:', data);
};

ws.onerror = (error) => {
  console.error('WebSocket error:', error);
};

ws.onclose = () => {
  console.log('Disconnected');
};
```

---

### Commands

#### 1. Server Info

```javascript
ws.send(JSON.stringify({
  command: 'server_info'
}));
```

#### 2. Get Token Data

```javascript
const issuer = 'rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs';
const currencyHex = '24425542424C4553000000000000000000000000';

ws.send(JSON.stringify({
  command: 'token',
  identifier: `${currencyHex}+${issuer}`
}));
```

#### 3. Subscribe to Token Updates

```javascript
ws.send(JSON.stringify({
  command: 'tokens_subscribe',
  identifiers: ['24425542424C4553000000000000000000000000+rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs']
}));

// Real-time updates will be sent automatically
ws.onmessage = (event) => {
  const update = JSON.parse(event.data);
  if (update.type === 'token_update') {
    console.log('Price updated:', update.metrics.price);
  }
};
```

#### 4. Unsubscribe

```javascript
ws.send(JSON.stringify({
  command: 'tokens_unsubscribe',
  identifiers: ['24425542424C4553000000000000000000000000+rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs']
}));
```

---

## Complete Examples

### React Hook for Token Data

```typescript
import { useState, useEffect } from 'react';

interface TokenData {
  currency: string;
  issuer: string;
  supply?: number;
  holders?: number;
  metrics?: {
    price?: number;
    volume_24h?: number;
  };
}

export function useToken(currencyHex: string, issuer: string) {
  const [token, setToken] = useState<TokenData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<Error | null>(null);

  useEffect(() => {
    const identifier = `${currencyHex}+${issuer}`;

    fetch(`https://s1.xrplmeta.org/token/${identifier}`)
      .then(res => res.json())
      .then(data => {
        setToken(data);
        setLoading(false);
      })
      .catch(err => {
        setError(err);
        setLoading(false);
      });
  }, [currencyHex, issuer]);

  return { token, loading, error };
}

// Usage
function BubblesToken() {
  const { token, loading } = useToken(
    '24425542424C4553000000000000000000000000',
    'rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs'
  );

  if (loading) return <div>Loading...</div>;

  return (
    <div>
      <h2>$BUBBLES</h2>
      <p>Price: ${token?.metrics?.price}</p>
      <p>Holders: {token?.holders}</p>
      <p>24h Volume: {token?.metrics?.volume_24h} XRP</p>
    </div>
  );
}
```

### Node.js Monitoring Script

```javascript
const WebSocket = require('ws');

class TokenMonitor {
  constructor(currencyHex, issuer) {
    this.identifier = `${currencyHex}+${issuer}`;
    this.ws = null;
  }

  connect() {
    this.ws = new WebSocket('wss://s1.xrplmeta.org');

    this.ws.on('open', () => {
      console.log('Connected to XRPL Meta');
      this.subscribe();
    });

    this.ws.on('message', (data) => {
      const message = JSON.parse(data);
      this.handleUpdate(message);
    });

    this.ws.on('error', (error) => {
      console.error('WebSocket error:', error);
    });

    this.ws.on('close', () => {
      console.log('Connection closed, reconnecting...');
      setTimeout(() => this.connect(), 5000);
    });
  }

  subscribe() {
    this.ws.send(JSON.stringify({
      command: 'tokens_subscribe',
      identifiers: [this.identifier]
    }));
  }

  handleUpdate(message) {
    if (message.type === 'token_update') {
      console.log('\n--- Token Update ---');
      console.log('Price:', message.metrics?.price);
      console.log('Volume:', message.metrics?.volume_24h);
      console.log('Holders:', message.holders);
    }
  }

  disconnect() {
    if (this.ws) {
      this.ws.close();
    }
  }
}

// Monitor $BUBBLES token
const monitor = new TokenMonitor(
  '24425542424C4553000000000000000000000000',
  'rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs'
);

monitor.connect();

// Graceful shutdown
process.on('SIGINT', () => {
  console.log('\nShutting down...');
  monitor.disconnect();
  process.exit(0);
});
```

### Python Example

```python
import requests
import websocket
import json
import threading

class XRPLMetaClient:
    def __init__(self, base_url='https://s1.xrplmeta.org'):
        self.base_url = base_url
        self.ws_url = 'wss://s1.xrplmeta.org'

    def get_token(self, currency_hex, issuer):
        identifier = f"{currency_hex}+{issuer}"
        response = requests.get(f"{self.base_url}/token/{identifier}")
        response.raise_for_status()
        return response.json()

    def get_series(self, currency_hex, issuer, metric, period='1d', limit=30):
        identifier = f"{currency_hex}+{issuer}"
        params = {'period': period, 'limit': limit}
        response = requests.get(
            f"{self.base_url}/token/{identifier}/series/{metric}",
            params=params
        )
        response.raise_for_status()
        return response.json()

# Example usage
client = XRPLMetaClient()

# Get $BUBBLES token data
bubbles = client.get_token(
    '24425542424C4553000000000000000000000000',
    'rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs'
)

print(f"Token: {bubbles.get('meta', {}).get('name', 'Unknown')}")
print(f"Price: ${bubbles.get('metrics', {}).get('price', 0)}")
print(f"Holders: {bubbles.get('holders', 0)}")

# Get price history
price_history = client.get_series(
    '24425542424C4553000000000000000000000000',
    'rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs',
    'price',
    period='1d',
    limit=7
)

print("\n7-day price history:")
for point in price_history:
    print(f"{point['timestamp']}: ${point['value']}")
```

---

## Currency Code Format

XRPL supports both standard currency codes (3 letters) and hex-encoded currency codes (40 hex characters).

**$BUBBLES Example**:
- ASCII: `$BUBBLES`
- Hex: `24425542424C4553000000000000000000000000`

**Converting currency codes**:

```javascript
function currencyToHex(currency) {
  if (currency.length === 3) {
    return currency.toUpperCase();
  }

  // Pad with zeros to 40 characters
  const hex = Buffer.from(currency, 'utf8').toString('hex').toUpperCase();
  return hex.padEnd(40, '0');
}

function hexToCurrency(hex) {
  if (hex.length === 3) {
    return hex;
  }

  // Remove trailing zeros and convert
  const trimmed = hex.replace(/0+$/, '');
  return Buffer.from(trimmed, 'hex').toString('utf8');
}

// Examples
console.log(currencyToHex('$BUBBLES'));
// 24425542424C4553000000000000000000000000

console.log(hexToCurrency('24425542424C4553000000000000000000000000'));
// $BUBBLES
```

---

## Rate Limits

- REST API: Not explicitly documented, use reasonable request rates
- WebSocket: Single connection can subscribe to multiple tokens
- Recommended: Cache data when possible, use WebSocket for real-time updates

---

## Error Handling

```javascript
async function safeGetToken(currencyHex, issuer) {
  try {
    const identifier = `${currencyHex}+${issuer}`;
    const response = await fetch(`https://s1.xrplmeta.org/token/${identifier}`);

    if (!response.ok) {
      if (response.status === 404) {
        throw new Error('Token not found');
      }
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to fetch token:', error);
    throw error;
  }
}
```

---

## Resources

- **API Base**: https://xrplmeta.org/docs
- **Public Nodes**: s1, s2, sx.xrplmeta.org
- **WebSocket**: Real-time token updates and subscriptions
- **XRPL Explorer**: https://livenet.xrpl.org

---

## Example: $BUBBLES Dashboard

```javascript
class BubblesDashboard {
  constructor() {
    this.currencyHex = '24425542424C4553000000000000000000000000';
    this.issuer = 'rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs';
    this.ws = null;
  }

  async init() {
    // Fetch initial data
    await this.fetchTokenData();
    await this.fetchPriceHistory();

    // Connect WebSocket for real-time updates
    this.connectWebSocket();
  }

  async fetchTokenData() {
    const identifier = `${this.currencyHex}+${this.issuer}`;
    const response = await fetch(`https://s1.xrplmeta.org/token/${identifier}`);
    const data = await response.json();

    console.log('=== $BUBBLES Token Info ===');
    console.log('Supply:', data.supply);
    console.log('Holders:', data.holders);
    console.log('Trustlines:', data.trustlines);
    console.log('Price:', data.metrics?.price);
    console.log('24h Volume:', data.metrics?.volume_24h);
  }

  async fetchPriceHistory() {
    const identifier = `${this.currencyHex}+${this.issuer}`;
    const response = await fetch(
      `https://s1.xrplmeta.org/token/${identifier}/series/price?period=1h&limit=24`
    );
    const history = await response.json();

    console.log('\n=== 24h Price Chart ===');
    history.forEach(point => {
      const bar = '█'.repeat(Math.floor(point.value * 100));
      console.log(`${point.timestamp}: ${bar} $${point.value}`);
    });
  }

  connectWebSocket() {
    this.ws = new WebSocket('wss://s1.xrplmeta.org');

    this.ws.onopen = () => {
      console.log('\n=== Live Updates Started ===');
      this.ws.send(JSON.stringify({
        command: 'tokens_subscribe',
        identifiers: [`${this.currencyHex}+${this.issuer}`]
      }));
    };

    this.ws.onmessage = (event) => {
      const data = JSON.parse(event.data);
      if (data.type === 'token_update') {
        console.log('\n[UPDATE]', new Date().toISOString());
        console.log('Price:', data.metrics?.price);
        console.log('Volume:', data.metrics?.volume_24h);
      }
    };
  }
}

// Run dashboard
const dashboard = new BubblesDashboard();
dashboard.init();
```
