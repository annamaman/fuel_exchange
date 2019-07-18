from module.fuel import Fuel
from module.crane import Crane, CraneController
from module.field import Field
from module.fuel_exchange_controller import FuelExchangeController
from module.q_learning import QLearning_Solver

# 使用する燃料、クレーンを定義
fuel1 = Fuel(state=3, location=[1,1], name="F3")
fuel2 = Fuel(state=3, location=[1,2], name="F3")
fuel3 = Fuel(state=3, location=[2,1], name="F3")
fuel4 = Fuel(state=3, location=[2,2], name="F3")
# fuel5 = Fuel(state=3, location=[2,3], name="F3")
# fuel6 = Fuel(state=3, location=[3,2], name="F3")
# fuel7 = Fuel(state=3, location=[3,3], name="F3")
# fuel5 = Fuel(state=3, location=[2,3], name="F3")

crane1 = Crane(moving_speed=1, fuel=None, location=[4,2], moving_area=[[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]], moving_vec=[[1,0],[-1,0],[0,1],[0,-1]], name="C1")
crane2 = Crane(moving_speed=2, fuel=None, location=[4,3], moving_area=[[1,1],[1,2],[1,3],[1,4],[2,1],[2,2],[2,3],[2,4],[3,1],[3,2],[3,3],[3,],[4,1],[4,2],[4,3],[4,4]], moving_vec=[[1,0],[-1,0],[0,1],[0,-1]], name="C2")

# リスト化（手作業）
fuel_list = [fuel1, fuel2, fuel3, fuel4]
crane_list = [crane1]

# field作成
# field = Field([["W","W","W","W","W"],["W","S","S","S","W"],["W","S","S","S","W"],["W","S","S","S","W"],["W","W","W","W","W"]], crane_list, fuel_list)
field = Field([["W","W","W","W","W","W"],["W","S","S","S","S","W"],["W","S","S","S","S","W"],["W","S","S","S","S","W"],["W","S","S","S","S","W"],["W","W","W","W","W","W"]], crane_list, fuel_list)

# クレーンコントローラーを定義
c_controller1 = CraneController(field, crane1, fuel_list)

# リスト化（手作業）
crane_controller_list = [c_controller1]

# ゲーム全体のコントローラーを定義
fuel_exchange_controller = FuelExchangeController(field, crane_controller_list, fuel_list)

qsolver = QLearning_Solver(fuel_exchange_controller)
qsolver.qlearn(500, 1)