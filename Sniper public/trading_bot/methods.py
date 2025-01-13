def get_state(data, t):
    """State representation for flash trading"""
    state = np.array([
        data['price'],
        data['volume'],
        data['bid_ask_spread'],
        data['order_book_imbalance'],
        data['volatility'],
        data['latency']
    ])
    return state.reshape(1, -1)

def train_model(agent, episode, data, ep_count=100, batch_size=32):
    """Training optimized for flash trading"""
    total_profit = 0
    data_length = len(data) - 1
    agent.inventory = []
    avg_loss = []

    state = get_state(data, 0)
    
    for t in tqdm(range(data_length)):
        reward = 0
        next_state = get_state(data, t + 1)
        
        # Quick market analysis
        microstructure = agent.analyze_market_microstructure(data)
        
        if not all(microstructure.values()):
            action = 0  # Hold if conditions unfavorable
        else:
            action = agent.act(state)
        
        # Execute flash trading strategy
        if action == 1:  # Buy
            entry_price = data['price'][t]
            trade_result = agent.execute_trade(data['token_address'], entry_price, action)
            
            if trade_result:
                # Calculate immediate reward based on spread capture
                exit_price = data['price'][t + 1]  # Next tick
                profit_pips = (exit_price - entry_price) / agent.tick_size
                
                if profit_pips >= agent.take_profit_pips:
                    reward = 1.0
                elif profit_pips <= -agent.stop_loss_pips:
                    reward = -1.0
                else:
                    reward = profit_pips / agent.take_profit_pips
            else:
                reward = -0.1  # Small penalty for failed execution
                
        elif action == 2:  # Sell
            if len(agent.inventory) > 0:
                bought_price = agent.inventory.pop(0)
                current_price = data['price'][t]
                profit_pips = (current_price - bought_price) / agent.tick_size
                reward = profit_pips / agent.take_profit_pips
        
        done = (t == data_length - 1)
        agent.remember(state, action, reward, next_state, done)
        
        if len(agent.memory) > batch_size:
            loss = agent.train_experience_replay(batch_size)
            avg_loss.append(loss)
            
        state = next_state
        
    return (episode, ep_count, total_profit, np.mean(np.array(avg_loss)))