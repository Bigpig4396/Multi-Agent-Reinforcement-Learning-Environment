from env_Warehouse import EnvWarehouse
import random

if __name__ == '__main__':
    num_agt = 4
    env = EnvWarehouse(num_agt)
    max_iter = 100000
    for i in range(max_iter):
        print('iter', i)
        for k in range(len(env.agt_list)):
            print('agent', env.agt_list[k].id, 'is at', env.agt_list[k].pos, 'catching box', env.agt_list[k].catch_box)
        for k in range(len(env.box_list)):
            print('box', env.box_list[k].id, 'is at', env.box_list[k].pos, ', caught by', env.get_caught_agt_index_list(env.box_list[k].id))
        env.plot_scene()
        # env.render()
        action_list = []
        for k in range(num_agt):
            action_list.append(random.randint(0, 3))
        reward = env.step(action_list)
