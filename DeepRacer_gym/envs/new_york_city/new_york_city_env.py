import os
import sys
import time
import logging

import gym

from DeepRacer_gym.envs import UnityEnvBase
from DeepRacer_gym.utils.error import DeepRacerException
from DeepRacer_gym.utils import GoogleDriveDownloader


from .env_info import ENV_VERSION


class NewYorkCityEnv(gym.Env):
    metadata = {'render.modes': ['rgb_array']}

    def __init__(self, version, no_graphics=False):

        super(NewYorkCityEnv, self).__init__()


        env_version = ENV_VERSION.get(version, None)

        if env_version is None:
            DeepRacerException("invalid version number: {}".format(version))

        if not GoogleDriveDownloader.check_or_download(executable_path=env_version['executable_path'],
                                                       download_id=env_version['download_id'],
                                                       filename=env_version['filename']):
            raise DeepRacerException("Failed to download environment")


        self._env = UnityEnvBase(env_version['executable_path'], no_graphics=no_graphics)


        self.metadata = self._env.metadata
        self.reward_range = self._env.reward_range
        self.action_space = self._env.action_space
        self.observation_space = self._env.observation_space
        self.number_agents = self._env.number_agents


    def reset(self):
        return self._env.reset()

    def step(self, action):
        self._take_action(action)

        return self._current_step_info

    def _take_action(self, action): 
        obs, reward, done, info = self._env.step(action)

        vec_obs = info['vector_observations']

        observation = {}

        observation['all_wheels_on_track'] = vec_obs[0] > 0
        observation['x'] = vec_obs[1]
        observation['y'] = vec_obs[2]
        observation['distance_from_center'] = vec_obs[3]
        observation['is_left_of_center'] = vec_obs[4] > 0
        observation['heading'] = vec_obs[5]
        observation['progress'] = vec_obs[6]
        observation['steps'] = int(vec_obs[7])
        observation['speed'] = vec_obs[8]
        observation['steering_angle'] = vec_obs[9]
        observation['track_width'] = vec_obs[10]
        observation['waypoints_count'] = int(vec_obs[11])

        observation['waypoints'] = []

        

        for i in range( observation['waypoints_count'] ):
            x_index = 12 + i * 2
            y_index = 12 + i * 2 + 1
            observation['waypoints'].append( (vec_obs[x_index], vec_obs[y_index]) )

        observation['closest_waypoints'] = [int(vec_obs[-3]), int(vec_obs[-2])]
        observation['is_clear'] = vec_obs[-1] > 0
        observation['is_reversed'] = False

        self._current_step_info = (obs, reward, done, observation)

    def _get_reward(self):
        return self._current_step_info[1]

    def _seed(self):
        pass

    def render(self, mode='human', close=False):
        pass

    def close(self):
        try:
            self._env.close()
        except:
            pass

    def __del__(self):
        try:
            self._env.close()
        except:
            pass



