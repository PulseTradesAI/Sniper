import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('TRADING_API_KEY')
    SOLANA_RPC = os.getenv('SOLANA_RPC_ENDPOINT')
    SOLANA_KEY = os.getenv('SOLANA_WALLET_KEY')
    
    # Sniper Bot Parameters
    MIN_LIQUIDITY = 5000         # Minimum $5K liquidity
    MAX_SLIPPAGE = 0.03         # Maximum 3% slippage
    GAS_MULTIPLIER = 2          # 2x gas for faster execution
    
    # Token Safety Parameters
    MIN_LP_LOCKED = 30          # 30 days minimum LP lock
    MAX_WALLET_SHARE = 0.05     # Maximum 5% wallet concentration
    MIN_LP_SOL = 50            # Minimum 50 SOL in liquidity
    
    # Trading Limits
    MAX_CONCURRENT_SNIPES = 3   # Maximum concurrent snipe attempts
    MAX_DAILY_TRADES = 50       # Maximum trades per day
    MAX_GAS_PRICE = 10000      # Maximum gas price in Lamports
    
    # Position Management
    POSITION_SIZE = 0.01       # 1% of portfolio per position
    QUICK_FLIP = True         # Enable quick flip mode
    AUTO_SELL = True          # Enable auto sell
    
    # Take Profit / Stop Loss
    TP_TARGETS = [1.5, 2, 3]  # Take profit at 50%, 100%, 200%
    SL_PERCENTAGE = 0.15      # 15% stop loss
    TRAILING_STOP = 0.05      # 5% trailing stop when in profit
    
    # Performance Settings
    MAX_BUY_TAX = 0.10       # Maximum 10% buy tax
    MAX_SELL_TAX = 0.10      # Maximum 10% sell tax
    MIN_BLOCK_TIME = 2       # Minimum blocks before buying