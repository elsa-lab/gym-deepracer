# DeepRacer Gym

## Param List
* More info: [AWS DeepRacer Developer Guide](https://docs.aws.amazon.com/en_us/deepracer/latest/developerguide/deepracer-reward-function-input.html)
```
{
    "all_wheels_on_track": Boolean,    # flag to indicate if the vehicle is on the track
    "x": float,                        # vehicle's x-coordinate in meters
    "y": float,                        # vehicle's y-coordinate in meters
    "distance_from_center": float,     # distance in meters from the track center 
    "is_left_of_center": Boolean,      # Flag to indicate if the vehicle is on the left side to the track center or not. 
    "heading": float,                  # vehicle's yaw in degrees
    "progress": float,                 # percentage of track completed
    "steps": int,                      # number steps completed
    "speed": float,                    # vehicle's speed in meters per second (m/s)
    "steering_angle": float,           # vehicle's steering angle in degrees
    "track_width": float,              # width of the track
    "waypoints": [[float, float], … ], # list of [x,y] as milestones along the track center
    "closest_waypoints": [int, int]    # indices of the two nearest waypoints.
}
```

## Example 1

```python
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


MAXIMUM_STEPS = 5000

done = True
for step in range(MAXIMUM_STEPS):
    if done:
        state = env.reset()

    action = env.action_space.sample() # random sample
    state, reward, done, info = env.step(action)


    LOG.info("[step {:4d}] action: ({:10.2f}, {:10.2f}), speed: {:10.6f}, steering: {:10.2f}, xy: ({:10.6f}, {:10.6f}), all_wheels_on_track: {}, closest_waypoints: {}".format(
                step, action_table[action]['Speed'], action_table[action]['Steering'], info['speed'], info['steering_angle'], info['x'], info['y'], info['all_wheels_on_track'], info['closest_waypoints']))


env.close()
```


## Example 2: Integrating with stable_baselines

```python
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
```
