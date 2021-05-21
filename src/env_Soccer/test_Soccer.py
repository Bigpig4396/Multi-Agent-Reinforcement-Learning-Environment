from env_Soccer import EnvSoccer
import matplotlib.pyplot as plt
import random

env = EnvSoccer()

max_MC_iter = 2000
env.ball.vel[0] = env.ball.vel[0] + 40 * random.random()
env.ball.vel[1] = env.ball.vel[1] + 60 * random.random()
fig = plt.figure()
for MC_iter in range(max_MC_iter):
    print(MC_iter)

    plt.imshow(env.get_global_obs())
    plt.xticks([])
    plt.yticks([])
    rand_action_list = []
    rand_vec_list = []
    rand_const_list = []
    for i in range(6):
        temp = [20 * (random.random()-0.5), 20 * (random.random()-0.5)]
        rand_action_list.append(random.randint(0, 4))
        rand_vec_list.append(temp)
        rand_const_list.append(20 * random.random())
    # add random velocity
    env.step(rand_action_list, rand_vec_list, rand_const_list)
    #plt.show()
    plt.pause(.04)
    plt.draw()