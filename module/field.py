import copy

class Field(object):
    def __init__(self, field_map, crane_list, fuel_list):
        self.map = field_map
        self.crane_list = crane_list
        self.fuel_list = fuel_list

    # 目視用 人の目に見やすいように、燃料とクレーンは名前で表示
    def display(self):        
        field_map = copy.deepcopy(self.map)
        for fuel in self.fuel_list:
            field_map[fuel.location[0]][fuel.location[1]] = fuel.name
        for crane in self.crane_list:
            field_map[crane.location[0]][crane.location[1]] = crane.name
        for line in field_map:
            print(line)
    
    # クレーンコントローラー用
    def get_whole_map(self):        
        field_map = copy.deepcopy(self.map)
        for fuel in self.fuel_list:
            field_map[fuel.location[0]][fuel.location[1]] = "F"
        for crane in self.crane_list:
            field_map[crane.location[0]][crane.location[1]] = "C"
        return field_map

    # directionは vh か dia か all の３種類
    # vhは縦と横の直近の要素のインデックス、diaは斜め方向の直近のインデックスを返す
    def get_neighbor(self, location, direction="vh"):
        neighbor = []
        vecs = []
        if direction == "vh":
            vecs = [[1,0],[0,1],[-1,0],[0,-1]]
        if direction == "dia":
            vecs = [[1,1],[-1,1],[1,-1],[-1,-1]]
        if direction == "all":
            vecs = [[1,0],[0,1],[-1,0],[0,-1],[1,1],[-1,1],[1,-1],[-1,-1]]
        for vec in vecs:
            next_location = [0,0]
            next_location[0] = location[0] + vec[0]
            next_location[1] = location[1] + vec[1]
            if next_location[0] < 0 or next_location[0] >= len(self.map) or next_location[1] < 0 or next_location[1] >= len(self.map):
                continue
            else:
                neighbor.append(next_location)
        return neighbor

    def get_state(self):
        state = []
        for crane in self.crane_list:
            state.append(crane.location[0])
            state.append(crane.location[1])
            if crane.fuel is None:
                state.append(0)
            else:
                state.append(1)
        for fuel in self.fuel_list:
            state.append(fuel.location[0])
            state.append(fuel.location[1])
            state.append(fuel.state)
        for crane in self.crane_list:
            if crane.fuel is not None:
                state.append(crane.fuel.location[0])
                state.append(crane.fuel.location[1])
                state.append(crane.fuel.state)
        return state          

                

