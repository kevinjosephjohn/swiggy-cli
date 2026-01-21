# 📸 Swiggy API Capture - Manual Guide

Follow these steps to capture the Swiggy APIs yourself. This will make the CLI fully functional.

---

## 🎯 What You'll Capture

We need these 4 key API endpoints:

| # | Endpoint | Purpose |
|---|----------|---------|
| 1 | Restaurant Search | Find restaurants by query |
| 2 | Menu Data | Get restaurant menu items |
| 3 | Order Status | Check order status |
| 4 | Active Orders | List all active orders |

---

## 📋 Step-by-Step Guide

### Step 1: Open Developer Tools

**Chrome/Edge:**
1. Press `F12` or `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Windows)
2. Click on the **Network** tab
3. Click the **Fetch/XHR** filter button (this shows only API calls)
4. Click the 🚫 icon to clear previous requests
5. Check **"Preserve log"** (keeps logs during page reloads)

### Step 2: Open Swiggy

1. Go to https://www.swiggy.com
2. Log in to your account (important!)
3. Set your location (click "Set location" at top)

### Step 3: Capture Restaurant Search API

1. In the search bar on Swiggy, type something like "pizza"
2. Press Enter
3. **Watch the Network tab** - you'll see new requests appear

**Find this request:**
- Look for a request with URL containing: `/restaurants/list/` or `/search/`
- It should have query params like `lat`, `lng`, `search`

**What to copy:**
1. Click on that request
2. Go to **Headers** tab
3. Copy the **Request URL** (right-click → Copy → Copy link address)
4. Copy the **Request Headers** section (right-click → Copy → Copy as cURL)
5. Click on **Preview** tab and look at the response structure

**Example format you should see:**
```
URL: https://www.swiggy.com/dapi/restaurants/list/v5?lat=12.9716&lng=77.5946&search=pizza
Method: GET
Response: { "data": { "cards": [...] } }
```

**Paste these into the form below:**
```
SEARCH_URL: [paste here]
SEARCH_CURL: [paste here]
SEARCH_RESPONSE_STRUCTURE: [briefly describe - e.g., "restaurants are in data.cards array"]
```

---

### Step 4: Capture Menu API

1. Click on any restaurant from the search results
2. **Watch Network tab** - new requests appear

**Find this request:**
- URL containing: `/menu/` or `restaurant-menu-id`

**What to copy:**
1. Click on that request
2. Copy the **Request URL**
3. Copy the **Request Headers** (as cURL)
4. Note the response structure

**Example format:**
```
URL: https://www.swiggy.com/dapi/menu/pl?lat=12.9716&lng=77.5946&restaurant-menu-id=12345
Method: GET
Response: { "data": { "items": [...] } }
```

**Paste these into the form below:**
```
MENU_URL: [paste here]
MENU_CURL: [paste here]
MENU_RESPONSE_STRUCTURE: [describe structure]
```

---

### Step 5: Capture Order Status API

1. Click on the **Orders** link in Swiggy (top right → Orders)
2. Click on an **active order** (if you have one)
3. **Watch Network tab**

**Find this request:**
- URL containing: `/orders/` or `/status/`

**What to copy:**
1. Copy the **Request URL**
2. Copy the **Request Headers**
3. Note the response structure

**Example format:**
```
URL: https://www.swiggy.com/dapi/orders/ord_abc123?lat=12.9716&lng=77.5946
Method: GET
Response: { "data": { "status": "cooking", "eta": "20 mins" } }
```

**Paste these into the form below:**
```
STATUS_URL: [paste here]
STATUS_CURL: [paste here]
STATUS_RESPONSE_STRUCTURE: [describe structure]
```

---

### Step 6: Capture Active Orders API

1. While still on the Orders page
2. Watch for requests that load the orders list

**Find this request:**
- URL containing: `/orders/list` or similar

**What to copy:**
1. Copy the **Request URL**
2. Copy the **Request Headers**
3. Note the response structure

**Example format:**
```
URL: https://www.swiggy.com/dapi/orders/list?lat=12.9716&lng=77.5946
Method: GET
Response: { "data": { "orders": [...] } }
```

**Paste these into the form below:**
```
ORDERS_URL: [paste here]
ORDERS_CURL: [paste here]
ORDERS_RESPONSE_STRUCTURE: [describe structure]
```

---

### Step 7: Copy Authentication Cookies

**You need the Cookie header from any of the above requests:**

1. Click on any request you captured
2. Go to **Headers** tab
3. Scroll down to **Request Headers**
4. Find the line that starts with `Cookie:`
5. Copy everything after `Cookie:` (right-click → Copy)

**Note:** The Cookie value will be long - that's normal!

**Paste this into the form below:**
```
COOKIE_HEADER: [paste here]
```

---

## 📝 Submit Your Findings

Copy the template below and fill it with your captured data:

```
=== SWIGGY API CAPTURE RESULTS ===

[STEP 3 - RESTAURANT SEARCH]
SEARCH_URL: 
SEARCH_CURL: 
SEARCH_RESPONSE_STRUCTURE: 

[STEP 4 - MENU]
MENU_URL: 
MENU_CURL: 
MENU_RESPONSE_STRUCTURE: 

[STEP 5 - ORDER STATUS]
STATUS_URL: 
STATUS_CURL: 
STATUS_RESPONSE_STRUCTURE: 

[STEP 6 - ACTIVE ORDERS]
ORDERS_URL: 
ORDERS_CURL: 
ORDERS_RESPONSE_STRUCTURE: 

[STEP 7 - AUTHENTICATION]
COOKIE_HEADER: 

[LOCATION]
YOUR_LATITUDE: 
YOUR_LONGITUDE: 
```

**Send this back to me** and I'll update the CLI with working APIs!

---

## 💡 Tips

1. **If you don't have an active order**, you can place a test order (small amount, cancel if needed) to capture the status API.

2. **Location matters** - Make sure you set your location on Swiggy before capturing. Note your coordinates (visible in the URL params).

3. **Keep Network tab open** - Don't close it until you've captured all endpoints.

4. **Copy as cURL** is best - It includes all headers and parameters.

5. **Preview tab** shows the response structure - just describe it briefly (e.g., "restaurants in data.cards array with name, id, rating fields").

---

## ❓ Troubleshooting

**"I don't see any requests in Network tab"**
- Make sure you clicked "Fetch/XHR" filter
- Try reloading the page
- Make sure "Preserve log" is checked

**"The request shows no response"**
- That's okay - just copy the URL and headers
- The CLI will send the same request

**"I can't find the request"
- Use the search box in Network tab to filter by "restaurants", "menu", "orders"
- Look for requests to swiggy.com domain

**"I'm not logged in"**
- Log into Swiggy first, then capture the requests
- The Cookie header won't work without being logged in

---

## 🎯 Once You Have the Data

Send me the filled template above and I'll:
1. Update `swiggy.py` with the correct endpoints
2. Update response parsing logic
3. Test with your captured cookies
4. Confirm everything works!

Happy API hunting! 🕵️‍♂️
