# src/menu_cli.py
"""
Menu-driven CLI for the Binance Futures Bot with OCO support.
Run from project root:
    python -m src.menu_cli
Or (works too):
    python src/menu_cli.py
"""

# try absolute imports (when running as package), then fallback to relative imports
try:
    from src.market_orders import place_market_order
    from src.limit_orders import place_limit_order
    from src.advanced.twap import place_twap_order
    from src.advanced.oco import place_oco_order
    from src.logger import log_event
except Exception:
    # fallback when running inside src/ directly
    from market_orders import place_market_order
    from limit_orders import place_limit_order
    from advanced.twap import place_twap_order
    try:
        from advanced.oco import place_oco_order
    except Exception:
        place_oco_order = None
    from logger import log_event

def input_float(prompt, default=None):
    s = input(prompt).strip()
    if s == "" and default is not None:
        return default
    try:
        return float(s)
    except ValueError:
        print("Invalid number. Try again.")
        return None

def input_int(prompt, default=None):
    s = input(prompt).strip()
    if s == "" and default is not None:
        return default
    try:
        return int(s)
    except ValueError:
        print("Invalid integer. Try again.")
        return None

def safe_side(inp):
    s = inp.strip().upper()
    if s in ("BUY", "SELL"):
        return s
    print("Side must be BUY or SELL.")
    return None

def menu():
    while True:
        print("\n=== Binance Futures Bot (Menu CLI) ===")
        print("1. Market Order")
        print("2. Limit Order")
        print("3. TWAP Order")
        print("4. OCO Order (Take-profit + Stop-loss)")
        print("5. Exit")

        choice = input("Select an option (1-5): ").strip()

        if choice == "1":
            # Market
            symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
            side = None
            while side is None:
                side = safe_side(input("Side (BUY/SELL): "))
            qty = None
            while qty is None:
                qty = input_float("Quantity: ")
            log_event(f"[ACTION] Market order requested: {side} {qty} {symbol}")
            place_market_order(symbol, side, qty)

        elif choice == "2":
            # Limit
            symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
            side = None
            while side is None:
                side = safe_side(input("Side (BUY/SELL): "))
            qty = None
            while qty is None:
                qty = input_float("Quantity: ")
            price = None
            while price is None:
                price = input_float("Limit price: ")
            log_event(f"[ACTION] Limit order requested: {side} {qty} {symbol} @ {price}")
            place_limit_order(symbol, side, qty, price)

        elif choice == "3":
            # TWAP
            symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
            side = None
            while side is None:
                side = safe_side(input("Side (BUY/SELL): "))
            total_qty = None
            while total_qty is None:
                total_qty = input_float("Total quantity: ")
            slices = None
            while slices is None:
                slices = input_int("Number of slices (default 5): ", default=5)
            delay = None
            while delay is None:
                delay = input_float("Delay between slices in seconds (default 1.0): ", default=1.0)
            log_event(f"[ACTION] TWAP requested: {side} {total_qty} {symbol} in {slices} slices (delay {delay}s)")
            place_twap_order(symbol, side, total_qty, slices=slices, delay=delay)

        elif choice == "4":
            # OCO
            if place_oco_order is None:
                print("OCO functionality is not available (oco.py missing).")
                continue

            symbol = input("Symbol (e.g., BTCUSDT): ").strip().upper()
            side = None
            while side is None:
                side = safe_side(input("Side (BUY/SELL): "))
            qty = None
            while qty is None:
                qty = input_float("Quantity: ")

            # Optional TP and SL input; leave blank to auto-calc
            tp_input = input("Take-profit price (leave blank to auto-calc): ").strip()
            sl_input = input("Stop-loss (stop) price (leave blank to auto-calc): ").strip()

            tp = None
            sl = None
            try:
                if tp_input != "":
                    tp = float(tp_input)
            except ValueError:
                print("Invalid take-profit price; ignoring and will auto-calc.")

            try:
                if sl_input != "":
                    sl = float(sl_input)
            except ValueError:
                print("Invalid stop price; ignoring and will auto-calc.")

            log_event(f"[ACTION] OCO requested: {side} {qty} {symbol} TP={tp if tp is not None else 'AUTO'} SL={sl if sl is not None else 'AUTO'}")

            # Try to call place_oco_order with optional args if provided
            try:
                if tp is None and sl is None:
                    res = place_oco_order(symbol, side, qty)
                else:
                    # try keyword args first (handles newer function signatures)
                    try:
                        res = place_oco_order(symbol, side, qty, price=tp, stop_price=sl)
                    except TypeError:
                        # fallback to positional if signature differs
                        res = place_oco_order(symbol, side, qty, tp, sl)
                # optionally inspect res if needed
            except Exception as e:
                log_event(f"[ERROR] OCO placement failed in CLI: {e}")

        elif choice == "5":
            print("Exiting...")
            break

        else:
            print("Invalid choice. Please select 1-5.")

if __name__ == "__main__":
    menu()
