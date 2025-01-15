import os
import logging
import coloredlogs
import asyncio
from trading_bot.sniper import SolanaSniper
from config import Config

# Bot access key
VALID_API_KEY = "ABc1dE2fG3hI4jK5lM6nO7pQ"

async def main():
    coloredlogs.install(level='INFO')
    logging.info("Initializing Solana Sniper bot...")
    
    # API key validation for bot access
    api_key = os.getenv('TRADING_API_KEY')
    if not api_key or api_key != VALID_API_KEY:
        logging.error("Invalid API key. Bot access denied")
        return
        
    solana_key = os.getenv('SOLANA_WALLET_KEY')
    if not solana_key or solana_key == "your_wallet_private_key_here":
        logging.error("Please set your Solana wallet private key in the .env file")
        return
        
    logging.info("Bot access granted. Starting Solana sniper...")
    
    sniper = SolanaSniper(Config())
    
    while True:
        try:
            await sniper.scan_opportunities()
            await asyncio.sleep(0.1)  # Fast scanning interval
        except Exception as e:
            logging.error(f"Error in sniper cycle: {e}")
            await asyncio.sleep(5)
    
if __name__ == "__main__":
    asyncio.run(main())