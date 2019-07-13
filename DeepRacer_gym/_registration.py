import gym


def _register_deepracer_env(id, env_name, **kwargs):
    entrypoint = 'DeepRacer_gym:{}'.format(env_name)

    gym.envs.registration.register(
        id=id,
        entry_point=entrypoint,
        max_episode_steps=9999999,
        reward_threshold=9999999,
        kwargs=kwargs,
        nondeterministic=False
    )


_register_deepracer_env('NewYorkCity-v0', 'NewYorkCityEnv', version=0)

make = gym.make

__all__ = [make.__name__]
