# src/market_orders.py
from src.logger import log_event
from src.client import get_client

def place_market_order(symbol, side, quantity):
    client = get_client()
    try:
        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="MARKET",
            quantity=quantity
        )
        msg = f"[MARKET] {side} {quantity} {symbol} | OrderId={order['orderId']}"
        log_event(msg)
        return order
    except Exception as e:
        log_event(f"[ERROR] Market order failed: {e}")
        return None
