import random,copy
from module.fuel import Fuel
from module.crane import Crane, CraneController
from module.field import Field
from module.fuel_exchange_controller import FuelExchangeController
import numpy as np
from matplotlib import pyplot


class QLearning_Solver(object):
    def __init__(self, field, crane_controller, fuel_exchange_controller, display=False):
        self.Qvalue = {}
        self.Field = field
        self.crane_controller = crane_controller
        self.fuel_exchange_controller = fuel_exchange_controller
        self.alpha = 0.2
        self.gamma  = 0.9
        self.epsilon = 0.2
        self.steps = 0
        self.score = 0

    def qlearn(self):
        i = 0
        j = 0
        score_list = []
        while True:
            action = self.choose_action(self.crane_controller)
            # self.Field.display()
            self.crane_controller.do_action(action)
            i += 1
            if self.update_Qvalue(self.crane_controller, action):
                print("エポック数 : " + str(j) + " 操作回数 : " + str(i))
                if i >= 10:
                    score_list.append(self.fuel_exchange_controller.score)
                    fuel_list = [Fuel(state=3, location=[1,1], name="F3"), Fuel(state=3, location=[1,2], name="F3"),Fuel(state=3, location=[2,1], name="F3")]
            
                    crane = Crane(moving_speed=1, fuel=None, location=[2,1], moving_area=[[1,1],[1,2],[1,3],[2,1],[2],[2,3],[3,1],[3,2],[3,3]], moving_vec=[[1,0],[-1,0],[0,1],[0,-1]], name="C1")
                    crane_list = [crane]
                    field = Field([["W","W","W","W","W"],["W","S","S","S","W"],["W","S","S","S","W"],["W","S","S","S","W"],["W","W","W","W","W"]], crane_list, fuel_list)
                    crane_controller_list = [CraneController(field, crane, fuel_list)]
                    fuel_exchange_controller = FuelExchangeController(field, crane_controller_list, fuel_list)
                    self.Field = field
                    self.crane_controller = crane_controller_list[0]
                    self.fuel_exchange_controller = fuel_exchange_controller
                    i = 0
                    j += 1
                    continue
                # x = np.linspace(0,10,len(score_list))  #0から2πまでの範囲を100分割したnumpy配列
                # y = np.array(score_list)
                # pyplot.plot(x, y)
                # pyplot.show()
          
                break

    def update_Qvalue(self, crane_controller, action):
        state = [crane_controller.crane.location[0], crane_controller.crane.location[1]]
        for fuel in self.Field.fuel_list:
            state.append(fuel.location[0])
            state.append(fuel.location[1])
        Q_s_a = self.get_Qvalue(state, action)
        Q_s_a_list = []
        for n_action in self.crane_controller.get_actions():
            crane_controller.do_action(n_action)
            state = [crane_controller.crane.location[0], crane_controller.crane.location[1]]
            for fuel in self.Field.fuel_list:
                state.append(fuel.location[0])
                state.append(fuel.location[1])
            Q_s_a_list.append(self.get_Qvalue(state, n_action))
            reverse_n_action = [-1*n_action[0], -1*n_action[1], -1*n_action[2]]
            crane_controller.do_action(reverse_n_action)
        mQ_s_a = max(Q_s_a_list)
        r_s_a, finish_flg = self.fuel_exchange_controller.scoring_field()
        q_value = Q_s_a + self.alpha * ( r_s_a +  self.gamma * mQ_s_a - Q_s_a)
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

    def choose_action(self, crane_controller):
        action = []
        state = []
        if self.epsilon < random.random():
            return random.choice(crane_controller.get_actions())
        else:
            state = [crane_controller.crane.location[0], crane_controller.crane.location[1]]
            for fuel in self.Field.fuel_list:
                state.append(fuel.location[0])
                state.append(fuel.location[1])
            return self.choose_action_greedy(state, crane_controller.get_actions())

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
