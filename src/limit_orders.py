# src/limit_orders.py
from src.logger import log_event
from src.client import get_client

def round_to_tick(price, tick_size):
    return round(price // tick_size * tick_size, 2)

def place_limit_order(symbol, side, quantity, price):
    client = get_client()
    try:
        # Get tick size for the symbol
        symbol_info = client.futures_exchange_info()
        tick_size = float([f['tickSize'] for s in symbol_info['symbols'] if s['symbol']==symbol for f in s['filters'] if f['filterType']=="PRICE_FILTER"][0])

        price = round_to_tick(price, tick_size)

        order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC"
        )
        msg = f"[LIMIT] {side} {quantity} {symbol} at {price} | OrderId={order['orderId']}"
        log_event(msg)
        return order
    except Exception as e:
        log_event(f"[ERROR] Limit order failed: {e}")
        return None
