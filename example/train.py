import gym_gvgai
import os
from stable_baselines.deepq.policies import CnnPolicy
from stable_baselines import DQN  # test arbitrary agent
from stable_baselines.results_plotter import load_results, ts2xy
from stable_baselines.bench import Monitor
import numpy as np


best_mean_reward, n_steps = -np.inf, 0

def callback(_locals, _globals):
  """
  Callback called at each step (for DQN and others) or after n steps (see ACER or PPO2)
  :param _locals: (dict)
  :param _globals: (dict)
  """
  global n_steps, best_mean_reward
  # Print stats every 1000 calls
  if (n_steps + 1) % 1000 == 0:
      # Evaluate policy training performance
      x, y = ts2xy(load_results(log_dir), 'timesteps')
      if len(x) > 0:
          mean_reward = np.mean(y[-100:])
          print(x[-1], 'timesteps')
          print("Best mean reward: {:.2f} - Last mean reward per episode: {:.2f}".format(best_mean_reward, mean_reward))

          # New best model, you could save the agent here
          if mean_reward > best_mean_reward:
              best_mean_reward = mean_reward
              # Example for saving best model
              print("Saving new best model")
              _locals['self'].save(log_dir + 'best_model_gold_digger_lvl0.pkl')
  n_steps += 1
  return True


# Create log dir
log_dir = "/your_dir"
os.makedirs(log_dir, exist_ok=True)

env = gym_gvgai.make('gvgai-golddigger-lvl0-v0')
env = Monitor(env, log_dir, allow_early_resets=True)

model = DQN(CnnPolicy, env, verbose=1,prioritized_replay=True, buffer_size= 1000000, exploration_final_eps=0.1, train_freq=4)
model.learn(total_timesteps=int(1e6), callback=callback)

