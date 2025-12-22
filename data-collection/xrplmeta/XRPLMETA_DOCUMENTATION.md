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

**Real Response**:
```json
{
  "server_version": "2.22.0-alpha",
  "available_range": {
    "sequence": {
      "start": 94898013,
      "end": 101048065
    },
    "time": {
      "start": 1742473002,
      "end": 1766408700
    }
  },
  "trustlists": [
    {
      "id": "xrplmeta",
      "url": "https://xrplmeta.org/trusted.toml",
      "trust_level": 3
    },
    {
      "id": "xaman",
      "url": "https://unhosted.exchange/tokens.toml",
      "trust_level": 3
    }
  ],
  "total_tokens": 185368,
  "total_nfts": 0
}
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

**Response**: Object with count and tokens array

**Example**:
```javascript
const response = await fetch('https://s1.xrplmeta.org/tokens');
const data = await response.json();
console.log(`Found ${data.count} tokens`);
console.log('First token:', data.tokens[0]);
```

**Real Response Structure**:
```json
{
  "count": 185270,
  "tokens": [
    {
      "currency": "534F4C4F00000000000000000000000000000000",
      "issuer": "rsoLo2S1kiGeCcn6hCUXVrCpGMWLrRrLZz",
      "meta": {
        "token": {
          "name": "SOLO",
          "desc": "SOLO is the utility token for the Sologenic ecosystem...",
          "icon": "https://s1.xrplmeta.org/icon/C40439709A.png",
          "trust_level": 3,
          "urls": [{"url": "https://sologenic.com", "type": "website"}]
        },
        "issuer": {
          "name": "Sologenic",
          "domain": "sologenic.com",
          "kyc": true,
          "trust_level": 3
        }
      },
      "metrics": {
        "trustlines": 284576,
        "holders": 218432,
        "supply": "398752707.199299",
        "marketcap": "31272825.210684",
        "price": "0.0784266154086664",
        "volume_24h": "31521.5954929992",
        "volume_7d": "341862.228702793",
        "exchanges_24h": "1238",
        "exchanges_7d": "13538",
        "takers_24h": "100",
        "takers_7d": "404"
      }
    }
  ]
}
```

---

### 4. Get Specific Token

```bash
GET https://s1.xrplmeta.org/token/{identifier}
```

**Identifier format**: `{currency}:{issuer}`

**Examples**:
- Standard 3-letter code: `USD:rN7n7otQDd6FczFgLdlqtyMVrn3HMfXEUD`
- Hex currency code: `24425542424C4553000000000000000000000000:rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs`

**Response**: Token metadata, supply, holders, trustlines, volume, price data

#### Example: $BUBBLES Token

```javascript
// Using issuer and currency hash
const issuer = 'rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs';
const currencyHex = '24425542424C4553000000000000000000000000'; // $BUBBLES
const identifier = `${currencyHex}:${issuer}`;

const response = await fetch(`https://s1.xrplmeta.org/token/${identifier}`);
const bubbles = await response.json();

console.log({
  name: bubbles.meta?.issuer?.name,
  supply: bubbles.metrics?.supply,
  holders: bubbles.metrics?.holders,
  trustlines: bubbles.metrics?.trustlines,
  price: bubbles.metrics?.price,
  volume24h: bubbles.metrics?.volume_24h
});
```

**Real $BUBBLES Response**:
```json
{
  "currency": "24425542424C4553000000000000000000000000",
  "issuer": "rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs",
  "meta": {
    "issuer": {
      "name": "XRPL Meme Bubbles",
      "domain": "xvhkir6g4okchiihofod.toml.firstledger.net",
      "kyc": true,
      "trust_level": 1
    }
  },
  "metrics": {
    "trustlines": 495,
    "holders": 296,
    "supply": "58888669.5067317",
    "marketcap": "16143.3001565096",
    "price": "0.00027413253333333",
    "volume_24h": "1.02799699999999",
    "volume_7d": "102.901752999999",
    "exchanges_24h": "1",
    "exchanges_7d": "74",
    "takers_24h": "1",
    "takers_7d": "5"
  }
}
```

#### TypeScript Example

```typescript
interface TokenMetrics {
  trustlines: number;
  holders: number;
  supply: string;
  marketcap: string;
  price: string;
  volume_24h: string;
  volume_7d: string;
  exchanges_24h: string;
  exchanges_7d: string;
  takers_24h: string;
  takers_7d: string;
}

interface TokenMeta {
  token?: {
    name?: string;
    desc?: string;
    icon?: string;
    trust_level?: number;
    urls?: Array<{url: string; type: string}>;
  };
  issuer?: {
    name?: string;
    domain?: string;
    kyc?: boolean;
    trust_level?: number;
  };
}

interface TokenData {
  currency: string;
  issuer: string;
  meta?: TokenMeta;
  metrics?: TokenMetrics;
}

