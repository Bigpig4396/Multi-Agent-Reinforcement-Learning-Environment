from env_Drones import EnvDrones
import random
import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec


env = EnvDrones(50, 4, 10, 30, 5)   # map_size, drone_num, view_range, tree_num, human_num
env.rand_reset_drone_pos()

max_MC_iter = 100
fig = plt.figure()
gs = GridSpec(1, 2, figure=fig)
ax1 = fig.add_subplot(gs[0:1, 0:1])
ax2 = fig.add_subplot(gs[0:1, 1:2])
for MC_iter in range(max_MC_iter):
    print(MC_iter)
    ax1.imshow(env.get_full_obs())
    ax2.imshow(env.get_joint_obs())

    human_act_list = []
    for i in range(env.human_num):
        human_act_list.append(random.randint(0, 4))

    drone_act_list = []
    for i in range(env.drone_num):
        drone_act_list.append(random.randint(0, 4))
    env.step(human_act_list, drone_act_list)
    plt.pause(.5)
    plt.draw()
