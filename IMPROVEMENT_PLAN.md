# 🚀 Swiggy CLI v2.0 - Planned Improvements

## Inspiration from ordercli

https://github.com/steipete/ordercli

### Key Improvements to Implement

| Feature | Current Swiggy CLI | Ordercli Approach |
|----------|-------------------|-------------------|
| Authentication | Browser cookies only | OAuth2 tokens + browser cookie import |
| Project Structure | Single Python file | Multi-provider (foodora, deliveroo) |
| Config Management | Basic (session file) | Global + local config files |
| Error Messages | Generic | Specific, actionable with suggestions |
| Session Management | Save/Load only | Token refresh, cookie import |
| Reorder Feature | Not implemented | Reorder from history |
| Real-time Monitoring | Basic polling | `--watch` flag with websockets |
| CLI Structure | Single `swiggy.py` | Organized commands (orders, history, config) |
| Bot Protection | Manual workarounds | Built-in Playwright/Cloudflare handling |

---

## 🏗 New Project Structure Plan

```
swiggy-cli/
├── cmd/
│   ├── root.go              # Main entry point
│   ├── auth/               # Authentication commands
│   │   ├── login.go
│   │   ├── logout.go
│   │   └── import_cookies.go
│   ├── search/
│   │   └── restaurants.go   # Restaurant search
│   ├── orders/
│   │   ├── list.go           # List orders
│   │   ├── status.go         # Check order status
│   │   ├── show.go           # Show order details
│   │   ├── history.go         # Order history
│   │   ├── watch.go           # Real-time monitoring
│   │   └── reorder.go        # Reorder from history
│   ├── menu/
│   │   └── view.go           # View restaurant menu
│   └── config/
│       ├── get.go            # Get config value
│       ├── set.go            # Set config value
│       └── show.go           # Show all config
├── pkg/
│   ├── api/                 # API clients
│   │   ├── swiggy.go         # Swiggy API
│   │   └── client.go          # Generic HTTP client
│   ├── auth/                # Authentication logic
│   │   ├── oauth.go          # OAuth2 token management
│   │   └── session.go        # Session management
│   ├── config/              # Config file handling
│   │   └── files.go          # Load/save config files
│   └── models/              # Data models
│       ├── restaurant.go     # Restaurant data structure
│       ├── order.go          # Order data structure
│       └── menu.go           # Menu item structure
├── README.md
├── go.mod
└── go.sum
```

---

## 🔐 Authentication Improvements

### Current Implementation (Python)
```python
# Browser-based only
def login():
    phone = input("Phone: ")
    otp = input("OTP: ")
    # Manual cookie capture from DevTools
```

### New Implementation (Go - Inspired by ordercli)

```go
// OAuth2-based with browser cookie import
func Login(ctx *cli.Context) error {
    // Option 1: Browser-based (current)
    import := ctx.Bool("browser", false, "Import cookies from Chrome")
    if import {
        return ImportFromChrome(ctx)
    }

    // Option 2: OAuth2 (inspired by ordercli)
    email := ctx.String("email", "", "Email for OAuth login")
    if email != "" {
        return OAuthLogin(ctx, email)
    }
}

func OAuthLogin(ctx *cli.Context, email string) error {
    // 1. Request authorization code
    // 2. Exchange for tokens
    // 3. Save to config
    // 4. Auto-refresh tokens when expired
}

// Token refresh (like ordercli)
func RefreshTokens() error {
    // Check if access token is expired
    // Use refresh token to get new access token
    // Update config automatically
}
```

---

## 📊 Command Structure Improvements

### Current Commands
```bash
./swiggy search "pizza"
./swiggy menu 10575
./swiggy status ord_abc
./swiggy monitor ord_abc
./swiggy orders
./swiggy login
./swiggy logout
```

### New Commands (ordercli-inspired)

```bash
# Authentication
swiggy auth login --email user@example.com
swiggy auth logout
swiggy auth status
swiggy auth cookies chrome --profile "Default"  # Import from Chrome
swiggy auth session refresh  # Refresh tokens

# Restaurant Search
swiggy search "pizza" --city bangalore
swiggy search "biryani" --rating 4.0+
swiggy search "burger" --open-only  # Filter by availability

# Orders
swiggy orders list --state active
swiggy orders list --state completed
swiggy orders list --state cancelled
swiggy orders history --limit 20
swiggy orders show ORD123 --json  # Detailed JSON output
swiggy orders watch ORD123  # Real-time monitoring

# Order Operations
swiggy order status ORD123
swiggy order track ORD123  # Live tracking
swiggy order reorder ORD123 --confirm  # Reorder from history
swiggy order cancel ORD123 --confirm  # Cancel order

# Menu
swiggy menu show 10575 --veg-only
swiggy menu show 10575 --price-min 200
swiggy menu show 10575 --price-max 500

# Config
swiggy config show  # Show all config
swiggy config set location.lat 12.9716
swiggy config get location.lng
swiggy config init /path/to/config.json
```

