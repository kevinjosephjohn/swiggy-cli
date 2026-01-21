#!/usr/bin/env python3
"""
Swiggy CLI Tool - Place and monitor orders via unofficial API
"""

import argparse
import json
import requests
import time
import sys
from datetime import datetime
from getpass import getpass
import os

# Configuration
CONFIG_DIR = os.path.expanduser("~/.swiggy-cli")
CONFIG_FILE = os.path.join(CONFIG_DIR, "config.json")
SESSION_FILE = os.path.join(CONFIG_DIR, "session.json")

# Swiggy API endpoints (unofficial)
BASE_URL = "https://www.swiggy.com"
API_BASE = "https://www.swiggy.com/dapi"

# Colors for terminal output
class Colors:
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BLUE = '\033[94m'
    MAGENTA = '\033[95m'
    CYAN = '\033[96m'
    WHITE = '\033[97m'
    RESET = '\033[0m'
    BOLD = '\033[1m'

def print_color(message, color=Colors.WHITE):
    """Print colored message to terminal"""
    print(f"{color}{message}{Colors.RESET}")

def print_success(message):
    print_color(f"✓ {message}", Colors.GREEN)

def print_error(message):
    print_color(f"✗ {message}", Colors.RED)

def print_warning(message):
    print_color(f"⚠ {message}", Colors.YELLOW)

def print_info(message):
    print_color(f"ℹ {message}", Colors.BLUE)

