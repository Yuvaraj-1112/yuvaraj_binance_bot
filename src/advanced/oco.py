# OCO conceptual implementation for futures (non-atomic): place TP limit and stop market; you should monitor and cancel remaining order when one fills.
from basic_bot import BasicBot

def place_oco(api_key, api_secret, symbol, side, quantity, take_profit_price, stop_price, dry=True):
    bot = BasicBot(api_key, api_secret, testnet=True, dry_run=dry)
    tp_side = 'SELL' if side.upper() == 'BUY' else 'BUY'
    tp = bot.place_order(symbol=symbol, side=tp_side, order_type='LIMIT', quantity=quantity, price=take_profit_price)
    sm = bot.place_order(symbol=symbol, side=tp_side, order_type='STOP_MARKET', quantity=quantity, stopPrice=stop_price)
    return {'take_profit': tp, 'stop_market': sm}
