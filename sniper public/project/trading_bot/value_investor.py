import logging
from .value_analyzer import ValueAnalyzer
from .solana_client import SolanaClient
import asyncio

class ValueInvestor:
    def __init__(self, config):
        self.config = config
        self.analyzer = ValueAnalyzer(config)
        self.solana_client = SolanaClient(config)
        self.positions = {}
        self.last_rebalance = None
        
    async def analyze_opportunities(self):
        """Analyze investment opportunities"""
        try:
            logging.info("Analyzing market for value opportunities...")
            
            # Get potential tokens
            tokens = await self._get_token_list()
            opportunities = []
            
            for token in tokens:
                # Check value criteria
                is_valuable, reason = await self.analyzer.check_investment_criteria(token)
                if is_valuable:
                    score = await self.analyzer.analyze_token(token)
                    if score >= 0.7:  # 70% minimum score
                        opportunities.append((token, score))
            
            # Sort by value score
            opportunities.sort(key=lambda x: x[1], reverse=True)
            
            # Take positions in top opportunities
            for token, score in opportunities[:self.config.MAX_POSITIONS]:
                if token not in self.positions:
                    await self._take_position(token)
                    
            # Monitor existing positions
            await self._monitor_positions()
            
        except Exception as e:
            logging.error(f"Analysis failed: {e}")
            
    async def _take_position(self, token):
        """Take a new position"""
        try:
            # Calculate position size
            portfolio_value = await self._get_portfolio_value()
            position_size = portfolio_value * self.config.MAX_POSITION_SIZE
            
            # Execute buy through Jupiter
            success = await self.solana_client.execute_trade(
                token,
                position_size,
                "buy"
            )
            
            if success:
                entry_price = await self.solana_client.get_token_price(token)
                self.positions[token] = {
                    'entry_price': entry_price,
                    'size': position_size,
                    'stop_loss': entry_price * (1 - self.config.STOP_LOSS),
                    'take_profit': entry_price * (1 + self.config.TAKE_PROFIT)
                }
                logging.info(f"Took position in {token}")
                
        except Exception as e:
            logging.error(f"Failed to take position: {e}")
            
    async def _monitor_positions(self):
        """Monitor existing positions"""
        for token in list(self.positions.keys()):
            try:
                current_price = await self.solana_client.get_token_price(token)
                position = self.positions[token]
                
                # Check stop loss and take profit
                if current_price <= position['stop_loss']:
                    await self._close_position(token, "stop loss")
                elif current_price >= position['take_profit']:
                    await self._close_position(token, "take profit")
                    
            except Exception as e:
                logging.error(f"Error monitoring {token}: {e}")
                
    async def _close_position(self, token, reason):
        """Close an existing position"""
        try:
            position = self.positions[token]
            success = await self.solana_client.execute_trade(
                token,
                position['size'],
                "sell"
            )
            
            if success:
                exit_price = await self.solana_client.get_token_price(token)
                profit_pct = (exit_price - position['entry_price']) / position['entry_price']
                logging.info(f"Closed position in {token} ({reason}). Profit: {profit_pct:.2%}")
                del self.positions[token]
                
        except Exception as e:
            logging.error(f"Failed to close position: {e}")
            
    async def _get_portfolio_value(self):
        """Get total portfolio value"""
        # Implement portfolio value calculation
        return 1000  # Placeholder