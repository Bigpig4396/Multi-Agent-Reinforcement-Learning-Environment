from env_CatchPigs import EnvCatchPigs
import random

if __name__ == '__main__':
    env = EnvCatchPigs(9, True)
    max_iter = 10000
    for i in range(max_iter):
        action_list = [random.randint(0, 4), random.randint(0, 4)]
        #print("iter= ", i, env.agt1_pos, env.agt2_pos, env.pig_pos, env.agt1_ori, env.agt2_ori, a_1, a_2)
        reward_list, done = env.step(action_list)
        env.plot_scene()
        if reward_list[0] > 0:
            print("iter= ", i)
            print("agent 1 finds goal")



