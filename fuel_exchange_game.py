from module.fuel import Fuel
from module.crane import Crane, CraneController
from module.field import Field
from module.fuel_exchange_controller import FuelExchangeGameController

fuel_list = [Fuel(state=3, location=[1,1], name="F3"), Fuel(state=3, location=[3,3], name="F3"), Fuel(state=2, location=[3,2], name="F2"), Fuel(state=3, location=[1,2], name="F3")]
crane = Crane(moving_speed=1, fuel=None, location=[2,1], moving_area=[[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]], moving_vec=[[1,0],[-1,0],[0,1],[0,-1]], name="C1")
crane2 = Crane(moving_speed=2, fuel=None, location=[2,2], moving_area=[[1,1],[1,2],[1,3],[2,1],[2,2],[2,3],[3,1],[3,2],[3,3]], moving_vec=[[1,0],[-1,0],[0,1],[0,-1]], name="C2")
crane_list = [crane, crane2]

field = Field([["W","W","W","W","W"],["W","S","S","S","W"],["W","S","S","S","W"],["W","S","S","S","W"],["W","W","W","W","W"]], crane_list, fuel_list)

crane_controller_list = [CraneController(field, crane, fuel_list),  CraneController(field, crane2, fuel_list)]

fuel_exchange_game_controller = FuelExchangeGameController(field, crane_controller_list, fuel_list)
fuel_exchange_game_controller.main()