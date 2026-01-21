# 🗺️ Swiggy CLI - Development Roadmap

## Current Status

| Component | Status | Notes |
|-----------|---------|-------|
| Project Structure | ✅ Complete | Professional skill-like structure |
| Restaurant Search | ✅ Working | Fully functional, no auth needed |
| Authentication | ✅ Implemented | Browser-based login via Clawdbot |
| Session Management | ✅ Working | Saves to ~/.swiggy-cli/session.json |
| GitHub Repository | ✅ Published | https://github.com/kevinjosephjohn/swiggy-cli |
| Documentation | ✅ Complete | README, guides, cheatsheets |

---

## 🔴 Known Issues

### High Priority

#### 1. Menu API Returns "Something Went Wrong"

**Problem:**
```bash
curl https://www.swiggy.com/dapi/menu/pl?restaurantId=10575
# Returns: { "statusCode": 1, "statusMessage": "Oops!! Something Went Wrong" }
```

**Investigation:**
- Browser successfully loads menu page with full JSON data
- Auth cookies are captured and saved
- API endpoint is correct: `/dapi/menu/pl`
- Using correct query parameters

**Root Cause Analysis:**
1. **Missing SID cookie**: Browser may use a different session mechanism than just cookies
2. **Additional auth headers**: Swiggy likely requires CSRF token, session ID, or other headers not captured
3. **Anti-automation detection**: Swiggy may detect CLI-based requests vs browser requests
4. **Location mismatch**: Browser uses different location (13.08950, 80.27390 - possibly Chennai) than expected Bangalore (12.9716, 77.5946)

**Evidence from browser investigation:**
- URL called by browser: `lat=13.08950&lng=80.27390&restaurantId=bangalore`
- This is wrong - "bangalore" is not an ID, and coords are wrong for Bangalore area
- Search API works with same cookies (returns 12 cards)
- Menu API call fails with HTTP 202

**Possible Solutions:**
1. Capture SID from browser `sessionStorage.tid` and include in session
2. Use exact headers from browser (including CSRF token)
3. Try different restaurant IDs accessible from actual location
4. Manual browser-based menu access for now

#### 2. Order Status & Monitoring APIs

**Problem:** Same auth issue as menu - requires additional headers/tokens

**Status:** Code implemented, but untested due to menu API failure

#### 3. Order Placement API

**Status:** Not implemented - requires:
- Complex multi-step flow (cart → payment → confirm)
- Payment gateway integration
- Address validation
- Item customization (size, toppings, add-ons)

---

## 📊 Technical Debt

| Area | Priority | Effort |
|-------|----------|---------|
| Fix menu API auth | High | 2-4 hours |
| Fix order status API | Medium | 1-2 hours |
| Test order monitoring | Medium | 1 hour |
| Implement order placement | High | 4-8 hours |
| Add error handling improvements | Low | 1 hour |
| Add unit tests | Medium | 2-3 hours |

---

## 🎯 Development Plan

### Phase 1: Bug Fixes (Week 1)

**Goal:** Get menu and order features working

#### Tasks:
- [ ] Investigate and capture SID from `sessionStorage`
- [ ] Capture complete request headers from browser (CSRF, auth tokens)
- [ ] Test menu API with enhanced auth headers
- [ ] Test order status API
- [ ] Test order monitoring feature
- [ ] Add proper error messages for auth failures

**Deliverable:**
- Menu display working
- Order status checking working
- Real-time order monitoring working

#### Implementation Notes:
- Use browser automation to capture full auth context
- Parse SID from sessionStorage: `dd0be675-1e43-47df-ab7f-f2b368d429e0`
- Add SID to Cookie header
- Add CSRF token from API responses

---

### Phase 2: Feature Enhancements (Week 2-3)

**Goal:** Add missing features and improve UX

#### Tasks:
- [ ] Add location auto-detection (use IP geolocation or prompt user)
- [ ] Add favorites management (save restaurant IDs)
- [ ] Add order history
- [ ] Add quick reordering
- [ ] Add price filtering in search
- [ ] Add rating/sorting in search
- [ ] Add color-coded output (veg/non-veg indicators)
- [ ] Add interactive menu selection
- [ ] Add progress bars for long operations

**Deliverable:**
- Full-featured CLI for Swiggy management
- Enhanced search with filters
- Personalized features (favorites, history)

---

### Phase 3: Advanced Features (Week 4+)

**Goal:** Power user features

#### Tasks:
- [ ] Implement order placement flow
- [ ] Add cart management
- [ ] Add multiple location support
- [ ] Add backup/restore functionality
- [ ] Add notifications (desktop, push)
- [ ] Add web UI/dashboard mode
- [ ] Add export order history (CSV, PDF)
- [ ] Add price comparison across restaurants
- [ ] Add coupon/discount code management

