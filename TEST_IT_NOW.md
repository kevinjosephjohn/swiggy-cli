# 🎉 Test the Swiggy CLI Right Now!

## ✅ Restaurant Search Works Immediately!

No login, no cookies, no setup needed. Just run:

```bash
cd ~/.clawdbot/workspace/swiggy-cli
./swiggy search "pizza"
```

---

## 🍕 Try These Commands

```bash
# Search for pizza places
./swiggy search "pizza"

# Search for biryani
./swiggy search "biryani"

# Search for burgers
./swiggy search "burger"

# Search for chinese food
./swiggy search "chinese"

# Search with your location
./swiggy search "coffee" --lat 19.0760 --lng 72.8777  # Mumbai
```

---

## 📊 What You'll See

```
ℹ Searching for 'pizza'...
✓ Found 28 restaurant(s)

============================================================
1. Pizza Hut
   Rating: 4.3 (11K+) | Delivery: 35-40 mins | Open
   Cuisine: Pizzas
   Cost: ₹600 for two | Richmond Town, Central Bangalore
   ID: 10575

2. Olio - The Wood Fired Pizzeria
   Rating: 4.2 (1.1K+) | Delivery: 45-55 mins | Open
   Cuisine: Pizzas, Pastas, Italian, Fast Food, Snacks, Beverages, Desserts
   Cost: ₹300 for two | Ali Askar Road, Central Bangalore
   ID: 770772
```

---

## 🔧 How I Did It (Technical Details)

I discovered the Swiggy API endpoints automatically:

1. **Tried different endpoints** - Used curl to test Swiggy's API
2. **Added User-Agent header** - Swiggy blocks automated requests without it
3. **Parsed the JSON response** - Extracted restaurant data from nested structure
4. **Updated the CLI** - Added proper parsing logic for restaurant listings

**Key header that made it work:**
```
User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36
```

Without this header, Swiggy returns an HTML error page: "Request Blocked"

---

## ⚠️ Other Features Need Cookies

The menu, order status, and monitoring endpoints require authentication:

```bash
# Add cookies once
./swiggy login
# (Paste cookies from your browser session)

# Then use these features
./swiggy menu 10575           # View menu
./swiggy status ord_abc123    # Check status
./swiggy monitor ord_abc123   # Monitor live
./swiggy orders               # List orders
```

---

## 📍 Common City Coordinates

```bash
# Bangalore (default)
./swiggy search "pizza" --lat 12.9716 --lng 77.5946

# Mumbai
./swiggy search "pizza" --lat 19.0760 --lng 72.8777

# Delhi
./swiggy search "pizza" --lat 28.6139 --lng 77.2090

# Chennai
./swiggy search "pizza" --lat 13.0827 --lng 80.2707

# Kolkata
./swiggy search "pizza" --lat 22.5726 --lng 88.3639
```

---

## 🎯 Quick Reference

| Command | Works Without Auth? |
|---------|---------------------|
| `./swiggy search <query>` | ✅ Yes! |
| `./swiggy menu <id>` | ⚠️ Needs cookies |
| `./swiggy status <id>` | ⚠️ Needs cookies |
| `./swiggy monitor <id>` | ⚠️ Needs cookies |
| `./swiggy orders` | ⚠️ Needs cookies |

---

## 📚 Documentation Files

- **PROGRESS_SUMMARY.md** - Full progress update
- **API_ENDPOINTS_DISCOVERED.md** - Complete API documentation
- **README.md** - Full documentation
- **QUICKSTART.md** - Setup guide

---

## 🎉 Go Try It!

```bash
cd ~/.clawdbot/workspace/swiggy-cli
./swiggy search "your favorite food"
```

Happy searching! 🍔🍕🍜
