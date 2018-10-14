from env_FindGoals import EnvFindGoals
import random
import numpy as np

env = EnvFindGoals()
max_iter = 1000
action1_list = np.random.randint(0, 4, size=[1, max_iter])
action2_list = np.random.randint(0, 4, size=[1, max_iter])
env.test(action1_list, action2_list, max_iter, 200, True)