class SwiggyClient:
    def __init__(self):
        self.session = requests.Session()
        self.session_data = {}
        self.load_session()

    def ensure_config_dir(self):
        """Create config directory if it doesn't exist"""
        os.makedirs(CONFIG_DIR, exist_ok=True)

    def load_session(self):
        """Load saved session from file"""
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, 'r') as f:
                    self.session_data = json.load(f)
                    # Set session cookies
                    if 'cookies' in self.session_data:
                        for name, value in self.session_data['cookies'].items():
                            self.session.cookies.set(name, value)
                    # Set auth headers
                    if 'headers' in self.session_data:
                        self.session.headers.update(self.session_data['headers'])
            except Exception as e:
                print_error(f"Failed to load session: {e}")
                self.session_data = {}

    def save_session(self):
        """Save session to file"""
        self.ensure_config_dir()
        self.session_data['cookies'] = dict(self.session.cookies)
        self.session_data['headers'] = dict(self.session.headers)
        with open(SESSION_FILE, 'w') as f:
            json.dump(self.session_data, f, indent=2)
        print_success("Session saved")

    def login(self):
        """Login using email/phone and OTP"""
        print_info("Swiggy Login")
        print("-" * 40)

        method = input("Login with (email/phone)? ").strip().lower()

        if method == 'email':
            email = input("Enter your email: ").strip()
            payload = {"email": email}
        elif method == 'phone':
            phone = input("Enter your phone (with country code): ").strip()
            payload = {"phone": phone}
        else:
            print_error("Invalid method")
            return False

        # Send OTP
        print_info("Sending OTP...")
        try:
            # Note: Actual endpoint may vary; this is a placeholder
            # You may need to capture the actual endpoint from browser devtools
            print_warning("Note: You may need to capture the actual OTP endpoint from browser network tab")
            print_info("For now, we'll simulate login - replace with actual API call")

            otp = getpass("Enter OTP: ").strip()

            # Verify OTP (placeholder)
            # headers = self.session.headers.copy()
            # response = self.session.post(f"{API_BASE}/auth/verify-otp", json={**payload, "otp": otp})

            # For demo, ask for auth token directly from browser
            print("\n" + "="*50)
            print_info("To get your auth token:")
            print("1. Open Swiggy website in browser")
            print("2. Log in to your account")
            print("3. Open Developer Tools (F12)")
            print("4. Go to Network tab")
            print("5. Find a request to Swiggy API")
            print("6. Copy the 'Cookie' header value")
            print("="*50 + "\n")

            cookies = input("Paste Cookie header value: ").strip()
            if cookies:
                # Parse cookies
                cookie_dict = {}
                for item in cookies.split(';'):
                    item = item.strip()
                    if '=' in item:
                        key, value = item.split('=', 1)
                        cookie_dict[key] = value
                        self.session.cookies.set(key, value)

                self.save_session()
                print_success("Login successful!")
                return True
            else:
                print_error("No cookies provided")
                return False

        except Exception as e:
            print_error(f"Login failed: {e}")
            return False

    def logout(self):
        """Clear session"""
        if os.path.exists(SESSION_FILE):
            os.remove(SESSION_FILE)
        self.session_data = {}
        self.session.cookies.clear()
        print_success("Logged out successfully")

    def search_restaurants(self, query, lat=None, lng=None):
        """Search for restaurants"""
        if not lat or not lng:
            # Use default Bangalore coordinates
            lat = "12.9716"
            lng = "77.5946"

        print_info(f"Searching for '{query}'...")

        try:
            url = f"{API_BASE}/restaurants/list/v5"
            params = {
                "lat": lat,
                "lng": lng,
                "search": query
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Referer": "https://www.swiggy.com/"
            }

            response = self.session.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                restaurants = self._parse_restaurants(data)
                print_success(f"Found {len(restaurants)} restaurant(s)")
                return restaurants
            else:
                print_error(f"Search failed: HTTP {response.status_code}")
                return []

        except Exception as e:
            print_error(f"Search failed: {e}")
            return []

    def _parse_restaurants(self, data):
        """Parse restaurant data from API response"""
        restaurants = []

        if 'data' not in data:
            return restaurants

        cards = data['data'].get('cards', [])

        for card in cards:
            try:
                # Handle different card structures
                if isinstance(card, dict) and 'card' in card:
                    card_data = card['card']
                    if isinstance(card_data, dict) and 'card' in card_data:
                        card_data = card_data['card']

                    # Check for restaurant listing widgets
                    grid_elements = card_data.get('gridElements', {})
                    info_with_style = grid_elements.get('infoWithStyle', {})

                    if 'restaurants' in info_with_style:
                        for restaurant in info_with_style['restaurants']:
                            info = restaurant.get('info', {})
                            if 'id' in info and 'name' in info:
                                restaurants.append({
                                    'id': info.get('id'),
                                    'name': info.get('name'),
                                    'locality': info.get('locality', ''),
                                    'areaName': info.get('areaName', ''),
                                    'costForTwo': info.get('costForTwo', ''),
                                    'cuisines': info.get('cuisines', []),
                                    'avgRating': info.get('avgRating', 0),
                                    'avgRatingString': info.get('avgRatingString', 'N/A'),
                                    'totalRatingsString': info.get('totalRatingsString', '0'),
                                    'deliveryTime': info.get('sla', {}).get('deliveryTime', 0),
                                    'deliveryTimeStr': info.get('sla', {}).get('slaString', 'N/A'),
                                    'isOpen': info.get('isOpen', False)
                                })
            except Exception as e:
                # Skip malformed cards
                continue

        return restaurants

    def get_menu(self, restaurant_id, lat=None, lng=None):
        """Get menu for a restaurant"""
        if not lat or not lng:
            lat = "12.9716"
            lng = "77.5946"

        print_info(f"Fetching menu for restaurant ID: {restaurant_id}")

        try:
            url = f"{API_BASE}/menu/pl"
            params = {
                "lat": lat,
                "lng": lng,
                "page-type": "REGULAR_MENU",
                "complete-menu": "true",
                "restaurant-menu-id": restaurant_id
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Referer": "https://www.swiggy.com/"
            }

            response = self.session.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                menu_items = self._parse_menu(data)
                print_success(f"Found {len(menu_items)} menu item(s)")
                return menu_items
            else:
                print_error(f"Failed to fetch menu: HTTP {response.status_code}")
                print_warning("Note: Menu endpoint may require authentication (cookies)")
                print_info("Run './swiggy login' to add cookies from your browser session")
                return None

        except Exception as e:
            print_error(f"Failed to fetch menu: {e}")
            return None

    def _parse_menu(self, data):
        """Parse menu items from API response"""
        menu_items = []

        if 'data' not in data:
            return menu_items

        # Try different response structures
        menu_data = data['data']

        # Structure 1: Direct items array
        if 'items' in menu_data:
            for item in menu_data['items']:
                menu_items.append({
                    'id': item.get('id', ''),
                    'name': item.get('name', ''),
                    'price': item.get('price', 0),
                    'description': item.get('description', ''),
                    'isVeg': item.get('isVeg', True)
                })

        # Structure 2: Categories with items
        elif 'menu' in menu_data:
            menu_obj = menu_data['menu']
            if 'items' in menu_obj:
                for item in menu_obj['items']:
                    menu_items.append({
                        'id': item.get('id', ''),
                        'name': item.get('name', ''),
                        'price': item.get('price', 0),
                        'description': item.get('description', ''),
                        'isVeg': item.get('isVeg', True)
                    })

        return menu_items

    def place_order(self, items, restaurant_id, address_id=None, lat=None, lng=None):
        """
        Place an order
        items: list of dicts with item_id and quantity
        """
        if not lat or not lng:
            lat = "12.9716"
            lng = "77.5946"

        print_info("Placing order...")

        try:
            # Build order payload (structure may need adjustment)
            payload = {
                "restaurantId": restaurant_id,
                "items": items,
                "lat": lat,
                "lng": lng,
                "addressId": address_id,
                "paymentMode": "UPI"  # Can be changed
            }

            url = f"{API_BASE}/checkout/place-order"
            headers = {
                "Content-Type": "application/json",
                "User-Agent": "Mozilla/5.0"
            }

            response = self.session.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                data = response.json()
                if 'data' in data and 'orderId' in data['data']:
                    order_id = data['data']['orderId']
                    print_success(f"Order placed successfully! Order ID: {order_id}")
                    return order_id
                else:
                    print_error("Order placement failed")
                    return None
            else:
                print_error(f"Order failed: HTTP {response.status_code}")
                print_error(response.text)
                return None

        except Exception as e:
            print_error(f"Order placement failed: {e}")
            return None

    def get_order_status(self, order_id, lat=None, lng=None):
        """Get status of an order"""
        if not lat or not lng:
            lat = "12.9716"
            lng = "77.5946"

        print_info(f"Checking status for order {order_id}")

        try:
            url = f"{API_BASE}/orders/{order_id}"
            params = {"lat": lat, "lng": lng}

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Referer": "https://www.swiggy.com/"
            }

            response = self.session.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                status_info = self._parse_order_status(data)
                return status_info
            else:
                print_error(f"Failed to get status: HTTP {response.status_code}")
                print_warning("Note: Order status requires authentication (cookies)")
                print_info("Run './swiggy login' to add cookies from your browser session")
                return None

        except Exception as e:
            print_error(f"Failed to get order status: {e}")
            return None

    def _parse_order_status(self, data):
        """Parse order status from API response"""
        if 'data' not in data:
            return None

        order_data = data['data']

        return {
            'orderId': order_data.get('orderId', ''),
            'status': order_data.get('status', 'Unknown'),
            'eta': order_data.get('eta', 'N/A'),
            'deliveryPartner': order_data.get('deliveryPartner', 'N/A'),
            'restaurantName': order_data.get('restaurantName', 'N/A'),
            'total': order_data.get('total', 0),
            'trackingUrl': order_data.get('trackingUrl', ''),
            'items': order_data.get('items', [])
        }

    def list_active_orders(self, lat=None, lng=None):
        """List all active orders"""
        if not lat or not lng:
            lat = "12.9716"
            lng = "77.5946"

        print_info("Fetching active orders...")

        try:
            url = f"{API_BASE}/orders/list"
            params = {"lat": lat, "lng": lng}

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Referer": "https://www.swiggy.com/"
            }

            response = self.session.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                orders = self._parse_orders(data)
                print_success(f"Found {len(orders)} active order(s)")
                return orders
            else:
                print_error(f"Failed to fetch orders: HTTP {response.status_code}")
                print_warning("Note: Orders list requires authentication (cookies)")
                print_info("Run './swiggy login' to add cookies from your browser session")
                return []

        except Exception as e:
            print_error(f"Failed to fetch orders: {e}")
            return []

    def _parse_orders(self, data):
        """Parse orders list from API response"""
        orders = []

        if 'data' not in data:
            return orders

        orders_data = data['data']

        # Structure 1: Direct orders array
        if isinstance(orders_data, list):
            for order in orders_data:
                orders.append({
                    'orderId': order.get('orderId', ''),
                    'status': order.get('status', 'Unknown'),
                    'restaurantName': order.get('restaurantName', 'N/A'),
                    'total': order.get('total', 0),
                    'eta': order.get('eta', 'N/A'),
                    'orderDate': order.get('orderDate', 'N/A')
                })

        # Structure 2: Nested orders object
        elif isinstance(orders_data, dict) and 'orders' in orders_data:
            for order in orders_data['orders']:
                orders.append({
                    'orderId': order.get('orderId', ''),
                    'status': order.get('status', 'Unknown'),
                    'restaurantName': order.get('restaurantName', 'N/A'),
                    'total': order.get('total', 0),
                    'eta': order.get('eta', 'N/A'),
                    'orderDate': order.get('orderDate', 'N/A')
                })

        return orders

    def monitor_order(self, order_id, interval=30, lat=None, lng=None):
        """Monitor order status continuously"""
        if not lat or not lng:
            lat = "12.9716"
            lng = "77.5946"

        print_info(f"Monitoring order {order_id} (Ctrl+C to stop)")
        print("-" * 60)

        last_status = None

        try:
            while True:
                status_info = self.get_order_status(order_id, lat, lng)

                if status_info:
                    current_status = status_info.get('status', 'unknown')
                    timestamp = datetime.now().strftime("%H:%M:%S")

                    if current_status != last_status:
                        print_color(f"[{timestamp}] ", Colors.CYAN, end="")
                        print_color(f"Status: {current_status.upper()}", Colors.BOLD)

                        # Print additional details
                        if status_info.get('eta'):
                            print_info(f"ETA: {status_info['eta']}")
                        if status_info.get('deliveryPartner'):
                            print_info(f"Delivery Partner: {status_info['deliveryPartner']}")

                        last_status = current_status

                        # Stop monitoring if order is completed
                        if current_status.lower() in ['delivered', 'cancelled', 'failed']:
                            print_color("\n" + "="*60, Colors.GREEN)
                            print_success(f"Order {current_status}")
                            print_color("="*60 + "\n", Colors.GREEN)
                            break

                time.sleep(interval)

        except KeyboardInterrupt:
            print("\n")
            print_info("Monitoring stopped by user")
        except Exception as e:
            print_error(f"Monitoring error: {e}")