**Deliverable:**
- Complete food ordering CLI
- Desktop notifications support
- Analytics and reporting
- Cross-platform support (Linux, Windows)

---

## 🔬 Research Needed

| Area | Questions to Answer |
|-------|--------------------|
| Swiggy API Documentation | Are there official docs or reverse-engineered patterns? |
| Menu API Auth | What exact headers/tokens does menu API require? |
| Order Placement Flow | What's the complete order placement endpoint sequence? |
| Session Management | How does Swiggy generate and validate sessions? |
| Rate Limiting | What are Swiggy's API rate limits? |
| WebSockets | Does Swiggy use websockets for real-time updates? |

---

## 📈 Version History

| Version | Date | Changes |
|---------|------|---------|
| **1.0.0** | Initial release |
| | Restaurant search API |
| | Browser-based authentication |
| | Basic session management |
| | GitHub publication |
| **1.1.0** | In progress |
| | Enhanced documentation |
| | Development roadmap |
| | Project restructuring for skills format |
| **1.2.0** | Planned |
| | Menu API fix |
| | Order status/monitoring features |
| | Enhanced error handling |
| | Better location support |

---

## 💡 Architecture Decisions

### Why This Structure?

1. **Wrapper Script (`swiggy`)**
   - Auto-manages Python virtual environment
   - User-friendly entry point
   - Avoids `python3 -m venv` complexity

2. **Python Application (`swiggy.py`)**
   - Core CLI logic with argparse
   - Uses requests library for HTTP calls
   - Session management with cookies

3. **Documentation (`README.md`, etc.)**
   - Multiple entry points (quick start, full docs, reference)
   - Markdown format for GitHub rendering

4. **Git Configuration (`.gitignore`)**
   - Excludes sensitive auth data
   - Excludes virtual environment
   - Tracks only code and documentation

### Authentication Strategy

**Chosen:** Browser-based cookie capture via Clawdbot

**Reasons:**
1. Avoids storing passwords in CLI
2. Captures all necessary auth headers/tokens
3. Reuses existing browser session
4. More secure than CLI-based login

**Drawbacks:**
1. Requires browser interaction (one-time setup)
2. Session expires, needs renewal
3. Different from pure CLI experience

---

## 🤝 External Dependencies

| Dependency | Version | Purpose |
|------------|----------|---------|
| requests | >=2.31.0 | HTTP client |
| Python | >=3.7 | Runtime |
| Clawdbot Gateway | - | Browser automation (optional) |

---

## 🚧 Future Improvements

### Short-term (Next 2 weeks)
1. Fix menu API authentication
2. Add comprehensive error messages
3. Test all features end-to-end
4. Add unit tests for critical paths

### Mid-term (Next 1-2 months)
1. Implement order placement flow
2. Add cart management
3. Add favorites feature
4. Improve documentation with real examples
5. Add Docker support for easy deployment

### Long-term (Next 3-6 months)
1. Web dashboard for visual order management
2. Mobile app support
3. Multi-city/location support
4. Analytics dashboard
5. Community features (reviews, recommendations)

---

## 📞 Known Limitations

1. **Unofficial APIs** - Swiggy may change endpoints without notice
2. **No mobile support** - Designed for terminal/desktop use
3. **Location-dependent** - Search results vary by location
4. **Single account** - Doesn't support multi-account switching
5. **Session expiration** - Cookies expire, need manual re-login

---

## 🎯 Success Metrics

| Metric | Target | Current |
|---------|--------|---------|
| Features working | 10+ | 4 (search, auth, CLI) |
| User satisfaction | - | N/A (not released yet) |
| API reliability | 95% | ~60% (menu/orders failing) |
| Code coverage | 80% | ~30% (untested paths) |

---

## 📚 Additional Resources

### Internal
- `API_ENDPOINTS_DISCOVERED.md` - Full API documentation
- `API_INVESTIGATION.md` - Browser-based investigation
- `LOGIN_COMPLETE.md` - Authentication report
- `PROGRESS_SUMMARY.md` - Development progress

### External
- Swiggy website: https://www.swiggy.com
- Swiggy business (for partnerships): https://partner.swiggy.com

---

## 🎊 Risk Assessment

| Risk | Level | Mitigation |
|------|--------|------------|
| Swiggy API changes | High | Document endpoints, add error handling |
| Session expiration | Medium | Auto-renewal prompts, clear documentation |
| Bot detection | Medium | Use proper User-Agent, headers |
| Location data issues | Low | Auto-detection, clear prompts |

---

## 📝 Notes

- Development prioritized bug fixes (menu API) over new features
- Authentication is the biggest blocker for menu/orders features
- Browser-based auth is practical but not ideal for CLI
- Consider implementing pure CLI auth if Swiggy provides email/password login option
- Keep code modular for easier testing and maintenance

---

**Last Updated:** January 21, 2025
**Next Review:** After menu API fix is implemented
**Maintained by:** Kevin Joseph John
