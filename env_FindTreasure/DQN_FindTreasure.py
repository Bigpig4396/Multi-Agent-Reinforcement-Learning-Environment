from env_FindTreasure import EnvFindTreasure
from keras.models import Sequential
from keras.layers.convolutional import Conv2D
from keras.layers.core import Dense, Flatten, Activation
from keras.layers.core import Dense
from keras.optimizers import Adam
import numpy as np
import matplotlib.pyplot as plt
import random


def print_action_freq(a_list):
    temp_data_len = len(a_list)
    freq = np.zeros((1, 5))
    for k in range(temp_data_len):
        freq[0, int(a_list[k])] = freq[0, int(a_list[k])] + 1
    print(freq)


env = EnvFindTreasure()
map_size = 10

model_1 = Sequential()
model_1.add(Conv2D(32, (3, 3), input_shape=(map_size, map_size, 1), strides=(3, 3), padding="same"))
model_1.add(Activation('relu'))
model_1.add(Flatten())
model_1.add(Dense(units=200, activation='relu'))
model_1.add(Dense(units=5, activation='linear'))
adam = Adam(lr=1e-4)
model_1.compile(loss='mse', optimizer=adam)

model_2 = Sequential()
model_2.add(Conv2D(32, (3, 3), input_shape=(map_size, map_size, 1), strides=(3, 3), padding="same"))
model_2.add(Activation('relu'))
model_2.add(Flatten())
model_2.add(Dense(units=200, activation='relu'))
model_2.add(Dense(units=5, activation='linear'))
adam = Adam(lr=1e-4)
model_2.compile(loss='mse', optimizer=adam)



max_opt_iter = 5
max_MC_iter = 10000
max_test_iter = 10000
global_loss = []
global_best = -100000
action_num = 5

for opt_iter in range(max_opt_iter):
    print("iteration ", opt_iter)

    # generate an episode
    env.reset()

    batch_1 = [[], [], [], []]  # obs, q, a, r
    batch_2 = [[], [], [], []]
    done = 0

    for MC_iter in range(max_MC_iter):
        obs_1 = env.get_agt1_obs()
        obs_2 = env.get_agt2_obs()
        batch_1[0].append(obs_1)
        batch_2[0].append(obs_2)

        # predict Q value for each action
        q_1 = model_1.predict(np.array(obs_1).reshape((1, map_size, map_size, 1)))
        q_2 = model_2.predict(np.array(obs_2).reshape((1, map_size, map_size, 1)))
        batch_1[1].append(q_1)
        batch_2[1].append(q_2)

        # choose action with maximal Q value
        if random.random() < 0.3:
            a_1 = random.randint(0, 4)
            a_2 = random.randint(0, 4)
        else:
            q_1 = model_1.predict(np.array(obs_1).reshape((1, map_size, map_size, 1)))
            q_2 = model_2.predict(np.array(obs_2).reshape((1, map_size, map_size, 1)))
            a_1 = np.argmax(q_1)
            a_2 = np.argmax(q_2)
        a_pig = 3

        batch_1[2].append(a_1)
        batch_2[2].append(a_2)

        # excute action
        reward, obs_1, obs_2 = env.step(a_1, a_2)
        batch_1[3].append(reward)
        batch_2[3].append(reward)

        if done == 1:  # sample 1 more time
            break

        if reward > 0:
            done = 1

    # form target
    datalen = len(batch_1[0])
    print("episode length= ", datalen)

    target_1 = np.array(batch_1[1]).reshape((datalen, action_num))  #
    for i in range(datalen - 1):
        target_1[i][int(batch_1[2][i])] = batch_1[3][i] + 0.99 * np.max(batch_1[1][i + 1])

    target_2 = np.array(batch_2[1]).reshape((datalen, action_num))
    for i in range(datalen - 1):
        target_2[i][int(batch_2[2][i])] = batch_2[3][i] + 0.99 * np.max(batch_1[1][i + 1])

    train_x_1 = np.array(batch_1[0]).reshape((datalen, map_size, map_size, 1))
    train_x_2 = np.array(batch_2[0]).reshape((datalen, map_size, map_size, 1))
    train_y_1 = target_1
    train_y_2 = target_2

    # train neural network
    model_1.fit(train_x_1, train_y_1, batch_size=32, epochs=10, verbose=0, shuffle=True)
    model_2.fit(train_x_2, train_y_2, batch_size=32, epochs=10, verbose=0, shuffle=True)


    # test phase
    env.reset()
    a_1_list = []
    a_2_list = []
    acc_reward = 0
    for test_iter in range(max_test_iter):

        obs_1 = env.get_agt1_obs()
        obs_2 = env.get_agt2_obs()

        # predict Q value for each action
        q_1 = model_1.predict(np.array(obs_1).reshape((1, map_size, map_size, 1)))
        q_2 = model_2.predict(np.array(obs_2).reshape((1, map_size, map_size, 1)))

        # choose action with maximal Q value
        a_1 = np.argmax(q_1)
        a_2 = np.argmax(q_2)
        a_1_list.append(a_1)
        a_2_list.append(a_2)
        a_pig = 3

        # excute action
        reward, obs_1, obs_2 = env.step(a_1, a_2)
        acc_reward = acc_reward + reward
    print("Accumulated Reward", acc_reward)

    if acc_reward > global_best:
        global_best = acc_reward
        print("save new model")

    global_loss.append(acc_reward)
    print_action_freq(a_1_list)
    print_action_freq(a_2_list)
    print(" ")

x = np.arange(0, max_opt_iter)
plt.figure()
plt.plot(x, global_loss)
plt.show()