def main():
    parser = argparse.ArgumentParser(
        description="Swiggy CLI - Place and monitor orders via unofficial API",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  swiggy.py login                          # Login to your account
  swiggy.py search "pizza"                 # Search for restaurants
  swiggy.py menu <restaurant-id>           # Get restaurant menu
  swiggy.py status <order-id>              # Check order status
  swiggy.py monitor <order-id>             # Monitor order live
  swiggy.py orders                         # List active orders
        """
    )

    parser.add_argument('--lat', help='Latitude for location', default="12.9716")
    parser.add_argument('--lng', help='Longitude for location', default="77.5946")

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

    # Login command
    subparsers.add_parser('login', help='Login to Swiggy account')

    # Logout command
    subparsers.add_parser('logout', help='Logout and clear session')

    # Search command
    search_parser = subparsers.add_parser('search', help='Search restaurants')
    search_parser.add_argument('query', help='Search query')

    # Menu command
    menu_parser = subparsers.add_parser('menu', help='Get restaurant menu')
    menu_parser.add_argument('restaurant_id', help='Restaurant ID')

    # Status command
    status_parser = subparsers.add_parser('status', help='Get order status')
    status_parser.add_argument('order_id', help='Order ID')

    # Monitor command
    monitor_parser = subparsers.add_parser('monitor', help='Monitor order status live')
    monitor_parser.add_argument('order_id', help='Order ID')
    monitor_parser.add_argument('--interval', type=int, default=30,
                               help='Update interval in seconds (default: 30)')

    # Orders command
    subparsers.add_parser('orders', help='List active orders')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = SwiggyClient()

    # Execute commands
    if args.command == 'login':
        client.login()

    elif args.command == 'logout':
        client.logout()

    elif args.command == 'search':
        restaurants = client.search_restaurants(args.query, args.lat, args.lng)
        if restaurants:
            print("\n" + "="*60)
            for i, r in enumerate(restaurants[:10], 1):
                name = r.get('name', 'Unknown')
                cuisines = ', '.join(r.get('cuisines', []))
                rating = r.get('avgRatingString', 'N/A')
                total_ratings = r.get('totalRatingsString', '0')
                delivery_time = r.get('deliveryTimeStr', 'N/A')
                cost = r.get('costForTwo', 'N/A')
                locality = r.get('locality', '')
                area = r.get('areaName', '')
                location = f"{locality}, {area}" if locality else area
                is_open = "Open" if r.get('isOpen', False) else "Closed"

                print_color(f"{i}. {name}", Colors.BOLD)
                print(f"   Rating: {rating} ({total_ratings}) | Delivery: {delivery_time} | {is_open}")
                print(f"   Cuisine: {cuisines}")
                print(f"   Cost: {cost} | {location}")
                print(f"   ID: {r.get('id', 'N/A')}")
                print()

    elif args.command == 'menu':
        menu_items = client.get_menu(args.restaurant_id, args.lat, args.lng)
        if menu_items:
            print("\n" + "="*60)
            print_color("MENU", Colors.BOLD)
            print("="*60)
            for i, item in enumerate(menu_items[:20], 1):
                name = item.get('name', 'Unknown')
                price = item.get('price', 0)
                veg_indicator = "🟢" if item.get('isVeg', True) else "🔴"
                description = item.get('description', '')

                print_color(f"{i}. {veg_indicator} {name}", Colors.WHITE)
                print(f"   Price: ₹{price}")
                if description:
                    print(f"   {description[:80]}{'...' if len(description) > 80 else ''}")
                print()

    elif args.command == 'status':
        status = client.get_order_status(args.order_id, args.lat, args.lng)
        if status:
            print("\n" + "="*60)
            print_color(f"Order: {status.get('orderId', args.order_id)}", Colors.BOLD)
            print("="*60)
            print(f"Status: {status.get('status', 'Unknown')}")
            if status.get('eta'):
                print(f"ETA: {status.get('eta')}")
            if status.get('restaurantName'):
                print(f"Restaurant: {status.get('restaurantName')}")
            if status.get('total'):
                print(f"Total: ₹{status.get('total')}")
            if status.get('deliveryPartner'):
                print(f"Delivery Partner: {status.get('deliveryPartner')}")
            print()

    elif args.command == 'monitor':
        client.monitor_order(args.order_id, args.interval)

    elif args.command == 'orders':
        orders = client.list_active_orders(args.lat, args.lng)
        if orders:
            print("\n" + "="*60)
            print_color("ACTIVE ORDERS", Colors.BOLD)
            print("="*60)
            for order in orders:
                print_color(f"Order ID: {order.get('orderId', 'N/A')}", Colors.CYAN)
                print(f"Status: {order.get('status', 'Unknown')}")
                print(f"Restaurant: {order.get('restaurantName', 'N/A')}")
                print(f"Total: ₹{order.get('total', 'N/A')}")
                if order.get('eta'):
                    print(f"ETA: {order.get('eta')}")
                if order.get('orderDate'):
                    print(f"Date: {order.get('orderDate')}")
                print()


if __name__ == "__main__":
    main()
