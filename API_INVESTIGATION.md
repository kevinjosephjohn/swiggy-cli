# 🔍 Swiggy API Investigation Results

## Browser-Based API Calls Analysis

### Menu API Call Found

**URL Detected:**
```
https://www.swiggy.com/dapi/menu/pl?page-type=REGULAR_MENU&complete-menu=true&lat=13.08950&lng=80.27390&restaurantId=bangalore&catalog_qa=undefined&submitAction=ENTER
```

**Key Findings:**
| Parameter | Value | Issue |
|-----------|--------|-------|
| `lat` | 13.08950 | ❌ Wrong! (Bangalore should be ~12.97, ~77.59) |
| `lng` | 80.27390 | ❌ Wrong! |
| `restaurantId` | "bangalore" | ❌ This is NOT a restaurant ID! |
| Response Status | 202 | ⚠️ Accepted (not OK) |

### Problem Identified

The page is using:
1. **Wrong location** (13.08, 80.27) - Not Bangalore!
2. **Wrong restaurant ID** - "bangalore" instead of actual ID like "10575"

This explains why:
- Menu API returns "Something Went Wrong" ❌
- Restaurant search works (it uses correct coordinates)

### Root Cause

The browser session has a different location set than expected. Looking at localStorage:
- `userLocation` in cookies had encoded Bangalore coordinates
- But menu API call used coordinates 13.08, 80.27

**This location (13.08950, 80.27390) is likely:**
- Chennai (13.0827, 80.2707) - Close match!

### Authentication Flow Observed

Swiggy uses:
1. **Cookies**: `_gcl_au`, `_gid`, `_ga_*`, `aws-waf-token`, `userLocation`
2. **localStorage**: `NRBA_SESSION`, `aws_waf_token_challenge_attempts`
3. **sessionStorage**: `tid` (transaction ID)
4. **AWS WAF Token**: Changes on each request

### Why Menu API Fails from CLI

**Issue**: Restaurant ID is being passed wrong!

**Browser call:**
```
restaurantId=bangalore
```

**CLI call:**
```
restaurant-menu-id=10575
```

**Different parameter names!**
- Browser uses: `restaurantId`
- CLI uses: `restaurant-menu-id`

Let me test with correct parameter:
