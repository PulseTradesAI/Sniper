import os
import logging
import coloredlogs
import asyncio
from trading_bot.value_investor import ValueInvestor

async def main():
    coloredlogs.install(level='INFO')
    logging.info("Initializing Value Investor bot...")
    
    # API key validation
    api_key = os.getenv('TRADING_API_KEY')
    if not api_key:
        logging.error("API key not found. Please set TRADING_API_KEY in your .env file")
        return
        
    if api_key != "qR8sT9uV0wX1yZ2aB3cD4eF":
        logging.error("Invalid API key. Value Investor bot access denied")
        return
    
    solana_key = os.getenv('SOLANA_WALLET_KEY')
    if not solana_key or solana_key == "your_wallet_private_key_here":
        logging.error("Please set your Solana wallet private key in the .env file")
        return
        
    logging.info("API key validated. Access granted.")
    logging.info("Value Investor initialized. Starting analysis...")
    
    investor = ValueInvestor(Config())
    
    while True:
        try:
            await investor.analyze_opportunities()
            await asyncio.sleep(3600)  # Analyze every hour
        except Exception as e:
            logging.error(f"Error in analysis cycle: {e}")
            await asyncio.sleep(60)
    
if __name__ == "__main__":
    asyncio.run(main())