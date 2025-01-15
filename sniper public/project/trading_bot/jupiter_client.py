import json
import base58
from solana.rpc.api import Client
from solana.transaction import Transaction
import requests

class JupiterClient:
    def __init__(self, config):
        self.config = config
        self.client = Client(config.SOLANA_RPC)
        self.base_url = "https://quote-api.jup.ag/v6"
        
    async def get_quote(self, input_mint, output_mint, amount):
        """Get Jupiter swap quote"""
        try:
            url = f"{self.base_url}/quote"
            params = {
                "inputMint": input_mint,
                "outputMint": output_mint,
                "amount": str(amount),
                "slippageBps": 50  # 0.5% slippage
            }
            
            response = requests.get(url, params=params)
            if response.status_code == 200:
                return response.json()
            return None
            
        except Exception as e:
            print(f"Error getting quote: {e}")
            return None

    async def execute_swap(self, quote_response):
        """Execute swap using Jupiter"""
        try:
            # Get serialized transaction
            url = f"{self.base_url}/swap"
            wallet_pubkey = base58.b58decode(self.config.SOLANA_WALLET_KEY).hex()
            
            swap_data = {
                "quoteResponse": quote_response,
                "userPublicKey": wallet_pubkey,
                "wrapUnwrapSOL": True
            }
            
            response = requests.post(url, json=swap_data)
            if response.status_code != 200:
                return None
                
            # Sign and send transaction
            swap_result = response.json()
            tx = Transaction.deserialize(swap_result['swapTransaction'])
            
            # Sign transaction with private key
            signed_tx = self.client.send_transaction(
                tx,
                self.config.SOLANA_WALLET_KEY,
                opts={"skip_preflight": True}
            )
            
            return signed_tx
            
        except Exception as e:
            print(f"Error executing swap: {e}")
            return None

    async def get_token_price(self, token_mint):
        """Get token price from Jupiter"""
        try:
            # Use USDC as price reference
            usdc_mint = "EPjFWdd5AufqSSqeM2qN1xzybapC8G4wEGGkZwyTDt1v"
            
            quote = await self.get_quote(token_mint, usdc_mint, 1_000_000)  # 1 token
            if quote:
                return float(quote['outAmount']) / 1_000_000  # Convert to USDC price
            return None
            
        except Exception as e:
            print(f"Error getting price: {e}")
            return None