#!/usr/bin/env python3
import argparse, os, json, logging, sys
from basic_bot import BasicBot

LOG_FILE = os.path.join(os.path.dirname(__file__), '..', 'bot.log')

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s | %(levelname)s | %(message)s',
    handlers=[logging.FileHandler(LOG_FILE), logging.StreamHandler(sys.stdout)]
)

def positive_float(v):
    try:
        f = float(v)
    except:
        raise argparse.ArgumentTypeError('Must be a number')
    if f <= 0:
        raise argparse.ArgumentTypeError('Must be positive')
    return f

def main():
    p = argparse.ArgumentParser(description='Simple Binance Futures Testnet bot CLI')
    p.add_argument('order_type', choices=['MARKET','LIMIT','STOP_MARKET'], help='Order type')
    p.add_argument('symbol', help='Trading symbol e.g. BTCUSDT')
    p.add_argument('side', choices=['BUY','SELL'], help='Order side')
    p.add_argument('quantity', type=positive_float, help='Quantity (contract quantity or qty depending on symbol)')
    p.add_argument('--price', type=positive_float, help='Limit price (required for LIMIT orders)')
    p.add_argument('--stopPrice', type=positive_float, help='Stop price (required for STOP_MARKET)')
    p.add_argument('--api_key', default=os.getenv('BINANCE_API_KEY'), help='API key (or set BINANCE_API_KEY)')
    p.add_argument('--api_secret', default=os.getenv('BINANCE_API_SECRET'), help='API secret (or set BINANCE_API_SECRET)')
    p.add_argument('--dry', action='store_true', help='Dry run (do not send requests)')
    args = p.parse_args()

    if args.order_type == 'LIMIT' and not args.price:
        p.error('--price is required for LIMIT orders')
    if args.order_type == 'STOP_MARKET' and not args.stopPrice:
        p.error('--stopPrice is required for STOP_MARKET orders')

    bot = BasicBot(args.api_key, args.api_secret, testnet=True, dry_run=args.dry)
    try:
        logging.info('Placing order: %s %s %s qty=%s price=%s stopPrice=%s', args.order_type, args.side, args.symbol, args.quantity, args.price, args.stopPrice)
        res = bot.place_order(symbol=args.symbol, side=args.side, order_type=args.order_type, quantity=args.quantity, price=args.price, stopPrice=args.stopPrice)
        logging.info('Order response: %s', json.dumps(res, indent=2, default=str))
        print('\nORDER RESPONSE:\n', json.dumps(res, indent=2, default=str))
    except Exception as e:
        logging.exception('Order failed')
        print('Order failed:', e)

if __name__ == '__main__':
    main()
