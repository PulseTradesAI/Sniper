import random
from collections import deque
import numpy as np
import tensorflow as tf
import keras.backend as K
from keras.models import Sequential, load_model, clone_model
from keras.layers import Dense, LSTM
from keras.optimizers import Adam

class Agent:
    def __init__(self, state_size, strategy="t-dqn", reset_every=100, pretrained=False, model_name=None):
        self.strategy = strategy
        
        # Modified for Flash Trading
        self.state_size = state_size    # [price, volume, bid_ask_spread, order_book_imbalance, volatility, latency]
        self.action_size = 3            # [hold, buy, sell]
        self.model_name = model_name
        self.inventory = []
        self.memory = deque(maxlen=1000)  # Smaller memory for faster processing
        
        # Flash trading parameters
        self.min_spread = 0.0001        # Minimum spread to trade (1 pip)
        self.max_latency = 0.001        # Maximum acceptable latency (1ms)
        self.min_volume = 1000          # Minimum volume for liquidity
        self.tick_size = 0.00001        # Minimum price movement
        
        # Risk management
        self.position_ttl = 1           # Maximum hold time in seconds
        self.max_position_size = 0.02   # Maximum 2% of portfolio per trade
        self.stop_loss_pips = 2         # 2 pips stop loss
        self.take_profit_pips = 3       # 3 pips take profit
        self.max_trades_per_sec = 100   # Maximum trades per second
        self.max_open_positions = 5     # Maximum concurrent positions
        
        # Performance optimization
        self.batch_size = 32
        self.gamma = 0.50               # Lower gamma for immediate rewards
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.99       # Faster decay for quick adaptation
        self.learning_rate = 0.001
        self.loss = huber_loss
        self.optimizer = Adam(lr=self.learning_rate)

        if pretrained and self.model_name is not None:
            self.model = self.load()
        else:
            self.model = self._model()

    def _model(self):
        """Optimized model for microsecond decision making"""
        model = Sequential()
        model.add(Dense(64, activation="relu", input_dim=self.state_size))
        model.add(Dense(32, activation="relu"))
        model.add(Dense(self.action_size))
        model.compile(loss=self.loss, optimizer=self.optimizer)
        return model

    def analyze_market_microstructure(self, data):
        """Analyze order book and market microstructure"""
        return {
            'spread_opportunity': self._check_spread(data),
            'book_imbalance': self._calculate_order_imbalance(data),
            'execution_probability': self._estimate_fill_probability(data),
            'latency_check': self._verify_latency(data)
        }

    def act(self, state, is_eval=False):
        """Ultra-fast decision making"""
        # Extract microstructure metrics
        spread = state[2]
        imbalance = state[3]
        latency = state[5]
        
        # Instant reject conditions
        if latency > self.max_latency:
            return 0  # Hold if latency too high
        if spread < self.min_spread:
            return 0  # Hold if spread too tight
            
        # Use model for quick analysis
        action_probs = self.model.predict(state, batch_size=1)
        return np.argmax(action_probs[0])

    def execute_trade(self, token_address, price, action):
        """Execute trade with minimal latency"""
        try:
            if action == 1:  # Buy
                if len(self.inventory) >= self.max_open_positions:
                    return None
                
                tx = {
                    'type': 'IOC',  # Immediate-or-Cancel order
                    'price': price,
                    'time_in_force': 'IOC',
                    'post_only': True,
                    'stop_loss_pips': self.stop_loss_pips,
                    'take_profit_pips': self.take_profit_pips
                }
            else:  # Sell
                tx = {
                    'type': 'IOC',
                    'price': price,
                    'time_in_force': 'IOC',
                    'post_only': True
                }
            return self._send_transaction(token_address, tx)
        except Exception as e:
            return None

    def _check_spread(self, data):
        """Check if spread offers profitable opportunity"""
        spread = data['ask'] - data['bid']
        return spread >= self.min_spread

    def _verify_latency(self, data):
        """Verify current latency is within acceptable range"""
        return data['latency'] <= self.max_latency

    def _calculate_order_imbalance(self, data):
        """Calculate order book imbalance"""
        bid_volume = sum(data['bids'][:5])[1]  # Sum top 5 bid volumes
        ask_volume = sum(data['asks'][:5])[1]  # Sum top 5 ask volumes
        return (bid_volume - ask_volume) / (bid_volume + ask_volume)