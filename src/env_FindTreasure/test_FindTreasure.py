
from env_FindTreasure import EnvFindTreasure
import random

if __name__ == '__main__':
    env = EnvFindTreasure(7)
    max_iter = 1000
    for i in range(max_iter):
        print("iter= ", i)
        env.render()
        #env.plot_scene()
        action_list = [random.randint(0, 3), random.randint(0, 3)]
        print()
        reward, done = env.step(action_list)
        if done:
            print('find goal, reward', reward)
            env.reset()