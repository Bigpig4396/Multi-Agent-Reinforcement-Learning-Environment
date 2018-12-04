from env_SingleCatchPigs import EnvSingleCatchPigs
import random

env = EnvSingleCatchPigs(True)
max_iter = 10000
env.set_agent_at([2, 2], 0)
env.set_pig_at([4, 4], 0)
for i in range(max_iter):
    a_1 = random.randint(0, 4)
    a_pig = random.randint(0, 3)
    print("iter= ", i, env.agt1_pos, env.pig_pos, env.agt1_ori, env.pig_ori, a_1)
    env.plot_scene()
    reward_1, reward_pig, obs_1, obs_pig = env.step(a_1, a_pig)

    if reward_1 > 0:
        print("agent 1 finds goal")
        env.plot_scene()