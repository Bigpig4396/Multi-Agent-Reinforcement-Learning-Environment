from env_Cleaner import EnvCleaner
import random

if __name__ == '__main__':
    env = EnvCleaner(2, 13, 0)
    max_iter = 1000
    for i in range(max_iter):
        print("iter= ", i)
        env.render()
        action_list = [random.randint(0, 3), random.randint(0, 3)]
        reward = env.step(action_list)
        print('reward', reward)