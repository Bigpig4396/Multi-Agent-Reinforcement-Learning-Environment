from env_MoveBox import EnvMoveBox
import random

env = EnvMoveBox()
max_iter = 100000
for i in range(max_iter):
    print("iter= ", i)
    #env.plot_scene()
    env.render()
    action1 = random.randint(0, 3)
    action2 = random.randint(0, 3)
    reward_list = env.step([action1, action2])
    print('reward', reward_list[0])
    if reward_list[0] > 0:
        print('reset')
