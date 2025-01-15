from .agent import Agent
from .jupiter_client import JupiterClient
import logging
import asyncio
import time

class FlashTrader:
    def __init__(self, config):
        self.config = config
        self.jupiter = JupiterClient(config)
        self.agent = Agent(state_size=6)  # [price, volume, spread, imbalance, volatility, latency]
        self.active = True
        self.last_trade_time = 0
        self.min_trade_interval = 0.001  # 1ms minimum between trades
        
    async def run_trading_cycle(self):
        """Execute one flash trading cycle"""
        try:
            current_time = time.time()
            if current_time - self.last_trade_time < self.min_trade_interval:
                return  # Skip if too soon after last trade
                
            # Get market data with timeout
            market_data = await asyncio.wait_for(self._get_market_data(), timeout=0.001)
            if not market_data:
                return
                
            # Quick opportunity analysis
            if self._should_trade(market_data):
                # Get trading decision
                state = self._prepare_state(market_data)
                action = self.agent.act(state)
                
                # Execute trade through Jupiter if profitable
                if action > 0:  # 1 for buy, 2 for sell
                    success = await self._execute_jupiter_trade(action, market_data)
                    if success:
                        self.last_trade_time = time.time()
                    
        except asyncio.TimeoutError:
            pass  # Silently skip if timeout
        except Exception as e:
            logging.error(f"Trading cycle error: {e}")
            
    async def _execute_jupiter_trade(self, action, market_data):
        """Execute trade using Jupiter DEX"""
        try:
            quote = await self.jupiter.get_quote(
                market_data['input_mint'],
                market_data['output_mint'],
                market_data['amount']
            )
            
            if quote:
                return await self.jupiter.execute_swap(quote)
            return False
            
        except Exception as e:
            logging.error(f"Jupiter trade error: {e}")
            return False