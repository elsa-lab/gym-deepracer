import os
import sys
import time
import logging

import gym

import numpy as np

from DeepRacer_gym.utils.error import DeepRacerException

class DeepRacerActionWrapper(gym.Wrapper):
    def __init__(self, env, max_steering_angle,
                            steering_angle_granularity,
                            max_speed,
                            speed_granularity):


        super(DeepRacerActionWrapper, self).__init__(env)

        self.env = env

        self.max_steering_angle = float(max_steering_angle)
        self.steering_angle_granularity = steering_angle_granularity
        self.max_speed = float(max_speed)
        self.speed_granularity = speed_granularity


        self._create_action_space()

    def _create_action_space(self):
        
        assert self.max_steering_angle >= 1 and self.max_steering_angle <= 30, DeepRacerException('invalid steering angle: {0}, values must be between 1 and 30'.format(self.max_steering_angle))

        assert isinstance(self.steering_angle_granularity, int) and self.steering_angle_granularity > 0, DeepRacerException('invalid steering angle granularity: {0}, values must greater than 0'.format(self.steering_angle_granularity))

        assert self.max_speed >= 0.8 and self.max_speed <= 8, DeepRacerException('invalid max speed: {0}, values must be between 0.8 and 8'.format(self.max_speed))

        assert isinstance(self.speed_granularity, int) and self.speed_granularity > 0, DeepRacerException('invalid speed granularity: {0}, values must greater than 0'.format(self.speed_granularity))

        self._speeds = np.linspace(0.0, self.max_speed, num=self.speed_granularity + 1, endpoint=True)[1:]

        #self._speeds = np.flip(
        #            np.linspace(self.max_speed, 0.0, num=self.speed_granularity, endpoint=False) )
        



        self._steering_angles = np.linspace( -self.max_steering_angle, self.max_steering_angle, num=self.steering_angle_granularity, endpoint=True)

        #self._steering_angles = np.flip(v)


        action_space_size = len(self._speeds) * len(self._steering_angles)
        self.action_space = gym.spaces.Discrete(action_space_size)



        self.action_list = []

        for i in range(action_space_size):

            self.action_list.append( 
                    (self._steering_angles[ i//len(self._speeds) ], self._speeds[ i%len(self._speeds) ] ) )


    def action(self, act):
        return list(self.action_list[act])

    def step(self, act):
        action = self.action(act)
        return self.env.step(action)

    def action_table(self):
        table = []

        for i, item in enumerate(self.action_list):
            table.append(
                    { 'Action number': i,
                      'Steering': item[0],
                      'Speed': item[1]
                    })


        return table

    def close(self):
        self.env.close()
