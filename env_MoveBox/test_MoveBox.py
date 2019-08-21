from env_MoveBox import EnvMoveBox
import random
import matplotlib.pyplot as plt

env = EnvMoveBox()
max_iter = 100000
for i in range(max_iter):
    print("iter= ", i)
    plt.figure(figsize=(3, 3))
    plt.imshow(env.get_global_obs())
    plt.xticks([])
    plt.yticks([])
    plt.show()
    # env.render()
    action1 = random.randint(0, 3)
    action2 = random.randint(0, 3)
    reward, done = env.step([action1, action2])
    print('reward', reward)
    if reward > 0:
        print('reset')
