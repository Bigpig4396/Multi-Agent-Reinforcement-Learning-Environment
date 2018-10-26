from env_CatchPigs import EnvCatchPigs
import random

env = EnvCatchPigs(7)
max_iter = 10000
for i in range(max_iter):
    print("iter= ", i)
    reward_1, reward_2, reward_pig, obs_1, obs_2, obs_pig = env.step(random.randint(0, 4), random.randint(0, 4), random.randint(0, 3))
    env.plot_scene()
    env.print_info()