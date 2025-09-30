# Simple TWAP: split a total quantity into N equal chunks and place MARKET orders spaced by interval seconds.
import time
from basic_bot import BasicBot

def twap(api_key, api_secret, symbol, side, total_qty, slices=5, interval=2, dry=True):
    bot = BasicBot(api_key, api_secret, testnet=True, dry_run=dry)
    per = float(total_qty) / int(slices)
    results = []
    for i in range(int(slices)):
        res = bot.place_order(symbol=symbol, side=side, order_type='MARKET', quantity=round(per, 8))
        results.append(res)
        time.sleep(interval)
    return results
