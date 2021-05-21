from env_GoTogether import EnvGoTogether
import random

if __name__ == '__main__':
    env = EnvGoTogether(15)
    max_iter = 100000
    for i in range(max_iter):
        print("iter= ", i)
        env.plot_scene()
        action_list = [random.randint(0, 3), random.randint(0, 3)]
        reward, done = env.step(action_list)
        if done:
            print('find goal, reward', reward)
            env.reset()