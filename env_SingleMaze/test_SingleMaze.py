from env_SingleMaze import EnvSingleMaze
import random

env = EnvSingleMaze()
max_iter = 10000
for i in range(max_iter):
    a_1 = random.randint(0, 3)
    print("action", a_1)
    env.plot_scene()
    reward_1, obs_1 = env.step(a_1)
    if reward_1 > 0:
        print("iter= ", i)
        print("find")
        print("agent 1 at", env.agt1_pos)

