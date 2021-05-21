from env_FireFighter import EnvFireFighter
import random

def generate_tgt_list(agt_num):
    tgt_list = []
    for i in range(agt_num):
        tgt_list.append(random.randint(0, 1))
    return tgt_list


env = EnvFireFighter(4)

max_iter = 100
for i in range(max_iter):
    print("iter= ", i)
    print("actual fire level: ", env.firelevel)
    print("observed fire level: ", env.get_obs())
    tgt_list = generate_tgt_list(3)
    print("agent target: ", tgt_list)
    reward = env.step(tgt_list)
    print("reward: ", reward)
    print(" ")
