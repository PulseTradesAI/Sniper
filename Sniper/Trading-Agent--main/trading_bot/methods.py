def get_state(data, t):
    """State representation for sniping opportunities"""
    state = np.array([
        data['price'],
        data['liquidity'],
        data['time_since_listing'],
        data['holder_count'],
        data['transaction_count'],
        data['price_change_1m'],
        data['volume_1m'],
        data['unique_buyers_1m']
    ])
    return state.reshape(1, -1)

def train_model(agent, episode, data, ep_count=100, batch_size=32):
    """Training focused on sniping opportunities"""
    total_profit = 0
    data_length = len(data) - 1
    agent.inventory = []
    avg_loss = []

    state = get_state(data, 0)
    
    for t in tqdm(range(data_length)):
        reward = 0
        next_state = get_state(data, t + 1)
        
        # Get sniping signals
        token_safety = agent.check_token_safety(data['token_address'])
        
        if not all(token_safety.values()):
            action = 0  # Force skip if safety checks fail
        else:
            action = agent.act(state)
        
        # Execute snipe
        if action == 1:
            entry_price = data['price'][t]
            snipe_result = agent.execute_snipe(data['token_address'], data['suggested_amount'])
            
            if snipe_result:
                # Monitor position for quick exit
                for hold_time in range(agent.max_hold_time):
                    current_price = data['price'][t + hold_time]
                    profit_ratio = current_price / entry_price
                    
                    if profit_ratio >= agent.instant_sell_threshold:
                        reward = profit_ratio - 1  # Convert to percentage gain
                        break
                    elif hold_time == agent.max_hold_time - 1:
                        reward = (current_price / entry_price) - 1
            else:
                reward = -0.1  # Penalty for failed execution
        
        done = (t == data_length - 1)
        agent.remember(state, action, reward, next_state, done)
        
        if len(agent.memory) > batch_size:
            loss = agent.train_experience_replay(batch_size)
            avg_loss.append(loss)
            
        state = next_state
        
    return (episode, ep_count, total_profit, np.mean(np.array(avg_loss)))