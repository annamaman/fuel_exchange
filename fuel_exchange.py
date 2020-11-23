from module.fuel import Fuel
from module.crane import Crane, CraneController
from module.field import Field
from module.fuel_exchange_controller import FuelExchangeController
from module.q_learning import QLearning_Solver
import pygame, sys, time
from pygame.locals import *

# 使用する燃料、クレーンを定義
fuel1 = Fuel(state=3, location=[1,1], name="F3")
fuel2 = Fuel(state=3, location=[1,2], name="F3")
fuel3 = Fuel(state=3, location=[1,3], name="F3")
fuel4 = Fuel(state=3, location=[2,2], name="F3")
fuel5 = Fuel(state=3, location=[2,3], name="F3")
# fuel6 = Fuel(state=3, location=[3,2], name="F3")
# fuel7 = Fuel(state=3, location=[3,3], name="F3")
# fuel5 = Fuel(state=3, location=[2,3], name="F3")

crane1 = Crane(moving_speed=1, fuel=None, location=[3,3], moving_area=[[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[3,1],[3,2],[3,3],[3,4],[3,5],[3,6],[4,1],[4,2],[4,3],[4,4],[4,5],[4,6],[5,1],[5,2],[5,3],[5,4],[5,5],[5,6],[6,1],[6,2],[6,3],[6,4],[6,5],[6,6]], moving_vec=[[1,0],[-1,0],[0,1],[0,-1]], name="C1")
crane2 = Crane(moving_speed=2, fuel=None, location=[4,3], moving_area=[[1,1],[1,2],[1,3],[1,4],[1,5],[1,6],[2,1],[2,2],[2,3],[2,4],[2,5],[2,6],[3,1],[3,2],[3,3],[3,4],[3,5],[3,6],[4,1],[4,2],[4,3],[4,4],[4,5],[4,6],[5,1],[5,2],[5,3],[5,4],[5,5],[5,6],[6,1],[6,2],[6,3],[6,4],[6,5],[6,6]], moving_vec=[[1,0],[-1,0],[0,1],[0,-1]], name="C2")

# リスト化（手作業）
fuel_list = [fuel1, fuel2, fuel3, fuel4]
crane_list = [crane1]

# field作成
field = Field([["S","S","S","S","S","S"],["S","S","S","S","S","S"],["S","S","S","S","S","S"],["S","S","S","S","S","S"],["S","S","S","S","S","S"],["S","S","S","S","S","S "]], crane_list, fuel_list)

# クレーンコントローラーを定義
c_controller1 = CraneController(field, crane1, fuel_list)
c_controller2 = CraneController(field, crane2, fuel_list)

# リスト化（手作業）
crane_controller_list = [c_controller1]

# ゲーム全体のコントローラーを定義
fuel_exchange_controller = FuelExchangeController(field, crane_controller_list, fuel_list)

qsolver = QLearning_Solver(fuel_exchange_controller)

# 学習開始
min_states = qsolver.qlearn(1000, 1)


# 学習結果をpygameで可視化
pygame.init()

map_size = len(field.map)
c = 600 // map_size

# 初期設定など
screen = pygame.display.set_mode((600, 600))
font = pygame.font.Font(None, c*165//100)

craneImage = pygame.image.load('./img/crane.png')
craneImage = pygame.transform.scale(craneImage,(100,100))
fuelImage = pygame.image.load('./img/fuel.png')
fuelImage = pygame.transform.scale(fuelImage,(c,c))
blackImage = pygame.image.load('./img/black.png')
blackImage = pygame.transform.scale(blackImage,(c,c))
screen.fill((0,0,0))

#　画面の書き出し
while True:
    for i in range(map_size):
        for j in range(map_size):
                if field.map[i][j] == "W":
                    pygame.draw.rect(screen,(0,150,0),Rect(j*c,i*c,c,c))        
    
    s = 0
    past_states_fuel = [0] * len(fuel_list)
    past_states_crane = [0] * len(crane_controller_list)
    for traje in min_states:
        for l in range(len(fuel_list)):
            if s > 0:
                screen.blit(blackImage, ( past_states_fuel[l][0]*c,  past_states_fuel[l][1]*c))
        for k in range(len(crane_controller_list)):
            if s > 0:
                screen.blit(blackImage, ( past_states_crane[k][0]*c,  past_states_crane[k][1]*c))
        for l in range(len(fuel_list)):
            screen.blit(fuelImage, (((traje[2*len(crane_controller_list)+l] + map_size) // map_size *c, (traje[2*len(crane_controller_list)+l] + map_size) % map_size *c)))
            past_states_fuel[l] = [(traje[2*len(crane_controller_list)+l] + map_size) // map_size, (traje[2*len(crane_controller_list)+l] + map_size) % map_size]
        for k in range(len(crane_controller_list)):
            screen.blit(craneImage, (((traje[2*k] + map_size) // map_size *c, (traje[2*k] + map_size) % map_size *c)))
            past_states_crane[k] = [(traje[2*k] + map_size) // map_size, (traje[2*k] + map_size) % map_size]
        time.sleep(1)
        print(traje)
        pygame.display.update()
        s += 1

    pygame.quit()
    sys.exit()