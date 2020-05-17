from gym.envs.registration import register

register(
    id='BlackJack-v0',
    entry_point='gym_BlackJack.envs:BlackJackEnv',
)
