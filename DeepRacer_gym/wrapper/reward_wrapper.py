import os
import sys
import time
import logging

from inspect import signature

import gym

from DeepRacer_gym.utils.error import DeepRacerException


class CustomRewardWrapper(gym.Wrapper):
    def __init__(self, env, reward_fn):

        super(CustomRewardWrapper, self).__init__(env)
        self.env = env

        sig = signature(reward_fn)
        param_num = len(sig.parameters)

        assert param_num == 1, DeepRacerException('reward_fn must take 1 argument: reward_fn(obs)')

        self.reward_fn = reward_fn

    def reset(self):
        observation = self.env.reset()
        return observation

    def step(self, action):
        observation, reward, done, info = self.env.step(action)

        return observation, self.reward(info), done, info

    def reward(self, info):
        return self.reward_fn(info)
