import pygame, sys, time
from pygame.locals import *


# 学習結果をpygameで可視化
pygame.init()

map_size = len(field.map)
c = 600 // map_size

# winImage = pygame.image.load('img/win.jpg')
screen = pygame.display.set_mode((600, 600))
font = pygame.font.Font(None, c*165//100)

craneImage = pygame.image.load('./img/crane.png')
craneImage = pygame.transform.scale(craneImage,(100,100))
fuelImage = pygame.image.load('./img/fuel.png')
fuelImage = pygame.transform.scale(fuelImage,(c,c))
blackImage = pygame.image.load('./img/black.png')
blackImage = pygame.transform.scale(blackImage,(c,c))
screen.fill((0,0,0))

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

        # if traje[0] == goal_point[0] and traje[1] == goal_point[1]:
        #     screen.blit(winImage, (0,150))
        #     pygame.draw.rect(screen,(0,0,0),Rect(0,0,600,150))
        #     pygame.draw.rect(screen,(0,0,0),Rect(0,450,600,150))
        #     pygame.display.update()
        #     time.sleep(0.2)
    pygame.quit()
    sys.exit()

        # pygame.draw.rect(screen,(0,0,0),Rect(traje[1]*c,traje[0]*c,c,c))
