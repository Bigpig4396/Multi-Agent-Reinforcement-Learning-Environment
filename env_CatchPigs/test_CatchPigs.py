from env_CatchPigs import EnvCatchPigs
import random

env = EnvCatchPigs(9, True)
max_iter = 10000
for i in range(max_iter):
    a_1 = random.randint(0, 4)
    a_2 = random.randint(0, 4)
    a_pig = random.randint(0, 3)
    #print("iter= ", i, env.agt1_pos, env.agt2_pos, env.pig_pos, env.agt1_ori, env.agt2_ori, a_1, a_2)
    reward_1, reward_2, reward_pig, obs_1, obs_2, obs_pig = env.step(a_1, a_2, a_pig)
    env.plot_scene()
    if reward_1 > 0:
        print("iter= ", i)
        print("agent 1 finds goal")
        #env.plot_scene()


