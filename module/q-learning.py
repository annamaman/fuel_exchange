import random

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
        while True:
            action = self.choose_action(self.crane_controller)    
            if self.update_Qvalue(self.crane_controller, action):
                break

    def update_Qvalue(self, crane_controller, action):
        state = [crane_controller.crane.location[0], crane_controller.crane.location[1]]
        Q_s_a = self.get_Qvalue(state, action)
        mQ_s_a = max([self.get_Qvalue(action, n_action) for n_action in self.crane_controller.get_actions()])
        crane_controller.do_action(action)
        r_s_a, finish_flg = self.fuel_exchange_controller.scoring_field()
        q_value = Q_s_a + self.alpha * ( r_s_a +  self.gamma * mQ_s_a - Q_s_a)
        self.set_Qvalue(state, action, q_value)
        return finish_flg


    def get_Qvalue(self, state, action):
        state = (state[0], state[1])
        action = (action[0], action[1], action[2])
        try:
            return self.Qvalue[state][action]
        except KeyError:
            return 0.0

    def set_Qvalue(self, state, action, q_value):
        state = (state[0], state[1])
        action = (action[0], action[1], action[2])
        self.Qvalue.setdefault(state,{})
        self.Qvalue[state][action] = q_value

    def choose_action(self, crane_controller):
        action = []
        state = []
        if self.epsilon < random.random():
            action.append(random.choice(crane_controller.get_actions()))
        else:
            state = [crane_controller.crane.location[0], crane_controller.crane.location[1]]
            action.append(self.choose_action_greedy(state, crane_controller.get_actions()))
        return action

    def choose_action_greedy(self, state, actions):
        best_actions = []
        max_q_value = -100
        for a in actions:
            q_value = self.get_Qvalue(state, a)
            if q_value > max_q_value:
                best_actions = [a,]
                max_q_value = q_value
            elif q_value == max_q_value:
                best_actions.append(a)
        return random.choice(best_actions)
