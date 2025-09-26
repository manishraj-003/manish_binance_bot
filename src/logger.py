# src/logger.py
import logging

# Configure logging
logging.basicConfig(
    filename="bot.log",
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
)

def log_event(message):
    print(message)  # Also show on console
    logging.info(message)