---

## 🛠️ Bot Protection & Error Handling

### Current Approach
```python
# Basic retry with generic error
try:
    response = requests.get(url)
except Exception as e:
    print("Error:", e)
```

### New Approach (ordercli-inspired)

```go
// Cloudflare/bot detection handling
func GetWithRetry(url string) (*http.Response, error) {
    var resp *http.Response
    var err error

    for i := 0; i < 3; i++ {
        resp, err = http.Get(url)
        if err != nil {
            // Check if Cloudflare challenge
            if strings.Contains(resp.Body, "Cloudflare") {
                // Use Playwright to solve
                return SolveCloudflare(url)
            }
            // Check if rate limited
            if resp.StatusCode == 429 {
                time.Sleep(time.Second * 5)  // Backoff
                continue
            }
            return resp, nil
        }

        // Check if bot detected
        if resp.StatusCode == 403 {
            return nil, fmt.Errorf("bot detected - try browser-based auth")
        }

        return resp, nil
    }
}

// Better error messages (inspired by ordercli)
func PrintAPIError(err error, action string) {
    if strings.Contains(err.Error(), "401") {
        fmt.Printf("❌ Authentication failed. Run: swiggy auth login")
    } else if strings.Contains(err.Error(), "403") {
        fmt.Printf("❌ Access denied. Try: swiggy auth cookies chrome")
    } else if strings.Contains(err.Error(), "429") {
        fmt.Printf("⚠️  Rate limited. Wait 30 seconds and retry")
    } else if strings.Contains(err.Error(), "timeout") {
        fmt.Printf("⚠️  Request timeout. Check your connection")
    } else {
        fmt.Printf("❌ %s: %v", action, err)
    }
}
```

---

## 🔃 Session & Config Management

### Current (Python)
```python
# Single session file
SESSION_FILE = "~/.swiggy-cli/session.json"

def load_session():
    with open(SESSION_FILE) as f:
        return json.load(f)

def save_session(data):
    with open(SESSION_FILE, 'w') as f:
        json.dump(data, f)
```

### New (Go - ordercli-inspired)

```go
// Config file locations (like ordercli)
const (
    GlobalConfigDir  = "~/.config/swiggy-cli/"
    LocalConfigFile  = "./swiggy.json"
)

type Config struct {
    Auth     AuthConfig     `json:"auth"`
    Location LocationConfig `json:"location"`
    API      APIConfig      `json:"api"`
    Client   ClientConfig   `json:"client"`
}

type AuthConfig struct {
    AccessToken  string `json:"access_token"`
    RefreshToken string `json:"refresh_token"`
    ExpiresAt    int64  `json:"expires_at"`
    ClientID     string `json:"client_id"`
}

type LocationConfig struct {
    Lat  string `json:"lat"`
    Lng  string `json:"lng"`
    City string `json:"city"`
    Address string `json:"address"`
}

// Load from global config, override with local config
func LoadConfig() (*Config, error) {
    cfg, _ := LoadGlobalConfig()  // Load from ~/.config/swiggy-cli/
    localCfg, _ := LoadLocalConfig()    // Load from ./swiggy.json
    return MergeConfigs(cfg, localCfg)
}

// Save config (like ordercli's config set)
func SaveConfig(cfg *Config) error {
    SaveToGlobalConfig(cfg)
    return SaveLocalConfig(cfg)
}
```

---

## 📡 Real-time Monitoring

### Current (Python)
```python
def monitor_order(order_id, interval=30):
    while True:
        status = get_order_status(order_id)
        print(f"Status: {status}")
        time.sleep(interval)
```

### New (ordercli-inspired)

```go
// WebSocket or long-polling with better UX (like ordercli --watch)
func WatchOrder(ctx *cli.Context, orderID string) error {
    ticker := time.NewTicker(5 * time.Second)

    // Display loading spinner while waiting
    spinner := NewSpinner("Connecting...")

    for {
        select {
        case <-ticker.C:
            spinner.Update()

            status, err := GetOrderStatus(orderID)
            if err != nil {
                return err
            }

            // Clear spinner when data arrives
            spinner.Stop()

            // Color-coded status (like ordercli)
            switch status.State {
            case "CONFIRMED":
                PrintGreen("✓ Order confirmed")
            case "PREPARING":
                PrintYellow("⏳ Preparing")
            case "OUT_FOR_DELIVERY":
                PrintBlue("🚗 Out for delivery")
            case "DELIVERED":
                PrintGreen("✓ Delivered")
                return nil
            }

        case <-ctx.Done():
            return ctx.Err()
        }
    }
}
```

