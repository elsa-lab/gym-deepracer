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

## Example

```python
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
```
