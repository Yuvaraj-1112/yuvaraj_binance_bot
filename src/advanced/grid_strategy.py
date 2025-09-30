# Very simple grid strategy example: place limit buy/sell orders on a price grid.
from basic_bot import BasicBot

def create_grid(api_key, api_secret, symbol, lower_price, upper_price, steps, qty_per_order, dry=True):
    bot = BasicBot(api_key, api_secret, testnet=True, dry_run=dry)
    step = (upper_price - lower_price) / float(steps)
    orders = []
    for i in range(steps):
        price = round(lower_price + i*step, 2)
        orders.append(bot.place_order(symbol=symbol, side='BUY', order_type='LIMIT', quantity=qty_per_order, price=price))
        orders.append(bot.place_order(symbol=symbol, side='SELL', order_type='LIMIT', quantity=qty_per_order, price=round(price+step,2)))
    return orders
