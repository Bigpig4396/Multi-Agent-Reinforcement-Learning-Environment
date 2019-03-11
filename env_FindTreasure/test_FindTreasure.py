from env_FindTreasure import EnvFindTreasure
import random

if __name__ == '__main__':
    env = EnvFindTreasure()

    max_iter = 1000
    for i in range(max_iter):
        print("iter= ", i)
        action_list = [random.randint(0, 4), random.randint(0, 4)]
        reward_list, done = env.step(action_list)

        env.plot_scene()



