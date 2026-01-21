# Swiggy CLI

A CLI tool for monitoring Swiggy orders and searching restaurants via unofficial API.

**Current Versions:**
- `swiggy.py` (v1.0) - Basic browser cookie auth
- `swiggy_v2.py` (v2.0) - **Recommended** - Auth token extraction from API

**Note:** v2.0 automatically extracts auth tokens from API responses - no manual DevTools needed!

## Installation

```bash
# Clone or navigate to the project
cd swiggy-cli

# Setup Python virtual environment
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

Or use the wrapper script (auto-manages venv):
```bash
./swiggy --help
```

## Usage

### Login

```bash
./swiggy login
# Prompts for phone number/email and OTP
# Saves session to ~/.swiggy-cli/session.json
```

### Search Restaurants

```bash
./swiggy search "pizza"
./swiggy search "biryani" --lat 12.9716 --lng 77.5946
```

**Output includes:**
- Restaurant name
- Rating and review count
- Delivery time
- Cuisine types
- Cost for two people
- Location
- Open/Closed status

### View Menu

```bash
./swiggy menu <restaurant-id>
```

**Note:** Menu requires authentication cookies from browser session.

### Order Status

```bash
./swiggy status <order-id>
```

### Monitor Order Live

```bash
./swiggy monitor <order-id> --interval 30
# Updates every 30 seconds (default)
# Press Ctrl+C to stop
```

### List Active Orders

```bash
./swiggy orders
```

## Features

| Feature | Status | Authentication |
|----------|----------|---------------|
| Restaurant Search | ✅ Working | None required |
| Restaurant Menu | ⚠️ Requires cookies | Browser cookies needed |
| Order Status | ⚠️ Requires cookies | Browser cookies needed |
| Order Monitoring | ⚠️ Requires cookies | Browser cookies needed |
| Active Orders | ⚠️ Requires cookies | Browser cookies needed |

## API Endpoints

Swiggy's unofficial API endpoints used:

| Endpoint | URL | Auth Required |
|----------|-----|---------------|
| Search | `/dapi/restaurants/list/v5` | No |
| Menu | `/dapi/menu/pl` | Yes |
| Order Status | `/dapi/orders/{id}` | Yes |
| Orders List | `/dapi/orders/list` | Yes |

## Authentication

The CLI supports cookie-based authentication:

1. Log in to Swiggy in browser
2. Open DevTools (F12) → Network tab
3. Make any request (search or open restaurant)
4. Copy `Cookie:` header from Request Headers
5. Run: `./swiggy login`
6. Paste cookies when prompted

Session is saved to `~/.swiggy-cli/session.json`

## Configuration

| Setting | Location | Default |
|----------|----------|----------|
| Session file | `~/.swiggy-cli/session.json` | Auto-created |
| Config file | `~/.swiggy-cli/config.json` | Optional |
| Default Lat/Lng | Bangalore | `12.9716`, `77.5946` |

## Project Structure

```
swiggy-cli/
├── swiggy              # Wrapper script (auto venv)
├── swiggy.py           # Main CLI application
├── requirements.txt      # Python dependencies
├── README.md           # Full documentation
├── QUICKSTART.md       # Quick start guide
├── CHEATSHEET.md       # Command reference
├── API_INVESTIGATION.md  # API analysis
├── LOGIN_COMPLETE.md   # Login status
└── API_ENDPOINTS_DISCOVERED.md  # API documentation
```

## Development

To extend or modify:

```bash
cd swiggy-cli
source venv/bin/activate  # Activate virtual env
# Edit swiggy.py
# Test changes: ./swiggy search "test"
```

## Troubleshooting

### "Module not found: requests"
```bash
./swiggy  # Wrapper will auto-install dependencies
# Or manually:
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### "Login failed: HTTP 401/403"
Session expired or invalid cookies. Re-run:
```bash
./swiggy login
```

### "Search returns no results"
- Check location coordinates (use --lat --lng)
- Try different search terms
- Verify your area has Swiggy coverage

## Notes

- Uses unofficial Swiggy APIs (may change without notice)
- Cookie-based authentication (expires periodically)
- Restaurant search works without authentication
- Menu/orders require browser session cookies
- Tested on macOS with Python 3.7+

## License

MIT License - feel free to use and modify!
