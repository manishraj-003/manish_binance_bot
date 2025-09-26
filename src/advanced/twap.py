# src/advanced/twap.py
import time
from src.logger import log_event
from src.market_orders import place_market_order

def place_twap_order(symbol, side, total_qty, slices=5, delay=1.0):
    slice_qty = total_qty / slices
    results = []

    for i in range(1, slices + 1):
        order = place_market_order(symbol, side, slice_qty)
        msg = f"[TWAP] {side} {slice_qty:.4f} {symbol} (slice {i}/{slices})"
        log_event(msg)
        results.append(order)
        time.sleep(delay)

    return {"status": "completed", "type": "TWAP", "symbol": symbol, "slices": results}
