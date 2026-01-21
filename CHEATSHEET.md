# Swiggy CLI - Command Cheatsheet

Quick reference for all commands.

```bash
# Navigate to directory first
cd ~/.clawdbot/workspace/swiggy-cli

# Or if you created a symlink
swiggy <command>
```

---

## Authentication

| Command | Description |
|---------|-------------|
| `./swiggy login` | Login to Swiggy account |
| `./swiggy logout` | Logout and clear session |

---

## Restaurant Search

| Command | Description |
|---------|-------------|
| `./swiggy search <query>` | Search restaurants |
| `./swiggy search "pizza"` | Search for pizza places |
| `./swiggy search "biryani" --lat 12.9716 --lng 77.5946` | Search with custom location |

---

## Menu

| Command | Description |
|---------|-------------|
| `./swiggy menu <restaurant-id>` | Get restaurant menu |
| `./swiggy menu 12345 --lat 12.9716 --lng 77.5946` | Get menu with location |

---

## Order Management

| Command | Description |
|---------|-------------|
| `./swiggy status <order-id>` | Check order status |
| `./swiggy status ord_abc123` | Check specific order |
| `./swiggy monitor <order-id>` | Monitor order live |
| `./swiggy monitor ord_abc123 --interval 15` | Monitor with 15s interval |
| `./swiggy orders` | List all active orders |

---

## Options

| Option | Description | Default |
|--------|-------------|---------|
| `--lat` | Latitude | 12.9716 (Bangalore) |
| `--lng` | Longitude | 77.5946 (Bangalore) |
| `--interval` | Monitor update interval (seconds) | 30 |
| `-h, --help` | Show help | - |

---

## Common Coordinates

| City | Lat | Lng |
|------|-----|-----|
| Bangalore | 12.9716 | 77.5946 |
| Delhi | 28.6139 | 77.2090 |
| Mumbai | 19.0760 | 72.8777 |
| Chennai | 13.0827 | 80.2707 |
| Kolkata | 22.5726 | 88.3639 |
| Hyderabad | 17.3850 | 78.4867 |
| Pune | 18.5204 | 73.8567 |

---

## Example Workflow

```bash
# 1. Login (first time)
./swiggy login

# 2. Search for restaurants
./swiggy search "pizza near me"

# 3. Get menu of a restaurant
./swiggy menu 12345

# 4. (Manual) Place order on website, get order ID

# 5. Monitor your order
./swiggy monitor ord_abc123

# 6. Check status anytime
./swiggy status ord_abc123

# 7. List active orders
./swiggy orders
```

---

## Session Files

- `~/.swiggy-cli/session.json` - Your login session (cookies + headers)
- `~/.swiggy-cli/config.json` - Optional settings

**Keep these private!** They contain authentication tokens.
