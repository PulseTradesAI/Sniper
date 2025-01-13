import random
from collections import deque
import numpy as np
import tensorflow as tf
import keras.backend as K
from keras.models import Sequential, load_model, clone_model
from keras.layers import Dense, LSTM
from keras.optimizers import Adam

class Agent:
    def __init__(self, state_size, strategy="t-dqn", reset_every=1000, pretrained=False, model_name=None):
        self.strategy = strategy
        
        # Modified for Solana DEX Sniping
        self.state_size = state_size    # [price, liquidity, time_since_listing, holder_count, tx_count]
        self.action_size = 2            # [skip, snipe]
        self.model_name = model_name
        self.inventory = []
        self.memory = deque(maxlen=10000)
        
        # Sniping specific parameters
        self.min_liquidity = 5000       # Minimum liquidity in USDC
        self.max_slippage = 0.15        # Maximum 15% slippage
        self.min_holders = 10           # Minimum unique holders
        self.max_buy_amount = 0.05      # Maximum 5% of liquidity
        self.instant_sell_threshold = 3  # Sell if 3x profit reached
        self.max_hold_time = 300        # Max hold time in seconds
        self.gas_priority = "high"      # Priority for transaction execution
        
        # Anti-rug parameters
        self.min_team_tokens_locked = 0.5  # 50% of team tokens must be locked
        self.min_lock_time = 180 * 24 * 3600  # 180 days lock minimum
        self.max_team_wallet_size = 0.05  # Max 5% of supply per team wallet
        
        # Model config
        self.gamma = 0.99               # Higher gamma for longer-term considerations
        self.epsilon = 1.0
        self.epsilon_min = 0.01
        self.epsilon_decay = 0.995
        self.learning_rate = 0.001
        self.loss = huber_loss
        self.optimizer = Adam(lr=self.learning_rate)

        if pretrained and self.model_name is not None:
            self.model = self.load()
        else:
            self.model = self._model()

    def _model(self):
        """Specialized model for sniping opportunities"""
        model = Sequential()
        model.add(Dense(256, activation="relu", input_dim=self.state_size))
        model.add(Dense(512, activation="relu"))
        model.add(Dense(256, activation="relu"))
        model.add(Dense(self.action_size))
        model.compile(loss=self.loss, optimizer=self.optimizer)
        return model

    def act(self, state, is_eval=False):
        """Quick decision making for sniping opportunities"""
        # Extract key metrics
        liquidity = state[1]
        time_since_listing = state[2]
        holder_count = state[3]
        
        # Quick rejection conditions
        if liquidity < self.min_liquidity:
            return 0  # Skip if liquidity too low
        if holder_count < self.min_holders:
            return 0  # Skip if too few holders
            
        # Instant snipe conditions
        if time_since_listing < 60 and liquidity > self.min_liquidity * 2:
            return 1  # Instant snipe on new listings with good liquidity
            
        # Use model for other cases
        action_probs = self.model.predict(state)
        return np.argmax(action_probs[0])

    def check_token_safety(self, token_contract):
        """Verify token contract safety"""
        return {
            'honeypot_safe': self._check_honeypot(token_contract),
            'team_tokens_locked': self._verify_token_locks(token_contract),
            'contract_verified': self._check_contract_verification(token_contract),
            'ownership_renounced': self._check_ownership(token_contract)
        }

    def execute_snipe(self, token_address, amount):
        """Execute sniping transaction with high priority"""
        try:
            # Prepare transaction with high gas priority
            tx = {
                'gas_priority': self.gas_priority,
                'slippage': self.max_slippage,
                'amount': min(amount, self.max_buy_amount),
                'deadline': 60  # 1 minute deadline
            }
            return self._send_transaction(token_address, tx)
        except Exception as e:
            return None