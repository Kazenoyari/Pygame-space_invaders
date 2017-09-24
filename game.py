#///////////////////////////////////////////////////////////
#
# Main game file. Contains the actual game.
# Its in charge of creating the objects and  drawing them
# on the screen, recieving keyboard events and handling
# the win and loose logic.
# 
# Uses dirty rectangles for drawing
#
#///////////////////////////////////////////////////////////

import sys, pygame, color, settings
from classes import *

def run(screen,clock,size):

	#Flag for running the game. Set to 0 or False to end the game
	loop = True
	#FLags for pause menu logic
	pause = False
	exit_pause = False
	start_pause = False

	pause_snapshot = pygame.Surface((128,128))
	pause_image = pygame.image.load("images/pause.png").convert_alpha()

	#Creation of game objects

	alien_group = pygame.sprite.Group() #Group for alien objects
	bullet_group = pygame.sprite.Group() #Group for bullet objects
	sfx_group = pygame.sprite.LayeredDirty() #Group for sfx objects
	all_sprites = pygame.sprite.LayeredDirty() #Group for all objects

	ship = Ship(loc=((settings.size[0] / 2)-50,(settings.size[1] - 150)))
	all_sprites.add(ship)

	for i in range(1,5):
		for f in range(1,10):
			alien = Alien(loc=(5 + (f*42), 50 * i), sway=50)
			alien_group.add(alien)

	for alien in alien_group:
		all_sprites.add(alien)

	fire = Sfx('fire.png', loc=(20,settings.size[1]-32), speed=100, loop=1, size=(32,32))
	sfx_group.add(fire)
	all_sprites.add(fire)


	#Bacground for dirty rectangle clear function

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

	#Clean the screen

	screen.fill(color.BLACK)
	pygame.display.flip()

	#Main game loop

	while loop:
		for event in pygame.event.get():
		    if event.type == pygame.QUIT: 
		    	sys.exit()
		    else:
		    	if pause:
		    		if event.type == pygame.KEYDOWN:
		    			if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
		    				pause = False
		    				exit_pause = True
		    	else:
		    		if event.type == pygame.KEYDOWN:
		    			if event.key == pygame.K_ESCAPE or event.key == pygame.K_p:
		    				pause = True
		    				start_pause = True			
			    	reaction = ship.action(event)
			    	if type(reaction) is Bullet:
			    		bullet_group.add(reaction)
			    		all_sprites.add(reaction)

		if not pause and not exit_pause:
			ship.move()
			for bullet in bullet_group.sprites(): # Update position of all bullets
				bullet.move()
			for alien in alien_group.sprites(): # Update position for all alines and check if the hit a bullet
				alien.move()
				alien.checkHit(bullet_group)
				if alien.rect.centery > (settings.size[1] - 50) or alien.rect.colliderect(ship.rect):
					#If any alien gets to the bottomb of the screen or collides with the player ship,
					#stop the game loop and return 0 (loose)
					loop = False			
					return 0

			if not alien_group.sprites():
				#If there are no more aliens, stop the game loop and return 1 (win)
				loop = False		
				return 1

		if start_pause: #Saves the state of the screen affected by the pause menu before pausing
			pause_rect = pause_image.get_rect()
			pause_rect.topleft = ((settings.size[0] / 2)-64,200)
			display_screen = pygame.display.get_surface()
			pause_snapshot.blit(display_screen,(0,0), area=pause_rect) 


		fire.anim()
		all_sprites.clear(screen, background) #clear all the sprites to draw them again
		dirtyRects = all_sprites.draw(screen) #Save all the rects of the sprites that need redrawing
		if pause: #Draws the pause menu
			dirtyRects.append(screen.blit(pause_image,((settings.size[0] / 2)-64, 200)))
			start_pause = False
		if exit_pause: #Restores the screen affected by the pause menu
			dirtyRects.append(screen.blit(pause_snapshot,((settings.size[0] / 2)-64, 200)))
			exit_pause = False
		pygame.display.update(dirtyRects) #Redraw all rects in dirtyRects

		clock.tick(60)