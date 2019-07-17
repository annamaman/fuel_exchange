import copy

class FuelExchangeController(object):
    def __init__(self, field, crane_controller_list, fuel_list):
        self.field = field
        self.crane_controller_list = crane_controller_list
        self.fuel_list = fuel_list
        self.step_num = 0

    def step(self, action, crane_controller):
        self.step_num += 1
        score, finish_flg = self.get_reward(action, crane_controller)
        state = self.get_state(crane_controller)
        return state, score, finish_flg
    
    def get_state(self, controller):
        return self.field.get_state(self.step_num, controller)

    def get_action(self, crane_controller):
        return crane_controller.get_action()

    def get_reward(self, action, crane_controller):
        score_before, a = self.get_score()
        crane_controller.do_action(action)
        score_after, finish_flg = self.get_score()
        reward = (score_after - score_before)/100
        reward = reward - 0.3
        return reward, finish_flg


    def get_score(self):
        F3_F3_vh_score = -20
        F3_F3_dia_score = 0
        F3_F2_vh_score = 0

        score = 50
        fuel_combs = []
        clear_judge = True

        for i,fuel in enumerate(self.fuel_list):
            if fuel.state == 3:
                vh_neighbor = self.field.get_neighbor(fuel.location,"vh")
                dia_neighbor = self.field.get_neighbor(fuel.location,"dia")
                for j,fuel2 in enumerate(self.fuel_list):
                    if i == j:
                        continue
                    if fuel2.location in vh_neighbor and [fuel,fuel2] not in fuel_combs:
                        if fuel2.state == 3:
                            score = score + F3_F3_vh_score
                            clear_judge = False
                        if fuel2.state == 2:
                            score = score + F3_F2_vh_score
                            clear_judge = False
                            fuel_combs.append([fuel2,fuel])
                    if fuel2.location in dia_neighbor and [fuel,fuel2] not in fuel_combs:
                        if fuel2.state == 3:    
                            score = score + F3_F3_dia_score
                            clear_judge = False
                            fuel_combs.append([fuel2,fuel])
        if clear_judge:
            for crane_controller in self.crane_controller_list:
                if crane_controller.crane.fuel is not None:
                    clear_judge = False
                else:
                    score = score + 100000

        return score, clear_judge