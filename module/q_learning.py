import random,copy,sys,time
import numpy as np
from matplotlib import pyplot
import copy
class QLearning_Solver(object):
    def __init__(self, fuel_exchange_controller):
        self.Qvalue = {}
        self.f_controller = fuel_exchange_controller
        self.f_controller_ = copy.deepcopy(fuel_exchange_controller)
        self.alpha = 0.2
        self.gamma  = 0.9
        self.epsilon = 1
        self.steps = 0
        self.score = 0
        self.list = []
        self.min_states = []

    def qlearn(self, epoch, clear_time):
        start = time.time()
        min_episode = 0
        min_play_time = 1000
        for episode in range(epoch):
            [play_time, states] = self.game_play()
            if play_time < min_play_time:
                min_episode = episode + 1
                min_play_time = play_time
                self.min_states = states
            print("episode : " + str(episode+1) + "  playtime : " + str(play_time))
            self.list.append(play_time)
            self.epsilon = 1 - (episode+1)/epoch
            if play_time <= clear_time:
                sys.exit()
                x = np.linspace(0,epoch,len(self.list))  #0から2πまでの範囲を100分割したnumpy配列
                y = np.array(self.list)
                # pyplot.plot(x, y)
                # pyplot.show()
            self.f_controller = copy.deepcopy(self.f_controller_)
        goal = time.time()
        print("Execution Time : " + str(goal-start))
        print("min_episode : " + str(min_episode) + "  min_playtime : " + str(min_play_time))

        x = np.linspace(0,epoch,len(self.list))  #0から2πまでの範囲を100分割したnumpy配列
        y = np.array(self.list)
        # pyplot.plot(x, y)
        # pyplot.show()
        return self.min_states

    def game_play(self):
        i = 0
        states = []
        while True:
            for c_controller in self.f_controller.crane_controller_list:
                for j in range(c_controller.crane.moving_speed):
                    action = self.choose_action(c_controller)
                    states.append(self.f_controller.get_state(c_controller))
                    if self.update_Qvalue(c_controller, action):
                        return i, states
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

          
                # break

    def update_Qvalue(self, c_controller, action):
        state = self.f_controller.get_state(c_controller)
        next_state, score, finish_flg = self.f_controller.step(action, c_controller)
        # self.f_controller.field.display()
        # print(score)   
        # print(state)
        Q_s_a = self.get_Qvalue(state, action)
        Q_s_a_list = []
        # print("-------------------------------")
        # print( c_controller.get_action())
        for n_action in c_controller.get_action():
            # print("---------------------")
            # print(n_action)
            # print(self.get_Qvalue(state, n_action))
            # self.f_controller.field.display()
            # print("          ↓")
            c_controller.do_action(n_action)
            state_ = self.f_controller.get_state(c_controller)       
            Q_s_a_list.append(self.get_Qvalue(state_, n_action))
            # self.f_controller.field.display()
            reverse_n_action = [-1*n_action[0], -1*n_action[1], -1*n_action[2]]
            c_controller.do_action(reverse_n_action)

        mQ_s_a = max(Q_s_a_list)
        # print(mQ_s_a)
        if finish_flg:
            mQ_s_a = 0
        q_value = Q_s_a + self.alpha * ( score +  self.gamma * mQ_s_a - Q_s_a )
        # self.f_controller.field.display()
        self.set_Qvalue(state, action, q_value)
        # print(self.get_Qvalue(state, action))
        return finish_flg

    def get_Qvalue(self, state, action):
        state = tuple(state)
        action = (action[0], action[1], action[2])
        try:
            return self.Qvalue[state][action]
        except KeyError:
            return -1

    def set_Qvalue(self, state, action, q_value):
        state = tuple(state)
        action = (action[0], action[1], action[2])
        self.Qvalue.setdefault(state,{})
        # print(state)
        self.Qvalue[state][action] = q_value


    def choose_action(self, c_controller):
        actions = self.f_controller.get_action(c_controller)
        if self.epsilon > random.random():
            return random.choice(actions)
        else:
            state = self.f_controller.get_state(c_controller)
            return self.choose_action_greedy(state, actions)

    def choose_action_greedy(self, state, actions):
        best_actions = []
        max_q_value = -1000000
        for a in actions:
            q_value = self.get_Qvalue(state, a)
            if q_value > max_q_value:
                max_q_value = q_value
        for a in actions:
            q_value = self.get_Qvalue(state, a)
            if q_value == max_q_value:
                best_actions.append(a)

        return random.choice(best_actions)
