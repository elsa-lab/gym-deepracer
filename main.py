import os
import sys
import time
import logging


from DeepRacer_gym import CustomRewardWrapper
from DeepRacer_gym import DeepRacerActionWrapper
import DeepRacer_gym as deepracer

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
env = deepracer.make('NewYorkCityEnv-v0')
env = CustomRewardWrapper(env, reward_fn)
env = DeepRacerActionWrapper(env, max_steering_angle = 30,
                                  steering_angle_granularity = 5,
                                  max_speed = 1,
                                  speed_granularity = 2)

# Print out action space info
print(env.action_space)

# Print out action table
print('Action number\t\tSteering\t\tSpeed')
for t in env.action_table():
    print('{}\t\t\t{}\t\t{}'.format(t['Action number'], t['Steering'], t['Speed']))


MAXIMUM_STEPS = 5000

done = True
for step in range(MAXIMUM_STEPS):
    if done:
        state = env.reset()
    state, reward, done, info = env.step(env.action_space.sample())

env.close()

