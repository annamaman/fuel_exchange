class FuelExchangeGameController(object):
    def __init__(self, field, crane_controller_list, fuel_list):
        self.field = field
        self.crane_controller_list = crane_controller_list
        self.fuel_list = fuel_list
        self.score = 0
    
    def main(self, repeat_num=10):
        print("これから" + str(repeat_num) + "回試行します。")
        for i in range(repeat_num):
            print(str(i+1) + "巡目")
            self.go_next()
            self.scoring_field()
            print("")
            print(str(i+1) + "巡目のスコア: " + str(self.score))
            print("-------------------------------------------------------------------------")
        print("最終スコアは " + str(self.score) + " です。")

    def go_next(self):
        for crane_controller in self.crane_controller_list:
            print("")
            print(crane_controller.crane.name + "のターン")             
            for j in range(crane_controller.crane.moving_speed):
                print(str(j+1) + "回目の行動")
                actions = crane_controller.get_actions()
                action_code = self.decide_action(actions, self.field)
                print("")
                crane_controller.do_action(action_code)
        
    def decide_action(self, actions, field):
        field.display()
        while True:
            try:
                print("")
                print("可能なアクション: " + str(actions))
                action_code = input("アクションコード: ").split(",")
                if  [int(action_code[0]), int(action_code[1]), int(action_code[2])] in actions:
                    return [int(action_code[0]), int(action_code[1]), int(action_code[2])]
                else:
                    print("アクションコードは可能なアクションの中から選択してください。")
            except ValueError:
                print("x,y,z の形式で入力してください。")

    def scoring_field(self):
        self.score = 0
        fuel_combs = []
        F3_F3_vh_score = 100
        F3_F3_dia_score = 50
        F3_F2_vh_score = 10

        for i,fuel in enumerate(self.fuel_list):
            if fuel.state == 3:
                vh_neighbor = self.field.get_neighbor(fuel.location,"vh")
                dia_neighbor = self.field.get_neighbor(fuel.location,"dia")
                for j,fuel2 in enumerate(self.fuel_list):
                    if i == j:
                        continue
                    if fuel2.location in vh_neighbor and [fuel,fuel2] not in fuel_combs:
                        if fuel2.state == 3:
                            self.score = self.score + F3_F3_vh_score
                        if fuel2.state == 2:
                            self.score = self.score + F3_F2_vh_score
                        fuel_combs.append([fuel2,fuel])
                    if fuel2.location in dia_neighbor and [fuel,fuel2] not in fuel_combs:
                        if fuel2.state == 3:
                            self.score = self.score + F3_F3_dia_score
                        fuel_combs.append([fuel2,fuel])

class FuelExchangeController(object):
    def __init__(self, field, crane_controller_list, fuel_list):
        self.field = field
        self.crane_controller_list = crane_controller_list
        self.fuel_list = fuel_list
        self.score = 0
    
    def main(self, repeat_num=10):
        for i in range(repeat_num):
            self.go_next()
            self.scoring_field()

    def go_next(self):
        for crane_controller in self.crane_controller_list:
            for j in range(crane_controller.crane.moving_speed):
                actions = crane_controller.get_actions()
                action_code = self.decide_action(actions, self.field)
                crane_controller.do_action(action_code)
        
    def decide_action(self, actions, field):
        field.display()
        while True:
            try:
                action_code = input("アクションコード: ").split(",")
                if  [int(action_code[0]), int(action_code[1]), int(action_code[2])] in actions:
                    return [int(action_code[0]), int(action_code[1]), int(action_code[2])]
                else:
            except ValueError:

    def scoring_field(self):
        self.score = 0
        fuel_combs = []
        F3_F3_vh_score = 100
        F3_F3_dia_score = 50
        F3_F2_vh_score = 10

        for i,fuel in enumerate(self.fuel_list):
            if fuel.state == 3:
                vh_neighbor = self.field.get_neighbor(fuel.location,"vh")
                dia_neighbor = self.field.get_neighbor(fuel.location,"dia")
                for j,fuel2 in enumerate(self.fuel_list):
                    if i == j:
                        continue
                    if fuel2.location in vh_neighbor and [fuel,fuel2] not in fuel_combs:
                        if fuel2.state == 3:
                            self.score = self.score + F3_F3_vh_score
                        if fuel2.state == 2:
                            self.score = self.score + F3_F2_vh_score
                        fuel_combs.append([fuel2,fuel])
                    if fuel2.location in dia_neighbor and [fuel,fuel2] not in fuel_combs:
                        if fuel2.state == 3:
                            self.score = self.score + F3_F3_dia_score
                        fuel_combs.append([fuel2,fuel])