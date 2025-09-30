# Binance Futures Testnet Bot (Simplified)

## What's included
- `src/basic_bot.py` - BasicBot class that signs and sends REST requests to Binance Futures Testnet.
- `src/cli.py` - Command-line interface to place MARKET, LIMIT and STOP_MARKET orders.
- `src/advanced/` - Example helper scripts: stop_limit, oco (concept), twap, grid_strategy.
- `bot.log` - Log file written by the CLI when you run it.
- `requirements.txt` - Python deps.
- `report.pdf` - Placeholder (add your screenshots & explanations here).

## Setup
1. Create a Binance Futures Testnet account: https://testnet.binancefuture.com
2. Generate API key & secret from the testnet UI.
3. Install dependencies: `pip install -r requirements.txt`
4. Run example (dry run): `python src/cli.py MARKET BTCUSDT BUY 0.001 --dry`
5. Run with real API keys: `python src/cli.py LIMIT BTCUSDT BUY 0.001 --price 20000 --api_key YOURKEY --api_secret YOURSECRET`

## Notes & Safety
- This is intentionally simple for a coding assignment. Use `--dry` if you want to simulate without making live testnet requests.
- The scripts log requests and responses to `bot.log`.
- Some advanced behaviors (atomic OCO) require exchange-side support; here we provide a conceptual flow.
