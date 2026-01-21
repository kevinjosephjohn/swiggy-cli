# API Capture Guide for Swiggy

This guide helps you capture the actual API endpoints from Swiggy's website to make the CLI work.

## Step-by-Step Instructions

### 1. Open Developer Tools

**Chrome/Edge:**
- Press `F12` or `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Windows/Linux)
- Or right-click anywhere → Inspect

**Firefox:**
- Press `F12` or `Cmd+Option+I` (Mac) / `Ctrl+Shift+I` (Windows/Linux)
- Or right-click → Inspect Element

**Safari:**
- Enable Develop menu: Safari → Settings → Advanced → Show Develop menu
- Press `Cmd+Option+I`

### 2. Go to Network Tab

In DevTools:
1. Click on the **Network** tab
2. Filter by **Fetch/XHR** (this shows only API requests)
3. Keep this tab open

### 3. Login to Swiggy

1. Go to https://www.swiggy.com
2. Log in with your account
3. Watch the Network tab - you'll see API calls

### 4. Capture Authentication

Look for requests that return authentication data:

**What to look for:**
- Request URLs containing: `/auth/`, `/login/`, `/otp/`
- Response containing tokens, user ID, session ID

**Example request:**
```
URL: https://www.swiggy.com/dapi/auth/login
Method: POST
Response: { "data": { "userId": "...", "token": "..." } }
```

**What to copy:**
- The **Cookie** header from Request Headers (right-click → Copy → Copy as cURL)
- Any `Authorization` header if present

### 5. Capture Restaurant Search

1. Type a search query on Swiggy (e.g., "pizza")
2. Look for the request that returns restaurant results

**What to look for:**
- URL containing: `/restaurants/`, `/search/`
- Response containing list of restaurants with IDs, names, ratings

**Example:**
```
URL: https://www.swiggy.com/dapi/restaurants/list/v5?lat=12.97&lng=77.59&search=pizza
Method: GET
Response: { "data": { "cards": [...] } }
```

**Update in swiggy.py:**
- Update the `url` in `search_restaurants()` method
- Update response parsing logic to match actual structure

### 6. Capture Menu Data

1. Click on a restaurant
2. Look for the request that loads the menu

**What to look for:**
- URL containing: `/menu/`, `restaurant-menu-id`
- Response containing items with IDs, names, prices

**Example:**
```
URL: https://www.swiggy.com/dapi/menu/pl?lat=12.97&lng=77.59&restaurant-menu-id=12345
Method: GET
Response: { "data": { "items": [...] } }
```

**Update in swiggy.py:**
- Update the `url` in `get_menu()` method
- Update item parsing logic

### 7. Capture Order Status

1. Go to Orders section
2. Click on an active order
3. Look for status updates

**What to look for:**
- URL containing: `/orders/`, `/status/`
- Response containing status, ETA, delivery partner info

**Example:**
```
URL: https://www.swiggy.com/dapi/orders/ord_abc123
Method: GET
Response: { "data": { "status": "cooking", "eta": "20 mins" } }
```

**Update in swiggy.py:**
- Update `url` in `get_order_status()` method
- Update status parsing

### 8. (Optional) Capture Order Placement

⚠️ **This is sensitive - only capture for understanding, don't actually place orders during testing**

1. Add items to cart
2. Proceed to checkout (don't complete payment)
3. Look for the "place order" request

**What to look for:**
- URL containing: `/checkout/`, `/place-order/`
- Request body containing items, address, payment method

**Note:** This endpoint may require additional security tokens, CSRF protection, etc.

## Copying Request Details

### Method 1: Copy as cURL (Recommended)

1. Right-click on a request in Network tab
2. Select **Copy** → **Copy as cURL**
3. Paste into a file or text editor

The cURL command contains:
- Full URL
- All headers (cookies, auth tokens)
- Request body (if POST)

### Method 2: Copy Request Headers

1. Click on a request
2. Go to **Headers** tab
3. Scroll down to **Request Headers**
4. Copy relevant headers (Cookie, Authorization)

### Method 3: Export as HAR

1. Right-click on Network tab
2. Select **Save all as HAR with content**
3. This saves all network traffic to analyze later

## Updating swiggy.py

After capturing endpoints, update the corresponding values in `swiggy.py`:

```python
# Example - Update search endpoint
def search_restaurants(self, query, lat=None, lng=None):
    url = "https://www.swiggy.com/dapi/restaurants/list/v5"  # Updated
    params = {
        "lat": lat or "12.9716",
        "lng": lng or "77.5946",
        "search": query
    }
    # ... rest of code
```

## Testing Captured Endpoints

Use curl to test captured endpoints:

```bash
# Example - test restaurant search
curl "https://www.swiggy.com/dapi/restaurants/list/v5?lat=12.9716&lng=77.5946&search=pizza" \
  -H "Cookie: YOUR_COPIED_COOKIE_HERE" \
  -H "User-Agent: Mozilla/5.0 ..."
```

If the curl command works, the endpoint is correct and ready to use in the CLI.

## Common API Patterns

### Swiggy API Base
- Production: `https://www.swiggy.com/dapi`
- Sometimes: `https://www.swiggy.com/mapi` (mobile API)

### Common Query Params
- `lat`, `lng` - Location coordinates
- `tracking` - Usually "null"
- `is-seo-menu-page` - For restaurant menus
- `restaurant-menu-id` - Restaurant ID for menu

### Common Headers
- `Cookie` - Session cookies
- `User-Agent` - Browser identifier
- `Referer` - https://www.swiggy.com/
- `x-device-id` - Device identifier (sometimes needed)

## Tips

1. **Clear Network Tab** - Click the 🚫 icon to clear previous requests
2. **Preserve Log** - Check "Preserve log" to capture redirects
3. **Slow 3G** - Simulate slow network to see all requests
4. **Export HAR** - Save all traffic for later analysis
5. **Use Search** - Filter Network tab by typing keywords

## Next Steps

Once you have the endpoints:
1. Update `swiggy.py` with correct URLs
2. Test with captured cookies
3. Adjust parsing logic based on actual response structure
4. Improve error handling for API changes

Happy API hunting! 🕵️‍♂️
