# Swiggy CLI - Quick Start Guide

Get started with the Swiggy CLI in 3 easy steps!

## 🚀 Quick Start

### 1. Navigate to the directory

```bash
cd ~/.clawdbot/workspace/swiggy-cli
```

### 2. Login (first time only)

```bash
./swiggy login
```

You'll be asked to:
- Enter your email or phone
- Capture your Swiggy cookies from the browser (see below)

### 3. Start using it!

```bash
./swiggy search "pizza"        # Search restaurants
./swiggy menu <restaurant-id>   # View menu
./swiggy status <order-id>      # Check order status
./swiggy monitor <order-id>     # Watch order live
./swiggy orders                 # List active orders
```

---

## 📋 How to Get Your Swiggy Cookies

You only need to do this once!

### Step 1: Open Swiggy in your browser
Go to https://www.swiggy.com

### Step 2: Open Developer Tools
- **Chrome/Edge**: Press `F12` or `Cmd+Option+I`
- **Firefox**: Press `F12` or `Cmd+Option+I`
- **Safari**: Cmd+Option+I (enable Develop menu first in Settings)

### Step 3: Go to Network tab
1. Click on the **Network** tab
2. Filter by **Fetch/XHR** (click the filter button)
3. Click the 🚫 icon to clear previous requests

### Step 4: Log in to Swiggy
- Log into your Swiggy account in the browser
- Watch the Network tab - you'll see API requests

### Step 5: Copy the Cookie header
1. Click on any of the requests (look for one with "swiggy.com")
2. Go to the **Headers** tab
3. Scroll down to **Request Headers**
4. Find the `Cookie:` line
5. Copy everything after `Cookie:` (right-click → Copy)

### Step 6: Paste into the CLI
When the `./swiggy login` command asks for cookies, paste them!

That's it! Your session is now saved for future use.

---

## 📍 Setting Your Location

By default, it uses Bangalore coordinates. To use your location:

**Option 1: Pass with every command**
```bash
./swiggy search "pizza" --lat 28.6139 --lng 77.2090
```

**Option 2: Find your coordinates**
1. Go to Google Maps
2. Right-click on your location
3. Copy the coordinates at the bottom

---

## 🎯 Common Commands

| Command | Description | Example |
|---------|-------------|---------|
| `search` | Find restaurants | `./swiggy search "biryani"` |
| `menu` | View restaurant menu | `./swiggy menu 12345` |
| `status` | Check order status | `./swiggy status ord_abc123` |
| `monitor` | Watch order live | `./swiggy monitor ord_abc123` |
| `orders` | List active orders | `./swiggy orders` |
| `logout` | Clear session | `./swiggy logout` |

---

## 🐛 Troubleshooting

### "ModuleNotFoundError: No module named 'requests'"
Run the command again - the wrapper will auto-install dependencies.

### "Login failed: HTTP 401/403"
Your session expired. Run `./swiggy logout` then `./swiggy login` again.

### "No search results found"
- Try different search terms
- Check your location coordinates
- Make sure you're logged in

### Cookies don't work
- Ensure you copied the FULL Cookie header value
- Make sure you're logged into Swiggy in the browser
- Try capturing cookies from a different request in the Network tab

---

## 💡 Tips

1. **Create a symlink** for easy access:
   ```bash
   sudo ln -s ~/.clawdbot/workspace/swiggy-cli/swiggy /usr/local/bin/swiggy
   ```
   Then use `swiggy` from anywhere!

2. **Add to PATH** instead (if you don't have sudo):
   ```bash
   echo 'export PATH="$HOME/.clawdbot/workspace/swiggy-cli:$PATH"' >> ~/.zshrc
   source ~/.zshrc
   ```

3. **Check your location** - Use Google Maps to get precise coordinates for better results

---

## ⚠️ Important Notes

- This uses **unofficial APIs** - Swiggy may change them at any time
- Session tokens expire - you may need to re-login periodically
- Store your `~/.swiggy-cli/session.json` securely - it contains auth tokens
- Use at your own risk!

---

## 📚 More Documentation

- Full documentation: `README.md`
- API capture guide: `API_CAPTURE_GUIDE.md`

Happy ordering! 🍕🍔🍜
