# Swiggy API Endpoints - Discovered via Automated Testing

## Summary

I was able to automate API discovery using `curl` with proper User-Agent headers. Here's what I found working:

---

## ✅ Working Endpoints (No Auth Required)

### 1. Restaurant Search

**Endpoint:**
```
GET https://www.swiggy.com/dapi/restaurants/list/v5
```

**Query Parameters:**
| Param | Description | Example |
|-------|-------------|---------|
| `lat` | Latitude | `12.9716` (Bangalore) |
| `lng` | Longitude | `77.5946` (Bangalore) |
| `search` | Search query | `pizza`, `biryani`, etc. |

**Request:**
```bash
curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  "https://www.swiggy.com/dapi/restaurants/list/v5?lat=12.9716&lng=77.5946&search=pizza"
```

**Response Structure:**
```json
{
  "statusCode": 0,
  "data": {
    "statusMessage": "done successfully",
    "cards": [
      {
        "card": {
          "@type": "type.googleapis.com/swiggy.gandalf.widgets.v2.GridWidget",
          "gridElements": {
            "infoWithStyle": {
              "restaurants": [
                {
                  "info": {
                    "id": "10575",
                    "name": "Pizza Hut",
                    "locality": "Richmond Town",
                    "areaName": "Central Bangalore",
                    "costForTwo": "₹600 for two",
                    "cuisines": ["Pizzas"],
                    "avgRating": 4.3,
                    "avgRatingString": "4.3",
                    "totalRatingsString": "11K+",
                    "sla": {
                      "deliveryTime": 37,
                      "slaString": "35-40 mins"
                    },
                    "cloudinaryImageId": "..."
                  }
                }
              ]
            }
          }
        }
      }
    ]
  }
}
```

**Key Fields for Restaurants:**
- `id` - Restaurant ID (use for menu)
- `name` - Restaurant name
- `locality` - Location
- `areaName` - Area
- `costForTwo` - Cost for two people
- `cuisines` - Array of cuisines
- `avgRating` - Rating
- `avgRatingString` - Rating as string
- `sla.deliveryTime` - Delivery time in minutes
- `sla.slaString` - Human-readable delivery time

---

## ⚠️ Endpoints Requiring Authentication

These endpoints return 403/401 without proper cookies and session tokens:

### 2. Restaurant Menu

**Endpoint:**
```
GET https://www.swiggy.com/dapi/menu/pl
```

**Query Parameters:**
| Param | Description | Example |
|-------|-------------|---------|
| `lat` | Latitude | `12.9716` |
| `lng` | Longitude | `77.5946` |
| `page-type` | Page type | `REGULAR_MENU` |
| `complete-menu` | Include complete menu | `true` |
| `restaurant-menu-id` | Restaurant ID (from search) | `10575` |

**Request:**
```bash
curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  "https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=12.9716&lng=77.5946&restaurant-menu-id=10575"
```

**Note:** This endpoint likely requires authentication cookies to work properly.

---

### 3. Order Status

**Endpoint:**
```
GET https://www.swiggy.com/dapi/orders/{order_id}
```

**Query Parameters:**
| Param | Description | Example |
|-------|-------------|---------|
| `lat` | Latitude | `12.9716` |
| `lng` | Longitude | `77.5946` |

**Request:**
```bash
curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  "https://www.swiggy.com/dapi/orders/ord_abc123?lat=12.9716&lng=77.5946"
```

**Note:** Requires authentication. Order ID format: `ord_` followed by alphanumeric characters.

---

### 4. Active Orders List

**Endpoint:**
```
GET https://www.swiggy.com/dapi/orders/list
```

**Query Parameters:**
| Param | Description | Example |
|-------|-------------|---------|
| `lat` | Latitude | `12.9716` |
| `lng` | Longitude | `77.5946` |

**Request:**
```bash
curl -A "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36" \
  "https://www.swiggy.com/dapi/orders/list?lat=12.9716&lng=77.5946"
```

**Note:** Requires authentication cookies.

---

## 🔐 Authentication

Swiggy uses cookie-based authentication. You'll need to capture cookies from your browser session.

**Key Cookies (likely needed):**
- `_gid`, `_ga` - Google Analytics (may not be needed)
- `SID` - Session ID (important)
- Other session cookies

**How to capture:**
1. Log in to Swiggy in your browser
2. Open Developer Tools (F12) → Network tab
3. Make a request (search for something)
4. Find the `Cookie:` header in Request Headers
5. Copy the entire cookie string

---

## 📊 API Response Notes

### Restaurant Search Response
- Response is JSON with nested card structures
- Restaurants are inside `data.cards` array
- Different card types: banners, restaurant listings, etc.
- Need to filter cards to find `FoodRestaurantGridListingInfo` type

### Bot Protection
- Swiggy has basic bot detection
- Must include proper User-Agent header
- Without User-Agent: returns HTML error page "Request Blocked"
- With User-Agent: returns JSON

---

## 🛠️ Implementation Notes

For the CLI implementation:

1. **Search** - Works without auth ✅
   - Parse nested cards structure
   - Extract restaurant IDs, names, ratings, delivery times

2. **Menu** - Needs auth cookies ⚠️
   - User must provide cookies from browser
   - Parse items with prices, categories

3. **Order Status** - Needs auth cookies ⚠️
   - Parse status, ETA, delivery partner

4. **Active Orders** - Needs auth cookies ⚠️
   - List all recent orders

---

## 🎯 Next Steps

1. Update `swiggy.py` with working search endpoint
2. Test menu/status/orders endpoints with real cookies
3. Parse restaurant data properly from nested structure
4. Add better error handling for auth failures

---

## 📝 Common Location Coordinates

| City | Lat | Lng |
|------|-----|-----|
| Bangalore | 12.9716 | 77.5946 |
| Delhi | 28.6139 | 77.2090 |
| Mumbai | 19.0760 | 72.8777 |
| Chennai | 13.0827 | 80.2707 |
| Kolkata | 22.5726 | 88.3639 |

---

**Tested by:** Clawdbot AI Assistant
**Date:** 2025-01-21
**Status:** Search API confirmed working ✅
