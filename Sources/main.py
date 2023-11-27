#import login
import pygame
import const as c
import build_map as b
screen = pygame.display.set_mode((c.SCREEN_WIDTH, c.SCREEN_HEIGHT)) 
b.sokoban(screen, 0)
#login.init()