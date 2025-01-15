from solana.rpc.api import Client
from .jupiter_client import JupiterClient
import numpy as np
import time

class SolanaClient:
    def __init__(self, config):
        self.client = Client(config.SOLANA_RPC)
        self.jupiter = JupiterClient(config)
        self.config = config
        
    async def get_token_price(self, token_address):
        """Get current price of token using Jupiter"""
        return await self.jupiter.get_token_price(token_address)
            
    async def execute_trade(self, token_address, amount, side):
        """Execute trade using Jupiter"""
        try:
            # USDC mint address
            usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
            
            if side == "buy":
                input_mint = usdc_mint
                output_mint = token_address
            else:
                input_mint = token_address
                output_mint = usdc_mint
                
            # Get quote
            quote = await self.jupiter.get_quote(input_mint, output_mint, amount)
            if not quote:
                return False
                
            # Execute swap
            result = await self.jupiter.execute_swap(quote)
            return result is not None
            
        except Exception as e:
            print(f"Trade execution error: {e}")
            return False