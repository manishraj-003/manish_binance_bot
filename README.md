\# Binance Futures Trading Bot



\## Overview

This is a \*\*CLI-based trading bot for Binance USDT-M Futures\*\* that supports multiple order types, including Market, Limit, and TWAP (Time-Weighted Average Price). The bot includes \*\*robust logging, input validation\*\*, and a \*\*menu-driven interactive CLI\*\* for ease of use.  



\*\*Note:\*\* OCO (One-Cancels-the-Other) orders are implemented but can be commented out on testnet if triggering `-2021` errors.



---



\## Features



\### Core Orders (Mandatory)

\- \*\*Market Orders\*\* – Immediate execution at current market price.

\- \*\*Limit Orders\*\* – Executes at a specified price.



\### Advanced Orders (Optional / Bonus)

\- \*\*TWAP Orders\*\* – Split large orders into smaller slices over time.

\- \*\*OCO Orders\*\* – Place take-profit and stop-loss simultaneously (optional).



\### Validation \& Logging

\- Input validation: symbol, side, quantity, price thresholds.

\- Structured logs in `bot.log` with timestamps and errors.

\- Safe price calculations (tick size alignment) for Limit/TWAP/OCO orders.



---



\## Project Structure

│

├── src/

│ ├── client.py # Binance API client setup

│ ├── logger.py # log\_event() utility

│ ├── market\_orders.py # Market order logic

│ ├── limit\_orders.py # Limit order logic

│ ├── menu\_cli.py # Menu-driven interactive CLI

│ └── advanced/

│ ├── oco.py # OCO order logic (optional)

│ └── twap.py # TWAP order strategy

│

├── bot.log # Logs of order executions and errors

├── report.pdf # Screenshots + analysis

└── README.md # Setup and usage instructions



---



\## Setup Instructions



1\. \*\*Clone the repository\*\* or unzip the submission folder.

2\. \*\*Install Python 3.10+\*\* if not already installed.

3\. \*\*Install dependencies\*\*:



```bash

pip install python-binance python-dotenv





Create a .env file in \[project\_root] with your testnet API credentials:



API\_KEY="your\_testnet\_api\_key"

API\_SECRET="your\_testnet\_api\_secret"





Use Binance Futures Testnet: https://testnet.binancefuture.com



\##How to Run



Menu-driven Interactive CLI (menu\_cli.py)

python -m src.menu\_cli



Logs

All actions and errors are logged in bot.log:



\[MARKET] BUY 0.01 BTCUSDT | OrderId=5679698279

\[LIMIT] SELL 0.01 BTCUSDT at 27000 | OrderId=5679698301

\[TWAP] BUY 0.0100 BTCUSDT (slice 1/5)

\[ERROR] Limit order failed: APIError(...)

