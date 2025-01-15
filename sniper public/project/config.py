import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    API_KEY = os.getenv('TRADING_API_KEY')
    SOLANA_RPC = os.getenv('SOLANA_RPC_ENDPOINT')
    SOLANA_KEY = os.getenv('SOLANA_WALLET_KEY')
    
    # Sniper Settings
    MIN_LP_SOL = 50              # Minimum 50 SOL liquidity
    MAX_WALLET_SHARE = 0.03      # Maximum 3% in single wallet
    MIN_LP_LOCKED = 180          # Minimum 180 days LP lock
    MAX_BUY_TAX = 0.10          # Maximum 10% buy tax
    MAX_SELL_TAX = 0.10         # Maximum 10% sell tax
    
    # Trading Parameters
    MAX_CONCURRENT_SNIPES = 3    # Maximum concurrent snipe attempts
    MAX_DAILY_TRADES = 50        # Maximum trades per 24h
    MIN_PROFIT_TARGET = 0.30     # Minimum 30% profit target
    MAX_SLIPPAGE = 0.02         # Maximum 2% slippage
    GAS_BOOST = 2               # Gas price multiplier for sniping
    
    # Risk Management
    STOP_LOSS = 0.10           # 10% stop loss
    TRAILING_STOP = 0.05       # 5% trailing stop when in profit
    MAX_POSITION_SIZE = 0.05   # Maximum 5% of portfolio per position
    AUTO_SELL = True          # Enable auto sell at targets
    
    # Safety Checks
    CHECK_HONEYPOT = True     # Check for honeypot
    CHECK_LP_LOCK = True      # Verify LP lock
    CHECK_CONTRACT = True     # Basic contract audit
    VERIFY_OWNERSHIP = True   # Check contract ownership
    
    # Performance
    EXECUTION_TIMEOUT = 3     # Maximum 3s execution time
    MIN_EXECUTION_SPEED = 0.5 # Minimum 500ms execution speed
    MEMPOOL_SCAN_INTERVAL = 0.1 # 100ms mempool scan interval