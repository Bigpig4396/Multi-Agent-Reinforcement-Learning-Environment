from env_CatchPigs import EnvCatchPigs
import random
import numpy as np

env = EnvCatchPigs()
max_iter = 100
action1_list = np.random.randint(0, 4, size=[1, max_iter])
action2_list = np.random.randint(0, 4, size=[1, max_iter])
action_pig_list = np.random.randint(0, 3, size=[1, max_iter])
env.test(action1_list, action2_list, action_pig_list, max_iter, 1000, True)
