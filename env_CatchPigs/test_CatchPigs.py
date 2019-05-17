from env_CatchPigs import EnvCatchPigs
import random

if __name__ == '__main__':
    env = EnvCatchPigs(7, True)
    max_iter = 10000
    for i in range(max_iter):
        action1 = random.randint(0, 4)
        action2 = random.randint(0, 4)
        action_list = [action1, action2]
        obs_list = env.get_obs()
        obs1 = obs_list[0]
        obs2 = obs_list[1]
        print("iter= ", i, env.agt1_pos, env.agt2_pos, env.pig_pos, env.agt1_ori, env.agt2_ori, 'action', action1, action2)
        env.render()
        reward_list, done = env.step(action_list)
        #env.plot_scene()
        if reward_list[0] > 0:
            print("iter= ", i)
            print("agent 1 finds goal")



