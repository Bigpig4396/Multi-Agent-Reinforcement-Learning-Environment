from env_Navigation import EnvNavigation
import matplotlib.pyplot as plt
import random

env = EnvNavigation()
fig = plt.figure()
max_MC_iter = 2000
plt.xticks([])
plt.yticks([])
for MC_iter in range(max_MC_iter):
    print(MC_iter)
    plt.xticks([])
    plt.yticks([])
    plt.imshow(env.get_global_obs())

    # add random velocity
    reward = env.step([20*(random.random()-0.5), 20*(random.random()-0.5), 20*(random.random()-0.5)])
    plt.pause(.04)
    plt.draw()