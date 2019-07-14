import os
import sys
import time
import logging

from DeepRacer_gym import CustomRewardWrapper
from DeepRacer_gym import DeepRacerActionWrapper
import DeepRacer_gym as deepracer

LOG = logging.getLogger()

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

# Print action space info
print(env.action_space)

action_table = env.action_table()

# Print action table
print('Action number\t\tSteering\t\tSpeed')
for t in action_table:
    print('{}\t\t\t{}\t\t\t{}'.format(t['Action number'], t['Steering'], t['Speed']))


MAXIMUM_STEPS = 1000

state = env.reset()
for step in range(MAXIMUM_STEPS):

    action = env.action_space.sample() # random sample
    state, reward, done, info = env.step(action)

    LOG.info("[step {:4d}] action: ({:6.2f}, {:6.2f}), speed: {:10.6f}, steering: {:10.2f}, xy: ({:10.6f}, {:10.6f}), all_wheels_on_track: {}, closest_waypoints: {}".format(
                info['steps'], action_table[action]['Speed'], action_table[action]['Steering'], info['speed'], info['steering_angle'], info['x'], info['y'], info['all_wheels_on_track'], info['closest_waypoints']))


env.close()

