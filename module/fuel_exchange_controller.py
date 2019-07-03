import copy

class FuelExchangeController(object):
    def __init__(self, field, crane_controller_list, fuel_list):
        self.field = field
        self.crane_controller_list = crane_controller_list
        self.fuel_list = fuel_list
        self.step_num = 0

    def step(self, action, crane_controller):
        self.step_num += 1
        crane_controller.do_action(action)
        score, finish_flg = self.get_reward()
        state = self.get_state(crane_controller)
        return state, score, finish_flg
    
    def get_state(self, controller):
        return self.field.get_state(self.step_num, controller)

    def get_action(self, crane_controller):
        return crane_controller.get_action()

    def get_reward(self):
        clear_score = 0
        F3_F3_vh_score = -1 * self.step_num
        F3_F3_dia_score = -1 * self.step_num
        F3_F2_vh_score = 0

        score = clear_score        
        finish_flg = False
        fuel_combs = []

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
                        if fuel2.state == 2:
                            score = score + F3_F2_vh_score
                            fuel_combs.append([fuel2,fuel])
                    if fuel2.location in dia_neighbor and [fuel,fuel2] not in fuel_combs:
                        if fuel2.state == 3:    
                            score = score + F3_F3_dia_score
                            fuel_combs.append([fuel2,fuel])
        if score == clear_score:
            finish_flg = True
            score = 10000000
            for crane_controller in self.crane_controller_list:
                if crane_controller.crane.fuel is not None:
                    finish_flg = False
                    score = -1 * self.step_num
        
        # score = -1 * self.step_num
        return score, finish_flg