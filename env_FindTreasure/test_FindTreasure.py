from env_FindTreasure import EnvFindTreasure
import random

env = EnvFindTreasure()

max_iter = 1000
for i in range(max_iter):
    print("iter= ", i)
    reward, obs_1, obs_2 = env.step(random.randint(0, 4), random.randint(0, 4))
    env.plot_scene()
    env.print_info()

