import pygame, sys
from pygame.locals import *
import time
 

pygame.init()

screen = pygame.display.set_mode((600, 600))



def iter_chars(filename):
    """ Reads a text file char by char. """
    with open(filename, encoding='utf-8') as f:
        content = f.read()
    for ch in content:
        if ch == "\n":
            continue
        yield ch

def get_meiro_size(filename):
    meiro_size = 0
    with open(filename, encoding='utf-8') as f:
        content = f.read()
    for ch in content:
        if ch == "\n":
            break
        meiro_size = meiro_size + 1
    return meiro_size

meiro_size = get_meiro_size('memo2.txt')
meiro = [[0 for i in range(meiro_size)] for j in range(meiro_size)]

i = 0
j = 0
for ch in iter_chars('memo2.txt'):
    if j == meiro_size:
        j = 0
        i = i + 1
    if ch == "1":
        meiro[i][j] += 1
    if ch == "2":
        meiro[i][j] += 2
    j = j + 1

c = 600 // meiro_size




a_crane = 4
b_crane = 2

winFlg = False
font = pygame.font.Font(None, c*165//100)

action_list = [[-1, 0, 0], [0, 1, 0], [0, -1, 0], [-1, 0, 0], [0, 0, 1], [0, 1, 0], [0, -1, 0], [1, 0, 0], [0, 1, 0], [-1, 0, 0], [0, -1, 0], [0, -1, 0], [-1, 0, 0], [0, 1, 0], [1, 0, 0], [0, 1, 0], [1, 0, 0], [0, 0, -1], [-1, 0, 0], [-1, 0, 0], [0, -1, 0], [0, -1, 0], [1, 0, 0], [1, 0, 0], [-1, 0, 0], [1, 0, 0], [-1, 0, 0], [0, 0, 1], [1, 0, 0], [0, 0, -1], [0, 1, 0], [-1, 0, 0], [1, 0, 0], [-1, 0, 0], [-1, 0, 0], [0, 0, 1], [0, 1, 0], [0, 0, -1]]
       
while True: # main game loop
    screen.fill((0,0,0))
    text = font.render("C", True, (255,255,255))   
    screen.blit(text, [b_crane*c,a_crane*c])
    for i in range(meiro_size):
        for j in range(meiro_size):
                if meiro[i][j] == 1:
                    pygame.draw.rect(screen,(0,150,0),Rect(j*c,i*c,c,c))
                if meiro[i][j] == 2:
                    pygame.draw.rect(screen,(150,0,0),Rect(j*c,i*c,c,c))
    
            
    for event in pygame.event.get():
        lift = 0
        for i in range(len(action_list)):
            time.sleep(0.1)
            pygame.display.update()
            if lift == 0:
                a_crane = a_crane + action_list[i][0]
                b_crane = b_crane + action_list[i][1]
                
                if action_list[i][2] == 1:
                    lift += 1
                    
            if lift == 1:
                meiro[a_crane][b_crane] -= 2
                a_crane = a_crane + action_list[i][0]
                b_crane = b_crane + action_list[i][1]
                meiro[a_crane][b_crane] += 2

                if action_list[i][2] == -1:
                    lift -= 1
                    
            screen.fill((0,0,0))
            for i in range(meiro_size):
                for j in range(meiro_size):
                        if meiro[i][j] == 1:
                            pygame.draw.rect(screen,(0,150,0),Rect(j*c,i*c,c,c))
                        if meiro[i][j] >= 2:
                            pygame.draw.rect(screen,(150,0,0),Rect(j*c,i*c,c,c))
            screen.blit(text, [b_crane*c,a_crane*c])
            # print(meiro)    
            # print(a_crane,b_crane,lift)
            
        winFlg = True
        if winFlg:
            time.sleep(2)
            pygame.quit()
            sys.exit()
    



       
        
        if event.type == QUIT:

            pygame.quit()

            sys.exit()

    pygame.display.update()