#!/usr/bin/env python3
"""
Swiggy CLI v2.0 - Enhanced with auth token extraction from API responses
"""

import argparse
import json
import requests
import re
import sys
import os
from datetime import datetime
from getpass import getpass

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
        self.auth_token = None
        self.session_data = {}
        self.load_session()

    def ensure_config_dir(self):
        os.makedirs(CONFIG_DIR, exist_ok=True)

    def load_session(self):
        if os.path.exists(SESSION_FILE):
            try:
                with open(SESSION_FILE, 'r') as f:
                    self.session_data = json.load(f)
                    self.auth_token = self.session_data.get('auth_token')
                    if 'cookies' in self.session_data:
                        for name, value in self.session_data['cookies'].items():
                            self.session.cookies.set(name, value)
            except Exception as e:
                print_error(f"Failed to load session: {e}")
                self.session_data = {}

    def save_session(self):
        self.ensure_config_dir()
        session_to_save = {
            'auth_token': self.auth_token,
            'cookies': dict(self.session.cookies),
            'headers': self.session.headers.copy()
        }
        with open(SESSION_FILE, 'w') as f:
            json.dump(session_to_save, f, indent=2)
        print_success("Session saved")

    def extract_auth_from_response(self, response):
        """
        Extract auth token from Swiggy API response cookies.
        Key cookies: __SW (auth token), _sid (session), _device_id (device)
        """
        if response.headers.get('set-cookie'):
            cookies = response.headers.get('set-cookie', '')
            # Extract __SW token (main auth)
            sw_match = re.search(r'__SW=([^;]+)', cookies)
            if sw_match:
                self.auth_token = sw_match.group(1)
                print_success(f"Auth token extracted: {self.auth_token[:20]}...")

            # Extract session ID
            sid_match = re.search(r'_sid=([^;]+)', cookies)
            if sid_match:
                self.session_data['sid'] = sid_match.group(1)

            # Extract device ID
            device_match = re.search(r'_device_id=([^;]+)', cookies)
            if device_match:
                self.session_data['device_id'] = device_match.group(1)

            # Save all cookies to session
            for cookie in cookies.split(','):
                name_value = cookie.strip().split('=', 1)
                if len(name_value) == 2:
                    self.session.cookies.set(name_value[0], name_value[1])

    def search_restaurants(self, query, lat=None, lng=None):
        """
        Search restaurants - this also captures auth tokens!
        """
        if not lat or not lng:
            lat = "12.9716"
            lng = "77.5946"

        print_info(f"Searching for '{query}'...")

        try:
            url = f"{API_BASE}/restaurants/list/v5"
            params = {"lat": lat, "lng": lng, "search": query}

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Referer": "https://www.swiggy.com/"
            }

            response = self.session.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                restaurants = self._parse_restaurants(data)

                # Extract auth tokens from response
                self.extract_auth_from_response(response)

                print_success(f"Found {len(restaurants)} restaurant(s)")
                return restaurants
            else:
                print_error(f"Search failed: HTTP {response.status_code}")
                return []

        except Exception as e:
            print_error(f"Search failed: {e}")
            return []

    def get_menu(self, restaurant_id, lat=None, lng=None):
        """
        Get menu using extracted auth token
        """
        if not lat or not lng:
            lat = "12.9716"
            lng = "77.5946"

        print_info(f"Fetching menu for restaurant ID: {restaurant_id}")

        try:
            url = f"{API_BASE}/menu/pl"
            params = {
                "page-type": "REGULAR_MENU",
                "complete-menu": "true",
                "lat": lat,
                "lng": lng,
                "restaurantId": restaurant_id
            }

            headers = {
                "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "application/json",
                "Referer": "https://www.swiggy.com/",
                "Cookie": f"__SW={self.auth_token}" if self.auth_token else ""
            }

            response = self.session.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                menu_items = self._parse_menu(data)
                print_success(f"Found {len(menu_items)} menu item(s)")
                return menu_items
            elif response.status_code == 202:
                # Try to extract auth from response even on 202
                self.extract_auth_from_response(response)
                print_warning("Got 202 - retrying with new auth token...")
                return self.get_menu(restaurant_id, lat, lng)
            else:
                print_error(f"Failed to fetch menu: HTTP {response.status_code}")
                if response.text:
                    error_data = response.json() if response.headers.get('content-type', '').startswith('application/json') else {}
                    print_error(f"Error: {error_data.get('statusMessage', 'Unknown error')}")
                return None

        except Exception as e:
            print_error(f"Failed to fetch menu: {e}")
            return None

    def _parse_restaurants(self, data):
        restaurants = []
        if 'data' not in data:
            return restaurants

        cards = data['data'].get('cards', [])

        for card in cards:
            try:
                if isinstance(card, dict) and 'card' in card:
                    card_data = card['card']
                    if isinstance(card_data, dict) and 'card' in card_data:
                        card_data = card_data['card']

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
            except Exception:
                continue

        return restaurants

    def _parse_menu(self, data):
        menu_items = []
        if 'data' not in data:
            return menu_items

        menu_data = data['data']

        # Try different response structures
        if 'menu' in menu_data:
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

    def get_order_status(self, order_id, lat=None, lng=None):
        """
        Get order status using extracted auth token
        """
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
                "Referer": "https://www.swiggy.com/",
                "Cookie": f"__SW={self.auth_token}" if self.auth_token else ""
            }

            response = self.session.get(url, params=params, headers=headers)

            if response.status_code == 200:
                data = response.json()
                status_info = {
                    'orderId': data.get('data', {}).get('orderId', ''),
                    'status': data.get('data', {}).get('status', 'Unknown'),
                    'eta': data.get('data', {}).get('eta', 'N/A'),
                    'deliveryPartner': data.get('data', {}).get('deliveryPartner', 'N/A'),
                    'restaurantName': data.get('data', {}).get('restaurantName', 'N/A'),
                    'total': data.get('data', {}).get('total', 0)
                }
                return status_info
            else:
                print_error(f"Failed to get status: HTTP {response.status_code}")
                return None

        except Exception as e:
            print_error(f"Failed to get order status: {e}")
            return None

