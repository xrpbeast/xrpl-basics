# Prerequisites

Install Node.js, npm, and VS Code before proceeding.

> Skip if you already have these tools installed.

## 1. Node.js & npm

### Download
Visit [nodejs.org](https://nodejs.org/) and download the **LTS** version (recommended for stability).

### Install

**Windows:**
```bash
# Run the .msi installer, keep defaults
# Check "automatically install necessary tools" when prompted
node -v && npm -v  # verify in Command Prompt
```

**macOS:**
```bash
# Run the .pkg installer, keep defaults
node -v && npm -v  # verify in Terminal
```

**Linux (Ubuntu):**
```bash
sudo apt update
sudo apt install nodejs npm
node -v && npm -v  # verify
```

## 2. Visual Studio Code

### Download
Visit [code.visualstudio.com](https://code.visualstudio.com/) and download for your OS.

### Install

**Windows:** Run `.exe` installer, keep defaults

**macOS:** Unzip, drag to Applications folder

**Linux (Ubuntu):**
```bash
sudo apt update
sudo apt install code
# or download .deb from website
```

## Verify Setup

```bash
node -v   # should show version (e.g., v20.x.x)
npm -v    # should show version (e.g., 10.x.x)
code -v   # should show VS Code version
```

Ready to proceed to [Hello World](./02-hello-world.md).
