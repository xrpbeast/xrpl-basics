# Hello World

Connect to the XRP Ledger and fetch the latest validated ledger.

## Setup

```bash
mkdir xrpl-hello && cd xrpl-hello
npm init -y
npm install xrpl
```

## Code

Create `app.js`:

```javascript
const xrpl = require("xrpl");

const displayLastLedgerIndex = async () => {
  const client = new xrpl.Client("wss://xrplcluster.com");
  await client.connect();

  const ledgerInfo = await client.request({
    command: "ledger",
    ledger_index: "validated",
  });

  console.log(
    `Hello world from the XRP ledger, the last index was: ${ledgerInfo.result.ledger_index}`
  );

  await client.disconnect();
};

displayLastLedgerIndex();
```

## Run

```bash
node app.js
```

Expected output:
```
Hello world from the XRP ledger, the last index was: 85234567
```

## Code Breakdown

| Line | Purpose |
|------|---------|
| `require("xrpl")` | Import the xrpl.js library |
| `new xrpl.Client(url)` | Create client instance with WebSocket endpoint |
| `client.connect()` | Establish connection to XRPL node |
| `client.request({...})` | Send a command to the ledger |
| `command: "ledger"` | Request ledger information |
| `ledger_index: "validated"` | Get the latest validated (finalized) ledger |
| `client.disconnect()` | Close the connection |

## Public Endpoints

| Network | WebSocket URL |
|---------|---------------|
| Mainnet | `wss://xrplcluster.com` |
| Mainnet | `wss://s1.ripple.com` |
| Testnet | `wss://s.altnet.rippletest.net:51233` |
| Devnet | `wss://s.devnet.rippletest.net:51233` |
