from env_FindGoals import EnvFindGoals
import random
import numpy as np

env = EnvFindGoals()
'''max_iter = 1000
action1_list = np.random.randint(0, 4, size=[1, max_iter])
action2_list = np.random.randint(0, 4, size=[1, max_iter])
env.test(action1_list, action2_list, max_iter, 100, True)
'''

max_iter = 100
for i in range(max_iter):
    print("iter= ", i)
    env.step(random.randint(0, 4), random.randint(0, 4))
    print("agent 1 is at ", env.agent1_pos)
    print("agent 1 observation= ", env.get_agt1_obs())
    print("agent 2 is at ", env.agent2_pos)
    print("agent 2 observation= ", env.get_agt2_obs())