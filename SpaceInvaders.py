#///////////////////////////////////////////////////////////
#
# Starter file. Run this file to start the game
#
#///////////////////////////////////////////////////////////

import sys, pygame, settings
import menu
import game


pygame.init()

screen = pygame.display.set_mode(settings.size) #Create screen and window
pygame.display.set_caption("Space Invaders") #Set window title
clock = pygame.time.Clock() #Create clock object for keeping time

result = [0] #Result of the game. 0=loose, 1=win

while 1:
	menu.mainMenu(screen,clock,settings.size)
	result = game.run(screen,clock,settings.size)
	menu.gameOver(screen,clock,settings.size,result)