---

## 📦 Go vs Python Decision

### Current: Python
✅ Pros:
- Quick to prototype
- Many libraries available
- Easy to read and modify
- No compilation step

❌ Cons:
- Slower runtime
- Harder to distribute (needs Python installed)
- Version management complexity

### New: Go (ordercli-inspired)

✅ Pros:
- Single binary distribution (no Python needed)
- Faster execution
- Better concurrency support
- Easier deployment
- Type safety

❌ Cons:
- Longer development time
- More verbose code
- Need Go toolchain

---

## 🎯 Implementation Priority (Based on ordercli)

### Phase 1: Migration to Go (Week 2-3)
- [ ] Set up Go project structure
- [ ] Implement config management system
- [ ] Port search functionality
- [ ] Port authentication (browser + OAuth)
- [ ] Add better error messages

### Phase 2: Enhanced Orders (Week 4-5)
- [ ] Implement orders list with filters
- [ ] Implement order show with JSON output
- [ ] Implement order history
- [ ] Implement watch command (real-time monitoring)
- [ ] Implement reorder functionality
- [ ] Add order cancellation

### Phase 3: Menu Improvements (Week 6-7)
- [ ] Fix menu API authentication issues
- [ ] Add filtering options (veg, price range)
- [ ] Add menu item search
- [ ] Implement menu caching
- [ ] Add favorite items

### Phase 4: Advanced Features (Week 8+)
- [ ] Add multiple location support
- [ ] Add order sharing
- [ ] Add price comparisons
- [ ] Add notifications (desktop, push)
- [ ] Add export functionality (CSV, PDF)

---

## 📊 Comparison: Current vs Ordercli

| Feature | Swiggy CLI (Current) | Ordercli (Reference) |
|---------|----------------------|--------------------|
| Language | Python | Go |
| Auth Method | Browser cookies only | OAuth2 + browser cookies |
| Commands | Basic (6 commands) | Organized (30+ commands) |
| Config | Single file | Global + local files |
| Error Handling | Generic | Specific, actionable |
| Bot Protection | Manual | Built-in (Playwright) |
| Session Mgmt | Save/Load only | Token refresh + cookie import |
| Real-time | Basic polling | Watch with WebSocket/polling |
| History | Not implemented | Full history management |
| Reorder | Not implemented | One-command reorder |
| Distribution | Script + requirements.txt | Single binary |
| Rate Limiting | None | Auto-retry with backoff |

---

## 💡 Key Learnings from ordercli

1. **Provider abstraction** - Separate foodora/deliveroo implementations allows multiple providers
2. **Command structure** - Grouped commands (auth/, orders/, menu/) makes code maintainable
3. **Config priorities** - Global config overridden by local config allows system-wide defaults
4. **Better UX** - Loading spinners, color-coded output, specific error messages
5. **Cookie import** - `auth cookies chrome` is a great pattern for browser-based auth
6. **Watch command** - `orders --watch` provides real-time feedback better than manual polling
7. **JSON output** - `--json` flag enables integration with other tools
8. **Token refresh** - Auto-refresh tokens prevents manual re-login

---

## 🚀 Next Steps

### Immediate (This Week)
1. Create Go project structure
2. Port existing search functionality to Go
3. Implement OAuth2 authentication (browser import option)
4. Add better error messages inspired by ordercli

### Short-term (Next 2-3 Weeks)
1. Implement orders list/history with filters
2. Implement watch command for real-time monitoring
3. Add config management system
4. Test all existing features in Go version

### Long-term (Next 1-2 Months)
1. Implement reorder functionality
2. Add menu filtering and search
3. Add multiple provider support (for other food delivery)
4. Create single binary distribution

---

## 📝 Notes

- Ordercli uses Go and is much more mature than current Swiggy CLI
- Current Python CLI is functional for restaurant search and basic auth
- Migration to Go would provide better distribution, performance, and maintainability
- Pattern from ordercli can be directly applied while staying compatible with Swiggy APIs

---

## 🎯 Success Metrics (After Go Migration)

| Metric | Target |
|---------|--------|
| Commands organized | 30+ grouped commands |
| Error messages | 90% specific with suggestions |
| Session management | Auto-refresh + import |
| Real-time features | WebSocket or smart polling |
| Distribution | Single binary, no dependencies |
| Code maintainability | Modular with clear separation |

---

**Inspired by:** https://github.com/steipete/ordercli
**Last Updated:** January21,2026
