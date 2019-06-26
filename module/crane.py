import copy

class Crane(object):
    def __init__(self, moving_speed,  location, moving_area, moving_vec, fuel=None, name="C"):
        self.moving_speed = moving_speed
        self.fuel = fuel
        self.location = location
        self.moving_area = moving_area
        self.moving_vec = moving_vec
        self.name = name
    
    def lift(self, fuel, fuel_list):
        self.fuel = fuel
        fuel_list.remove(fuel)
    
    def put(self, fuel_list):
        fuel = copy.deepcopy(self.fuel)
        self.fuel = None
        fuel.location = copy.deepcopy(self.location)
        fuel_list.append(fuel)
    
    def move(self, action):
        next_location = [self.location[0] + action[0], self.location[1] + action[1]]
        if next_location in self.moving_area:
            self.location[0] = next_location[0]
            self.location[1] = next_location[1]
            if self.fuel is not None:
                self.fuel.location[0] = copy.copy(self.location[0])
                self.fuel.location[1] = copy.copy(self.location[1])

class CraneController(object):
    def __init__(self, field, crane, fuel_list):
        self.field = field
        self.crane = crane
        self.fuel_list = fuel_list
    
    def get_action(self):
        action_codes = [[0,0,0], [0,0,-1]]
        whole_map = self.field.get_whole_map()
        for vec in self.crane.moving_vec:           
            next_location = [self.crane.location[0] + vec[0], self.crane.location[1] + vec[1]]
            if next_location[0] < 0 or next_location[0] >= len(self.field.map) or next_location[1] < 0 or next_location[1] >= len(self.field.map):
                continue
            if next_location not in self.crane.moving_area:
                continue
            if whole_map[next_location[0]][next_location[1]] == "S" or whole_map[next_location[0]][next_location[1]] == "F":              
                action_codes.append([vec[0], vec[1], 0])
        if self.crane.fuel == None:
            action_codes.remove([0,0,-1])
        for fuel in self.fuel_list:
            if fuel.location == self.crane.location and self.crane.fuel == None:
                action_codes.append([0,0,1])
            if fuel.location == self.crane.location and [0,0,-1] in action_codes:
                action_codes.remove([0,0,-1])
        return action_codes

    def do_action(self, action_code):
        if action_code == [0,0,0]:
            return
        elif action_code == [0,0,1]:
            for fuel in self.fuel_list:
                if fuel.location == self.crane.location:
                    self.crane.lift(fuel, self.fuel_list)
                    break
            return
        elif action_code == [0,0,-1] and self.crane.fuel is not None:
            self.crane.put(self.fuel_list)
        else:
            self.crane.move([action_code[0], action_code[1]])