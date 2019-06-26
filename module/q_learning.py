import random,copy,sys
from module.fuel import Fuel
from module.crane import Crane, CraneController
from module.field import Field
from module.fuel_exchange_controller import FuelExchangeController
import numpy as np
from matplotlib import pyplot


class QLearning_Solver(object):
    def __init__(self, fuel_exchange_controller):
        self.Qvalue = {}
        self.field = fuel_exchange_controller.field
        self.c_controller_list = fuel_exchange_controller.crane_controller_list
        self.f_controller = fuel_exchange_controller
        self.alpha = 0.2
        self.gamma  = 0.9
        self.epsilon = 0.4
        self.steps = 0
        self.score = 0

    def qlearn(self):
        i = 0
        while True:
            for c_controller in self.c_controller_list:
                for j in range(c_controller.crane.moving_speed):
                    action = self.choose_action(c_controller)
                    print(self.f_controller.field.display())
                    if self.update_Qvalue(c_controller, action):
                        print(i)
                        sys.exit()
            i += 1
                    # if i >= 10:
                    #     score_list.append(self.fuel_exchange_controller.score)
                    #     fuel_list = [Fuel(state=3, location=[1,1], name="F3"), Fuel(state=3, location=[1,2], name="F3"),Fuel(state=3, location=[2,1], name="F3")]
                
                    #     crane = Crane(moving_speed=1, fuel=None, location=[2,1], moving_area=[[1,1],[1,2],[1,3],[2,1],[2],[2,3],[3,1],[3,2],[3,3]], moving_vec=[[1,0],[-1,0],[0,1],[0,-1]], name="C1")
                    #     crane_list = [crane]
                    #     field = Field([["W","W","W","W","W"],["W","S","S","S","W"],["W","S","S","S","W"],["W","S","S","S","W"],["W","W","W","W","W"]], crane_list, fuel_list)
                    #     crane_controller_list = [CraneController(field, crane, fuel_list)]
                    #     fuel_exchange_controller = FuelExchangeController(field, crane_controller_list, fuel_list)
                    #     self.Field = field
                    #     self.crane_controller = crane_controller_list[0]
                    #     self.fuel_exchange_controller = fuel_exchange_controller
                    #     i = 0
                    #     j += 1
                        # continue
                # x = np.linspace(0,10,len(score_list))  #0から2πまでの範囲を100分割したnumpy配列
                # y = np.array(score_list)
                # pyplot.plot(x, y)
                # pyplot.show()
          
                # break

    def update_Qvalue(self, c_controller, action):
        state, score, finish_flg = self.f_controller.step(action, c_controller)       
        Q_s_a = self.get_Qvalue(state, action)
        print(score)
        Q_s_a_list = []
        for n_action in c_controller.get_action():
            c_controller.do_action(n_action)
            state = self.f_controller.get_state()       
            Q_s_a_list.append(self.get_Qvalue(state, n_action))
            reverse_n_action = [-1*n_action[0], -1*n_action[1], -1*n_action[2]]
            c_controller.do_action(reverse_n_action)
        mQ_s_a = max(Q_s_a_list)

        q_value = Q_s_a + self.alpha * ( score +  self.gamma * mQ_s_a - Q_s_a )
        self.set_Qvalue(state, action, q_value)
        return finish_flg

    def get_Qvalue(self, state, action):
        state = tuple(state)
        action = (action[0], action[1], action[2])
        try:
            return self.Qvalue[state][action]
        except KeyError:
            return 0.0

    def set_Qvalue(self, state, action, q_value):
        state = tuple(state)
        action = (action[0], action[1], action[2])
        self.Qvalue.setdefault(state,{})
        self.Qvalue[state][action] = q_value

    def choose_action(self, c_controller):
        actions = self.f_controller.get_action(c_controller)
        if self.epsilon < random.random():
            return random.choice(actions)
        else:
            state = self.f_controller.get_state()
            return self.choose_action_greedy(state, actions)

    def choose_action_greedy(self, state, actions):
        best_actions = []
        max_q_value = -100
        for a in actions:
            q_value = self.get_Qvalue(state, a)
            if q_value > max_q_value:
                max_q_value = q_value
        for a in actions:
            q_value = self.get_Qvalue(state, a)
            if q_value == max_q_value:
                best_actions.append(a)
        return random.choice(best_actions)
