import os
import sys
import time
import logging

import itertools
import gym
import numpy as np
from gym_unity.envs.unity_env import UnityEnv


class UnityEnvBase(UnityEnv):
    
    worker_id = 0
    env_pool = {}

    def __init__(
        self,
        env_filename: str,
        use_visual=True,
        no_graphics=False
        ):

        self.worker_id = UnityEnvBase.worker_id
        UnityEnvBase.worker_id += 1
        UnityEnvBase.env_pool[self.worker_id] = self

        super(UnityEnvBase, self).__init__(env_filename, use_visual, True, False, False, no_graphics, False)

    def _reset(self):
        return self.reset()

    def _step(self, action):
        self._take_action(action)

        return self._current_obs, self._current_reward, self._current_done, self._current_info

    def _take_action(self, action):
        obs, reward, done, info = self.step(action)

        info = {"vector": info.vector_observations[0, :], "brain_info": info}

        self._current_obs = obs
        self._current_reward = reward
        self._current_done = done
        self._current_info = info

    def _get_reward(self):
        return self._current_reward

    def _render(self, mode='human', close=False):
        pass

    def close(self):
        self._env.close()
        del UnityEnvBase.env_pool[self.worker_id]

    @staticmethod
    def getEnv(worker_id):
        return UnityEnvBase.env_pool.get(work_id, None)
