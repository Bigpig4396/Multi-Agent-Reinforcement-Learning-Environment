# just click 'run'

from env_SingleMaze import EnvSingleMaze
from keras.models import Sequential
from matplotlib.gridspec import GridSpec
from keras.layers.core import Dense, Flatten, Activation
from keras.layers.convolutional import Conv2D
from keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt
import random


max_opt_iter = 200
max_MC_iter = 2000

global_loss = []
global_best = -100000
obs_dim = 8
action_num = 4

env = EnvSingleMaze(True)

model_1 = Sequential()
model_1.add(Conv2D(32, kernel_size=3, data_format="channels_last", input_shape=(5, 5, 3), strides=(1, 1), padding="same"))
model_1.add(Activation('relu'))
model_1.add(Flatten())
model_1.add(Dense(units=50, activation='relu'))
model_1.add(Dense(units=action_num))
adam = Adam(lr=1e-4)
model_1.compile(loss='mse', optimizer=adam)

#model_1.load_weights('DQN_SingleMaze_model1.h5')
annealing = 0.8
for opt_iter in range(max_opt_iter):
    print("iteration ", opt_iter)

    # generate an episode

    batch_1 = [[], [], [], []]  # obs, q, a, r_1, r_2
    done = 0
    print("annealing", annealing)
    for MC_iter in range(max_MC_iter):

        obs_1 = env.get_agt1_obs()
        batch_1[0].append(obs_1)

        # predict Q value for each action
        obs_1 = obs_1.reshape((1, 5, 5, 3))
        q_1 = model_1.predict(obs_1)
        batch_1[1].append(q_1)

        # choose action with maximal Q value

        if random.random() < annealing:
            a_1 = random.randint(0, action_num - 1)
        else:
            a_1 = np.argmax(q_1)

        batch_1[2].append(a_1)

        # excute action
        reward_1, obs_1 = env.step(a_1)
        batch_1[3].append(reward_1)

        if done == 1:   # sample 1 more time
            env.reset()
            break

        if reward_1 > 0:
            done = 1

    # form target
    datalen = len(batch_1[0])
    print("episode length= ", datalen)

    target_1 = np.array(batch_1[1]).reshape((datalen, action_num))

    for i in range(datalen - 2, -1, -1):
        target_1[i][int(batch_1[2][i])] = batch_1[3][i] + 0.95*np.max(batch_1[1][i + 1])

    train_x_1 = np.array(batch_1[0]).reshape((datalen, 5, 5, 3))
    train_y_1 = target_1

    # train neural network
    annealing = annealing * 0.99

    model_1.fit(train_x_1, train_y_1, batch_size=32, epochs=100, verbose=0, shuffle=True)
    model_1.save_weights('DQN_SingleMaze_model1.h5')



fig = plt.figure()
gs = GridSpec(3, 3, figure=fig)
ax1 = fig.add_subplot(gs[0:2, 0:3])
ax2 = fig.add_subplot(gs[2:3, 0:1])
env.reset()
for MC_iter in range(max_MC_iter):
    print(MC_iter)
    ax1.imshow(env.get_global_obs())
    ax2.imshow(env.get_agt1_obs())
    obs_1 = env.get_agt1_obs()
    obs_1 = obs_1.reshape((1, 5, 5, 3))
    q_1 = model_1.predict(obs_1)
    a_1 = np.argmax(q_1)
    reward_1, obs_1 = env.step(a_1)
    plt.pause(.5)
    plt.draw()