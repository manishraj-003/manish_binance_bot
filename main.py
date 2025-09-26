from src.client import get_client
from src.market_orders import place_market_order
from src.limit_orders import place_limit_order
from src.advanced.oco import place_oco_order
from src.advanced.twap import place_twap_order

client = get_client()

# --- MARKET ORDER ---
place_market_order("BTCUSDT", "BUY", 0.01)

# --- LIMIT ORDER (price rounded to tick size) ---
current_price = float(client.futures_symbol_ticker(symbol="BTCUSDT")['price'])
# Slightly above market for SELL
limit_price = current_price * 1.01
place_limit_order("BTCUSDT", "SELL", 0.01, price=limit_price)

# --- OCO ORDER ---
# Automatic TP/SL calculation (no need to provide price/stop_price)
place_oco_order("BTCUSDT", "SELL", 0.01)
# --- TWAP ORDER ---
# Buy 0.05 BTC in 5 slices, 0.5 sec delay between slices
place_twap_order("BTCUSDT", "BUY", 0.05, slices=5, delay=0.5)
