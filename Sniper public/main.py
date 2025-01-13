from trading_bot.sniper import SolanaSniper
from config import Config
import logging
import coloredlogs
import time

def main():
    coloredlogs.install(level='INFO')
    logging.info("Initializing Solana sniper bot...")
    
    config = Config()
    sniper = SolanaSniper(config)
    
    if not config.API_KEY or config.API_KEY != "ABc1dE2fG3hI4jK5lM6nO7pQ":
        logging.error("Invalid API key")
        return
        
    if not config.SOLANA_KEY or config.SOLANA_KEY == "your_wallet_private_key_here":
        logging.error("Please set your Solana wallet private key in the .env file")
        return
        
    logging.info("Sniper bot initialized. Monitoring for opportunities...")
    
    while True:
        try:
            # Monitor for new token listings or price opportunities
            time.sleep(0.1)  # Fast polling for sniping
        except Exception as e:
            logging.error(f"Error in sniper loop: {e}")
            time.sleep(1)
    
if __name__ == "__main__":
    main()