def main():
    parser = argparse.ArgumentParser(
        description="Swiggy CLI v2.0 - Enhanced with auth token extraction from API responses",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  swiggy.py search "pizza"
  swiggy.py menu 10575
  swiggy.py status ord_abc123
        """
    )

    parser.add_argument('--lat', help='Latitude for location', default="12.9716")
    parser.add_argument('--lng', help='Longitude for location', default="77.5946")

    subparsers = parser.add_subparsers(dest='command', help='Available commands')

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
    monitor_parser = subparsers.add_parser('monitor', help='Monitor order live')
    monitor_parser.add_argument('order_id', help='Order ID')
    monitor_parser.add_argument('--interval', type=int, default=30, help='Update interval in seconds')

    # Orders command
    subparsers.add_parser('orders', help='List active orders')

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        sys.exit(1)

    client = SwiggyClient()

    if args.command == 'search':
        restaurants = client.search_restaurants(args.query, args.lat, args.lng)
        if restaurants:
            print("\n" + "="*60)
            for i, r in enumerate(restaurants[:10], 1):
                cuisines = ', '.join(r.get('cuisines', []))
                rating = r.get('avgRatingString', 'N/A')
                total_ratings = r.get('totalRatingsString', '0')
                delivery_time = r.get('deliveryTimeStr', 'N/A')
                cost = r.get('costForTwo', 'N/A')
                locality = r.get('locality', '')
                area = r.get('areaName', '')
                location = f"{locality}, {area}" if locality else area
                is_open = "Open" if r.get('isOpen', False) else "Closed"

                print_color(f"{i}. {r.get('name', 'Unknown')}", Colors.BOLD)
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
                price = item.get('price', 0) / 100  # Convert paisa to rupees
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
                total = status.get('total', 0) / 100
                print(f"Total: ₹{total}")
            if status.get('deliveryPartner'):
                print(f"Delivery Partner: {status.get('deliveryPartner')}")
            print()

    elif args.command == 'monitor':
        import time as time_module
        print_info(f"Monitoring order {args.order_id} (Ctrl+C to stop)")
        print("-" * 60)

        last_status = None

        try:
            while True:
                status_info = client.get_order_status(args.order_id, args.lat, args.lng)

                if status_info:
                    current_status = status_info.get('status', 'unknown')
                    timestamp = datetime.now().strftime("%H:%M:%S")

                    if current_status != last_status:
                        print_color(f"[{timestamp}] ", Colors.CYAN, end="")
                        print_color(f"Status: {current_status.upper()}", Colors.BOLD)

                        if status_info.get('eta'):
                            print_info(f"ETA: {status_info.get('eta')}")
                        if status_info.get('deliveryPartner'):
                            print_info(f"Delivery Partner: {status_info.get('deliveryPartner')}")

                        last_status = current_status

                        if current_status.lower() in ['delivered', 'cancelled', 'failed']:
                            print_color("\n" + "="*60, Colors.GREEN)
                            print_success(f"Order {current_status}")
                            print_color("="*60 + "\n", Colors.GREEN)
                            break

                time_module.sleep(args.interval)

        except KeyboardInterrupt:
            print("\n")
            print_info("Monitoring stopped by user")
        except Exception as e:
            print_error(f"Monitoring error: {e}")

    elif args.command == 'orders':
        print_warning("Orders list requires additional API investigation")

if __name__ == "__main__":
    main()
