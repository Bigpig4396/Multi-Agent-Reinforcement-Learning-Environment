from env_FindGoals import EnvFindGoals
from keras.models import Sequential
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


env = EnvFindGoals()

model_1 = Sequential()
model_1.add(Dense(units=100, activation='relu', input_dim=8))
model_1.add(Dense(units=5, activation='linear'))
adam = Adam(lr=1e-4)
model_1.compile(loss='mse', optimizer=adam)

model_2 = Sequential()
model_2.add(Dense(units=100, activation='relu', input_dim=8))
model_2.add(Dense(units=5, activation='linear'))
adam = Adam(lr=1e-4)
model_2.compile(loss='mse', optimizer=adam)

max_opt_iter = 500
max_MC_iter = 10000
max_test_iter = 200
loss = []
global_best = -100000
obs_dim = 8
action_num = 5


FINAL_EPSILON = 0.0001  # final value of epsilon

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
        q_1 = model_1.predict(obs_1)
        q_2 = model_2.predict(obs_2)
        batch_1[1].append(q_1)
        batch_2[1].append(q_2)

        # choose action with maximal Q value

        a_1 = random.randint(0, action_num-1)
        a_2 = random.randint(0, action_num-1)

        batch_1[2].append(a_1)
        batch_2[2].append(a_2)

        # excute action
        reward, obs_1, obs_2 = env.step(a_1, a_2)
        batch_1[3].append(reward)
        batch_2[3].append(reward)

        if done == 1:   # sample 1 more time
            break

        if reward > 0:
            done = 1

    # form target
    datalen = len(batch_1[0])
    print("episode length= ", datalen)

    target_1 = np.array(batch_1[1]).reshape((datalen, action_num))  #
    for i in range(datalen - 1):
        target_1[i][int(batch_1[2][i])] = batch_1[3][i] + np.max(batch_1[1][i + 1])

    target_2 = np.array(batch_2[1]).reshape((datalen, action_num))
    for i in range(datalen - 1):
        target_2[i][int(batch_2[2][i])] = batch_2[3][i] + np.max(batch_1[1][i + 1])

    train_x_1 = np.array(batch_1[0]).reshape((datalen, obs_dim))
    train_x_2 = np.array(batch_2[0]).reshape((datalen, obs_dim))
    train_y_1 = target_1
    train_y_2 = target_2

    # train neural network
    model_1.fit(train_x_1, train_y_1, batch_size=32, epochs=10, verbose=0, shuffle=True)
    model_2.fit(train_x_2, train_y_2, batch_size=32, epochs=10, verbose=0, shuffle=True)

    # print_action_freq(batch_1[2])
    # print_action_freq(batch_2[2])




    # test phase
    env.reset()
    a_1_list = []
    a_2_list = []
    acc_reward = 0
    for test_iter in range(max_test_iter):

        obs_1 = env.get_agt1_obs()
        obs_2 = env.get_agt2_obs()

        # predict Q value for each action
        q_1 = model_1.predict(obs_1)
        q_2 = model_2.predict(obs_2)

        # choose action with maximal Q value
        a_1 = np.argmax(q_1)
        a_2 = np.argmax(q_2)
        a_1_list.append(a_1)
        a_2_list.append(a_2)

        # excute action
        reward, obs_1, obs_2 = env.step(a_1, a_2)
        acc_reward = acc_reward + reward

    print("Accumulated Reward", acc_reward)

    if acc_reward > global_best:
        global_best = acc_reward
        model_1.save_weights('DQN_FindGoals_model1.h5')
        model_2.save_weights('DQN_FindGoals_model2.h5')
        print("save new model")

    loss.append(acc_reward)
    # print_action_freq(a_1_list)
    # print_action_freq(a_2_list)
    print(" ")

x = np.arange(0, max_opt_iter)
plt.figure()
plt.plot(x, loss)
plt.show()
