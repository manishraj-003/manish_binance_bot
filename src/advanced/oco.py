# src/advanced/oco.py
from src.logger import log_event
from src.client import get_client

def round_to_tick(price, tick_size):
    """Rounds price down to nearest tick size"""
    return round(price // tick_size * tick_size, 2)

def place_oco_order(symbol, side, quantity, price=None, stop_price=None):
    """
    Places a safe OCO order on Binance Futures Testnet.
    Automatically adjusts stop_price and take-profit if not safe.
    """
    client = get_client()
    try:
        # Get current price and tick size
        current_price = float(client.futures_symbol_ticker(symbol=symbol)['price'])
        symbol_info = client.futures_exchange_info()
        tick_size = float([
            f['tickSize'] 
            for s in symbol_info['symbols'] 
            if s['symbol']==symbol 
            for f in s['filters'] 
            if f['filterType']=="PRICE_FILTER"
        ][0])

        # If price not provided, set default TP/SL offsets
        if price is None:
            price = current_price * (1.02 if side.upper()=="SELL" else 0.98)  # TP default
        if stop_price is None:
            stop_price = current_price * (0.97 if side.upper()=="SELL" else 1.03)  # SL default

        # Round to tick size
        price = round_to_tick(price, tick_size)
        stop_price = round_to_tick(stop_price, tick_size)

        # Ensure stop_price is safely away from current price
        if side.upper() == "SELL" and stop_price >= current_price:
            stop_price = round_to_tick(current_price * 0.97, tick_size)
        elif side.upper() == "BUY" and stop_price <= current_price:
            stop_price = round_to_tick(current_price * 1.03, tick_size)

        # Place take-profit limit
        tp_order = client.futures_create_order(
            symbol=symbol,
            side=side,
            type="LIMIT",
            quantity=quantity,
            price=price,
            timeInForce="GTC"
        )

        # Place stop-loss
        stop_side = "SELL" if side.upper() == "BUY" else "BUY"
        sl_order = client.futures_create_order(
            symbol=symbol,
            side=stop_side,
            type="STOP_MARKET",
            stopPrice=stop_price,
            quantity=quantity
        )

        msg = f"[OCO] {side} {quantity} {symbol} | TP={price} SL={stop_price} | TP OrderId={tp_order['orderId']} SL OrderId={sl_order['orderId']}"
        log_event(msg)
        return {"take_profit": tp_order, "stop_loss": sl_order}

    except Exception as e:
        log_event(f"[ERROR] OCO order failed: {e}")
        return None