async function getTokenData(currencyHex: string, issuer: string): Promise<TokenData> {
  const identifier = `${currencyHex}:${issuer}`;
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

console.log(`Token: ${bubbles.meta?.issuer?.name}`);
console.log(`Price: $${bubbles.metrics?.price}`);
console.log(`Holders: ${bubbles.metrics?.holders}`);
```

---

### 5. Get Time Series Data

```bash
GET https://s1.xrplmeta.org/token/{identifier}/series/{metric}
```

**Available metrics**: `price`, `volume`, `holders`, `trustlines`, `supply`

**Query parameters**: *Note: Series endpoint requires specific range parameters. Refer to official docs for current parameter format.*

#### Example: Token Series Request

```javascript
const issuer = 'rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs';
const currencyHex = '24425542424C4553000000000000000000000000';
const identifier = `${currencyHex}:${issuer}`;

// Series endpoint requires range parameters (sequence or time)
// Check official documentation for current parameter format
const response = await fetch(
  `https://s1.xrplmeta.org/token/${identifier}/series/price?<range_params>`
);
const seriesData = await response.json();
```

**Note**: The series endpoint documentation is evolving. For current metrics, use the main token endpoint which includes 24h and 7d aggregated data:

```javascript
const identifier = '24425542424C4553000000000000000000000000:rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs';
const response = await fetch(`https://s1.xrplmeta.org/token/${identifier}`);
const token = await response.json();

// Access aggregated metrics
console.log('24h Volume:', token.metrics.volume_24h);
console.log('7d Volume:', token.metrics.volume_7d);
console.log('24h Exchanges:', token.metrics.exchanges_24h);
console.log('24h Takers:', token.metrics.takers_24h);
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
  identifier: `${currencyHex}:${issuer}`
}));
```

#### 3. Subscribe to Token Updates

```javascript
ws.send(JSON.stringify({
  command: 'tokens_subscribe',
  identifiers: ['24425542424C4553000000000000000000000000:rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs']
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
  identifiers: ['24425542424C4553000000000000000000000000:rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs']
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
    const identifier = `${currencyHex}:${issuer}`;

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
    this.identifier = `${currencyHex}:${issuer}`;
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
        identifier = f"{currency_hex}:{issuer}"
        response = requests.get(f"{self.base_url}/token/{identifier}")
        response.raise_for_status()
        return response.json()

    def get_series(self, currency_hex, issuer, metric, range_params):
        """
        Get time series data for a token metric.

        Args:
            currency_hex: Currency code in hex format
            issuer: Issuer address
            metric: Metric to retrieve (price, volume, etc.)
            range_params: Dict with range parameters (check API docs for format)
        """
        identifier = f"{currency_hex}:{issuer}"
        response = requests.get(
            f"{self.base_url}/token/{identifier}/series/{metric}",
            params=range_params
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

print(f"Token: {bubbles.get('meta', {}).get('issuer', {}).get('name', 'Unknown')}")
print(f"Price: ${bubbles.get('metrics', {}).get('price', 0)}")
print(f"Holders: {bubbles.get('metrics', {}).get('holders', 0)}")
print(f"24h Volume: {bubbles.get('metrics', {}).get('volume_24h', 0)} XRP")
print(f"7d Volume: {bubbles.get('metrics', {}).get('volume_7d', 0)} XRP")
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
    const identifier = `${currencyHex}:${issuer}`;
    const response = await fetch(`https://s1.xrplmeta.org/token/${identifier}`);

    if (!response.ok) {
      const error = await response.json();
      if (response.status === 404) {
        throw new Error('Token not found');
      }
      if (response.status === 400) {
        throw new Error(`Invalid parameter: ${error.message}`);
      }
      throw new Error(`API error: ${response.status}`);
    }

    return await response.json();
  } catch (error) {
    console.error('Failed to fetch token:', error);
    throw error;
  }
}

// Example usage
try {
  const bubbles = await safeGetToken(
    '24425542424C4553000000000000000000000000',
    'rGUKfQ2Sm35KFSZ6BuKsjHxgyKSYgV7pzs'
  );
  console.log('Token data:', bubbles);
} catch (error) {
  console.error('Error:', error.message);
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
    // Fetch initial data and display metrics
    await this.displayMetrics();

    // Connect WebSocket for real-time updates
    this.connectWebSocket();
  }

  async fetchTokenData() {
    const identifier = `${this.currencyHex}:${this.issuer}`;
    const response = await fetch(`https://s1.xrplmeta.org/token/${identifier}`);
    const data = await response.json();

    console.log('=== $BUBBLES Token Info ===');
    console.log('Name:', data.meta?.issuer?.name);
    console.log('Supply:', data.metrics?.supply);
    console.log('Holders:', data.metrics?.holders);
    console.log('Trustlines:', data.metrics?.trustlines);
    console.log('Price:', data.metrics?.price);
    console.log('24h Volume:', data.metrics?.volume_24h);
    console.log('7d Volume:', data.metrics?.volume_7d);
    console.log('24h Exchanges:', data.metrics?.exchanges_24h);
  }

  async displayMetrics() {
    await this.fetchTokenData();
    console.log('\n=== Ready for real-time updates ===');
  }

  connectWebSocket() {
    this.ws = new WebSocket('wss://s1.xrplmeta.org');

    this.ws.onopen = () => {
      console.log('\n=== Live Updates Started ===');
      this.ws.send(JSON.stringify({
        command: 'tokens_subscribe',
        identifiers: [`${this.currencyHex}:${this.issuer}`]
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
