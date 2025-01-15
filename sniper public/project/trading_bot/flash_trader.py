from .agent import Agent
from .solana_client import SolanaClient
import logging
import asyncio
import time

class FlashTrader:
    def __init__(self, config):
        self.config = config
        self.solana_client = SolanaClient(config)
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
                
            # Quick spread check
            if market_data['bid_ask_spread'] < self.config.MIN_SPREAD:
                return
                
            # Latency check
            if market_data['latency'] > self.config.MAX_LATENCY:
                return
                
            # Ultra-fast market analysis
            if self._should_trade(market_data):
                # Get trading decision
                state = self._prepare_state(market_data)
                action = self.agent.act(state)
                
                # Execute trade if profitable opportunity exists
                if action > 0:  # 1 for buy, 2 for sell
                    success = await self._execute_flash_trade(action, market_data)
                    if success:
                        self.last_trade_time = time.time()
                    
        except asyncio.TimeoutError:
            pass  # Silently skip if timeout
        except Exception as e:
            logging.error(f"Flash trading cycle error: {e}")
            
    def _should_trade(self, data):
        """Ultra-fast trade opportunity check"""
        return (
            data['bid_ask_spread'] >= self.config.MIN_SPREAD and
            data['latency'] <= self.config.MAX_LATENCY and
            data['volume'] >= self.config.MIN_VOLUME
        )
            
    async def _get_market_data(self):
        """Fast market data fetch"""
        try:
            # Implement fast market data fetching here
            # This should connect directly to exchange websocket
            return {
                'price': 0,
                'volume': 0,
                'bid_ask_spread': 0,
                'order_book_imbalance': 0,
                'volatility': 0,
                'latency': 0
            }
        except Exception as e:
            return None
            
    def _prepare_state(self, market_data):
        """Prepare minimal state for decision"""
        return [
            market_data['price'],
            market_data['volume'],
            market_data['bid_ask_spread'],
            market_data['order_book_imbalance'],
            market_data['volatility'],
            market_data['latency']
        ]
        
    async def _execute_flash_trade(self, action, market_data):
        """Execute flash trade with minimal latency"""
        try:
            # Use IOC (Immediate-or-Cancel) orders for flash trading
            order = {
                'type': 'IOC',
                'price': market_data['price'],
                'time_in_force': 'IOC',
                'post_only': True
            }
            
            # Execute with timeout
            success = await asyncio.wait_for(
                self.solana_client.execute_trade(order),
                timeout=0.001
            )
            return success
            
        except (asyncio.TimeoutError, Exception) as e:
            return False