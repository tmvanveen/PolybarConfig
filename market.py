#!/usr/bin/env python3

import configparser
import sys
import requests
from decimal import Decimal
from os.path import expanduser, exists
import yfinance as yf
from datetime import datetime, timedelta
from bs4 import BeautifulSoup

def load_config():
    config = configparser.ConfigParser()
    try:
        with open(expanduser('~/.config/polybar/market-config'), 'r', encoding='utf-8') as f:
            config.read_file(f)
        return config
    except FileNotFoundError:
        sys.stdout.write('Config file not found')
        sys.exit(1)

def fetch_munten_price(metal):
    try:
        url = 'https://www.101munten.nl/'
        headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36'}
        response = requests.get(url, headers=headers, timeout=5)
        soup = BeautifulSoup(response.text, 'html.parser')
        
        metal_elem = soup.find('li', class_='graph-trigger metal-price', attrs={'data-metal-nicename': metal})
        if not metal_elem:
            return None, None
        
        price_tag = metal_elem.find('b')
        if not price_tag:
            return None, None
        price_text = price_tag.text.replace('€', '').replace(',', '').strip()
        price_eur_per_kg = Decimal(price_text)
        
        history_tag = metal_elem.find('span', class_='graph-history')
        change_direction = 0.0
        if history_tag:
            history_value = history_tag.get('data-history', 'neutral')
            change_direction = 1.0 if history_value == 'positive' else -1.0 if history_value == 'negative' else 0.0
        
        return price_eur_per_kg, change_direction
    except Exception as e:
        print(f"Error fetching {metal}")
        return None, None

def fetch_index_price(symbol):
    try:
        ticker = yf.Ticker(symbol)
        hist = ticker.history(period="2d", auto_adjust=False)
        if len(hist) >= 2:
            current_price = Decimal(str(hist['Close'].iloc[-1]))
            prev_price = Decimal(str(hist['Close'].iloc[-2]))
            change_24 = float(((current_price - prev_price) / prev_price) * 100)
            return round(current_price, 2), change_24
        return None, None
    except Exception as e:
        print(f"Error fetching {symbol}: {str(e)}", file=sys.stderr)
        return None, None

def get_next_item(config, items):
    state_file = expanduser('~/.config/polybar/market-state')
    items_list = [x for x in items if x != 'general']
    total_items = len(items_list)
    
    # Read current index or start at 0
    current_idx = 0
    if exists(state_file):
        with open(state_file, 'r') as f:
            try:
                current_idx = int(f.read().strip()) % total_items
            except ValueError:
                current_idx = 0
    
    # Get the current item
    item = items_list[current_idx]
    icon = config[item].get('icon', '')
    display_opt = config['general'].get('display', 'both')
    
    if item == 'silver':
        price, change_24 = fetch_munten_price('zilver')
    elif item == 'gold':
        price, change_24 = fetch_munten_price('goud')
    elif item == 'dowjones':
        price, change_24 = fetch_index_price('^DJI')
    elif item == 'aex':
        price, change_24 = fetch_index_price('^AEX')
    else:
        price, change_24 = None, None
    
    # Write next index
    with open(state_file, 'w') as f:
        f.write(str((current_idx + 1) % total_items))
    
    # Format output
    if price is None or change_24 is None:
        return f'{icon} N/A'
    
    if display_opt == 'both':
        change_str = f"+{change_24:.0f}%" if change_24 > 0 else f"{change_24:.0f}%" if change_24 < 0 else "0%"
        if item in ['dowjones', 'aex']:
            change_str = f"{change_24:+.2f}%"
        return f'{icon} {price}/{change_str}'
    elif display_opt == 'percentage':
        change_str = f"{change_24:+.2f}%" if item in ['dowjones', 'aex'] else f"+{change_24:.0f}%" if change_24 > 0 else f"{change_24:.0f}%"
        return f'{icon} {change_str}'
    elif display_opt == 'price':
        return f'{icon} {price}'

def main():
    config = load_config()
    output = get_next_item(config, config.sections())
    sys.stdout.write(output)

if __name__ == '__main__':
    main()
