from env_SingleCatchPigs import EnvSingleCatchPigs
import random

env = EnvSingleCatchPigs(7)
max_iter = 10000
env.set_agent_at([2, 2], 0)
env.set_pig_at([4, 4], 0)
for i in range(max_iter):
    print("iter= ", i)
    env.render()
    action = random.randint(0, 4)
    print('action is', action)
    reward, done = env.step(action)
    print('reward', reward, 'done', done)
    if reward > 0:
        print('catch the pig', reward, done)

