import os
import sys
import time
import logging

from DeepRacer_gym import CustomRewardWrapper
from DeepRacer_gym import DeepRacerActionWrapper
import DeepRacer_gym as deepracer

from stable_baselines import PPO2
from stable_baselines.common.vec_env import SubprocVecEnv
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
def make_env():
    env = deepracer.make('NewYorkCity-v0')
    env = CustomRewardWrapper(env, reward_fn)
    env = DeepRacerActionWrapper(env, max_steering_angle = 30,
                                      steering_angle_granularity = 5,
                                      max_speed = 3,
                                      speed_granularity = 3)
    return env



MAX_TRAINING_STEPS = 5000
MAX_EVALUATE_STEPS = 1000



# Create Vec Env
env = SubprocVecEnv([make_env for i in range(6)])

model = PPO2(MlpPolicy, env, verbose=1)
model.learn(total_timesteps=MAX_TRAINING_STEPS)

env.close()



# Create new ENv
env = make_env()

states = env.reset()
for step in range(MAX_EVALUATE_STEPS):
    action, _states = model.predict(states)
    state, reward, done, info = env.step(action)

    if info['progress'] >= 99.99:
        print('Track complete')

env.close()

