import os
import sys
import time
import logging

from DeepRacer_gym import CustomRewardWrapper
from DeepRacer_gym import DeepRacerActionWrapper
import DeepRacer_gym as deepracer

from stable_baselines import PPO2
from stable_baselines.common.vec_env import DummyVecEnv
from stable_baselines.common.policies import MlpPolicy

# Define your custom reward function
def reward_fn(params):
    '''
    Example of using all_wheels_on_track and speed
    '''

    # Read input variables
    all_wheels_on_track = params['all_wheels_on_track']
    speed = params['speed']

    # Set the speed threshold based your action space
    SPEED_THRESHOLD = 1.0

    if not all_wheels_on_track:
        # Penalize if te car goes off track
        reward = 1e-3
    elif speed < SPEED_THRESHOLD:
        # Penalize if the car goes too slow
        reward = 0.5
    else:
        # High reward if the car stays on track and goes fast
        reward = 1.0

    return reward


# Create environment
env = deepracer.make('NewYorkCity-v0')
env = CustomRewardWrapper(env, reward_fn)
env = DeepRacerActionWrapper(env, max_steering_angle = 30,
                                  steering_angle_granularity = 5,
                                  max_speed = 3,
                                  speed_granularity = 3)

MAX_TRAINING_STEPS = 5000
MAX_EVALUATE_STEPS = 1000

# Create Dummy Env
env = DummyVecEnv([lambda: env])

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=MAX_TRAINING_STEPS)


states = env.reset()
for step in range(MAX_EVALUATE_STEPS):
    action, _states = model.predict(states)
    state, reward, done, info = env.step(action)

    if info['is_clear']:
        print("!!!Clear!!!")

env.close()

