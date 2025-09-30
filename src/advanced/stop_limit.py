# stop_limit helper using BasicBot to place conditional orders.
from basic_bot import BasicBot

def place_stop_market(api_key, api_secret, symbol, side, quantity, stopPrice, dry=True):
    bot = BasicBot(api_key, api_secret, testnet=True, dry_run=dry)
    return bot.place_order(symbol=symbol, side=side, order_type='STOP_MARKET', quantity=quantity, stopPrice=stopPrice)
