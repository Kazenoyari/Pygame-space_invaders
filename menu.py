#///////////////////////////////////////////////////////////
#
# Contains the game menus. 
#
# Uses full screen flip for drawing
#
#///////////////////////////////////////////////////////////

import sys, pygame, color, settings
from classes import *

loop = True

# FUnctions passed to the buttons
 
def quitGame():
	sys.exit()

def startGame():
	global loop
	loop = False

def returnMenu():
	global loop
	loop = False

# Function used for the drawing loop of the menu
def menuLoop(screen,clock,option_list,title=None,titleRect=None,subTitle=None,subTitleRect=None):

	all_sprites = pygame.sprite.LayeredDirty()
	for button in option_list:
		all_sprites.add(button)

	option_selected = 0

	#Create a pointer sprite
	pointer = pygame.sprite.DirtySprite()
	pointer.image = pygame.Surface((10,10)).convert()
	pointer.image.fill(color.WHITE)
	pointer.rect = pointer.image.get_rect()
	all_sprites.add(pointer)
	
	#Bacground for dirty rectangle clear function

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill(color.BLACK)
	#Draw the menu title on the background
	if (title != None) and (titleRect != None):
		background.blit(title,(titleRect.x,titleRect.y))

	if (subTitle != None) and (subTitleRect != None):
		background.blit(subTitle,(subTitleRect.x,subTitleRect.y))

	#Clean the screen
	screen.fill(color.BLACK)
	pygame.display.flip()


	while loop:
		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				sys.exit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_DOWN:
					pointer.dirty = 1
					option_selected += 1
					if option_selected > 1:
						option_selected = 0
				if event.key == pygame.K_UP:
					pointer.dirty = 1
					option_selected -= 1
					if option_selected < 0:
						option_selected = 1
				if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
					option_list[option_selected].action()

		if pointer.dirty == 1:
			pointer.rect.center = option_list[option_selected].rect.center
			pointer.rect.x = option_list[option_selected].rect.x - 20

		all_sprites.clear(screen, background)
		dirtyRects = all_sprites.draw(screen)
		pygame.display.update(dirtyRects)

		clock.tick(60)


def mainMenu(screen,clock,size):

	global loop
	loop = True
	option_list = []

	startButton = Button(screen, (size[0]/2 ,size[0]/2), text='Start Game', fontSize=25, color=color.WHITE, action=startGame)
	quitButton = Button(screen, (size[0]/2,size[0]/2 + 50), text='Quit', fontSize=25, color=color.WHITE, action=quitGame)

	option_list.append(startButton)
	option_list.append(quitButton)

	titleText = pygame.font.Font(None, 50)
	title = titleText.render('Space Invaders',0,color.WHITE)
	titleRect = title.get_rect(center=(size[0]/2, 25))

	menuLoop(screen,clock,option_list,title=title,titleRect=titleRect)

def gameOver(screen, clock, size, score):

	global loop
	loop = True
	option_list = []

	returnButton = Button(screen, (size[0]/2 ,size[0]/2), text='Back to main menu', fontSize=25, color=color.WHITE, action=returnMenu)
	quitButton = Button(screen, (size[0]/2 ,size[0]/2 + 50), text='Quit', fontSize=25, color=color.WHITE, action=quitGame)

	option_list.append(returnButton)
	option_list.append(quitButton)

	titleText = pygame.font.Font(None, 50)
	title = titleText.render('Game Over',0,color.WHITE)
	titleRect = title.get_rect(center=(size[0]/2,25))

	scoreText = pygame.font.Font(None, 30)
	playerScore = scoreText.render('Your score: ' + str(score),0,color.WHITE)
	scoreRect = playerScore.get_rect(center=(size[0]/2,75))

	menuLoop(screen,clock,option_list,title=title,titleRect=titleRect,subTitle=playerScore ,subTitleRect=scoreRect)