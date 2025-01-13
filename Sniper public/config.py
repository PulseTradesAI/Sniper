import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('TRADING_API_KEY')
    SOLANA_RPC = os.getenv('SOLANA_RPC_ENDPOINT')
    SOLANA_KEY = os.getenv('SOLANA_WALLET_KEY')
    
    # Sniper Settings
    GAS_MULTIPLIER = 2.0        # Multiply gas price for faster transactions
    MAX_SLIPPAGE = 0.15         # 15% max slippage for sniping
    MIN_LIQUIDITY = 5           # Minimum liquidity in SOL
    BUY_TAX_LIMIT = 0.20        # Maximum buy tax (20%)
    SELL_TAX_LIMIT = 0.20       # Maximum sell tax (20%)
    
    # Anti-Rug Settings
    MIN_LP_LOCKED = 30          # Minimum LP lock time in days
    MAX_WALLET_SHARE = 0.05     # Maximum wallet concentration (5%)
    MIN_LP_SOL = 2              # Minimum LP in SOL
    
    # Trading Parameters
    AUTO_SELL = True            # Auto sell on profit target
    PROFIT_TARGET = 2.0         # 200% profit target
    STOP_LOSS = 0.5             # 50% stop loss
    MAX_BUY_AMOUNT = 2.0        # Maximum buy in SOL
    MIN_BUY_AMOUNT = 0.1        # Minimum buy in SOL
    
    # Speed & Gas Settings
    BLOCK_CONFIRMATIONS = 1     # Number of block confirmations to wait
    MAX_GAS_PRICE = 100000     # Maximum gas price in lamports
    TRANSACTION_TIMEOUT = 60    # Transaction timeout in seconds
    
    # Safety Settings
    MAX_DAILY_TRADES = 10       # Maximum trades per day
    MAX_CONCURRENT_SNIPES = 2   # Maximum concurrent snipe attempts
    BLACKLIST_TOKENS = []       # Blacklisted token addresses