from module.fuel import Fuel
from module.crane import Crane, CraneController
from module.field import Field
from module.fuel_exchange_controller import FuelExchangeController
from module.q_learning import QLearning_Solver

fuel_list = [Fuel(state=3, location=[1,1], name="F3"), Fuel(state=3, location=[1,2], name="F3"),Fuel(state=3, location=[2,1], name="F3")]
crane = Crane(moving_speed=1, fuel=None, location=[2,1], moving_area=[[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]], moving_vec=[[1,0],[-1,0],[0,1],[0,-1]], name="C1")
crane_list = [crane]

field = Field([["W","W","W","W","W"],["W","S","S","S","W"],["W","S","S","S","W"],["W","S","S","S","W"],["W","W","W","W","W"]], crane_list, fuel_list)

crane_controller_list = [CraneController(field, crane, fuel_list)]

fuel_exchange_controller = FuelExchangeController(field, crane_controller_list, fuel_list)
qsolver = QLearning_Solver(field, crane_controller_list[0], fuel_exchange_controller)
qsolver.qlearn()