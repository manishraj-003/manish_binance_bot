# src/cli.py
import argparse
from src.market_orders import place_market_order
from src.limit_orders import place_limit_order
from src.advanced.twap import place_twap_order
# from src.advanced.oco import place_oco_order  # OCO commented for now

def main():
    parser = argparse.ArgumentParser(description="Binance Futures Trading Bot CLI")

    parser.add_argument("order_type", choices=["MARKET", "LIMIT", "TWAP"], 
                        help="Type of order to place")
    parser.add_argument("symbol", type=str, help="Trading symbol, e.g. BTCUSDT")
    parser.add_argument("side", choices=["BUY", "SELL"], help="Order side")
    parser.add_argument("quantity", type=float, help="Quantity to trade")
    
    # Optional arguments
    parser.add_argument("--price", type=float, help="Limit price (required for LIMIT)")
    parser.add_argument("--slices", type=int, default=5, help="Number of slices for TWAP")
    parser.add_argument("--delay", type=float, default=1.0, help="Delay between TWAP slices in seconds")

    args = parser.parse_args()

    if args.order_type == "MARKET":
        place_market_order(args.symbol, args.side, args.quantity)
    
    elif args.order_type == "LIMIT":
        if not args.price:
            print("Error: --price is required for LIMIT orders")
            return
        place_limit_order(args.symbol, args.side, args.quantity, args.price)
    
    elif args.order_type == "TWAP":
        place_twap_order(args.symbol, args.side, args.quantity, slices=args.slices, delay=args.delay)

if __name__ == "__main__":
    main()
