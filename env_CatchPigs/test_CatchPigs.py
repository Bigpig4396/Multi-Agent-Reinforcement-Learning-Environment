from env_CatchPigs import EnvCatchPigs
import random
import numpy as np

env = EnvCatchPigs()
'''
max_iter = 100
action1_list = np.random.randint(0, 4, size=[1, max_iter])
action2_list = np.random.randint(0, 4, size=[1, max_iter])
action_pig_list = np.random.randint(0, 3, size=[1, max_iter])
env.test(action1_list, action2_list, action_pig_list, max_iter, 1000, True)
'''


max_iter = 100
for i in range(max_iter):
    print("iter= ", i)
    env.step(random.randint(0, 4), random.randint(0, 4), random.randint(0, 3))
    print("agent 1 is at ", env.agt1_pos)
    print("agent 1 is looking at ", env.agt1_ori)
    print("agent 1 observation= ", env.get_agt1_obs())
    print("agent 2 is at ", env.agt2_pos)
    print("agent 2 is looking at ", env.agt2_ori)
    print("agent 2 observation= ", env.get_agt2_obs())
    print("pig is at ", env.pig_pos)
    print("pig is looking at ", env.pig_ori)
    print("pig observation= ", env.get_pig_obs())
