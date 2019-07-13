import os
from .unity_env import UnityEnvBase
from .envs import NewYorkCityEnv
from .wrapper import DeepRacerActionWrapper, CustomRewardWrapper

from ._registration import make

dir_path = os.path.dirname(os.path.realpath(__file__))

os.environ['DEEPRACER_GYM_ROOT'] = dir_path

__all__ = [
    make.__name__,
    NewYorkCityEnv.__name__,
    DeepRacerActionWrapper.__name__,
    CustomRewardWrapper.__name__
]
