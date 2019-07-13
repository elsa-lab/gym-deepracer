import os
import sys
import time
import logging

import gym

from DeepRacer_gym import UnityEnvBase
from DeepRacer_gym.utils.error import DeepRacerException
from DeepRacer_gym.utils import GoogleDriveDownloader


current_dir = os.path.dirname(os.path.realpath(__file__))

ENV_VERSION = {
        0: {'executable_path': os.path.join(current_dir, 'executable/v0/new_york_city.x86_64'),
            'download_id': '15Z9vtfh_ZQGv9jNdVqnZEYwsdjWb9Rvd',
            'filename': os.path.join(current_dir, 'executable/v0.zip')}
        
        1: {'executable_path': os.path.join(current_dir, 'executable/v1/new_york_city.x86_64'),
            'download_id': '1Qo1t6fraKSxjyuOw-oTmX2xesN6m_8ir',
            'filename': os.path.join(current_dir, 'executable/v1.zip')}
}


class NewYorkCityEnv(UnityEnvBase):
    def __init__(self, version):

        env_version = ENV_VERSION.get(version, None)

        if env_version is None:
            DeepRacerException("invalid version number: {}".format(version))

        if not GoogleDriveDownloader.check_or_download(executable_path=env_version['executable_path'],
                                                       download_id=env_version['download_id'],
                                                       filename=env_version['filename']):
            DeepRacerException("Failed to download environment")

        super(NewYorkCityEnv, self).__init__(env_version['executable_file'], True, False)

    def _reset(self):
        return super(NewYorkCityEnv, self)._reset()

    def _step(self, action):
        self._take_action(action)

        return self._current_step_info

    def _take_action(self, action): 
        obs, reward, done, info = super(NewYorkCityEnv, self)._step(action)

        vec_obs = info['vector']

        observation = {}

        observation['all_wheels_on_track'] = vec_obs[0] > 0
        observation['x'] = vec_obs[1]
        observation['y'] = vec_obs[2]
        observation['distance_from_center'] = vec_obs[3]
        observation['is_left_of_center'] = vec_obs[4] > 0
        observation['heading'] = vec_obs[5]
        observation['progress'] = vec_obs[6]
        observation['steps'] = vec_obs[7]
        observation['speed'] = vec_obs[8]
        observation['steering_angle'] = vec_obs[9]
        observation['track_width'] = vec_obs[10]
        observation['waypoints_count'] = vec_obs[11]

        observation['waypoints'] = []

        for i in range(observation['waypoints_count']):
            x_index = 12 + i * 2
            y_index = 12 + i * 2 + 1
            observation['waypoints'].append( (vec_obs[x_index], vec_obs[y_index]) )

        observation['closest_waypoints'] = [vec_obs[-2], vec_obs[-1]]

        observation['is_reversed'] = False

        self._current_step_info = (obs, reward, done, observation)

    def _get_reward(self):
        return self._current_step_info[1]

    def _render(self, mode='human', close=False):
        pass

    def close(self):
        super(NewYorkCityEnv, self).close()

