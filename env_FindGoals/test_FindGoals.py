from env_FindGoals import EnvFindGoals
import random

env = EnvFindGoals()
max_iter = 100
for i in range(max_iter):
    print("iter= ", i)
    reward_1, reward_2, obs_1, obs_2 = env.step(random.randint(0, 4), random.randint(0, 4))
    env.plot_scene()
    # env.print_info()
    if reward_1 > 0:
        print("agent 1 finds goal")
    if reward_2 > 0:
        print("agent 2 finds goal")

