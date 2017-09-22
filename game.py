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

	loop = True

	#Creation of game objects

	alien_group = pygame.sprite.Group() #Group for alien objects
	bullet_group = pygame.sprite.Group() #Group for bullet objects
	sfx_group = pygame.sprite.LayeredDirty() #Group for sfx objects
	all_sprites = pygame.sprite.LayeredDirty() #Group for all objects

	ship = Ship(loc=(125, 200))
	all_sprites.add(ship)

	alien1 = Alien(loc=(50, 50), sway=50)
	alien2 = Alien(loc=(125, 50), sway=50)
	alien3 = Alien(loc=(200, 50), sway=50)
	alien4 = Alien(loc=(50, 10), sway=50)
	alien5 = Alien(loc=(125, 10), sway=50)
	alien6 = Alien(loc=(200, 10), sway=50)	
	alien_group.add(alien1)
	alien_group.add(alien2)
	alien_group.add(alien3)
	alien_group.add(alien4)
	alien_group.add(alien5)
	alien_group.add(alien6)

	for alien in alien_group:
		all_sprites.add(alien)

	fire = Sfx('fire.png', loc=(20,268), speed=100, loop=1, size=(32,32))
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
		    	reaction = ship.action(event)
		    	if type(reaction) is Bullet:
		    		bullet_group.add(reaction)
		    		all_sprites.add(reaction)


		ship.move()
		for bullet in bullet_group.sprites(): # Update position of all bullets
			bullet.move()
		for alien in alien_group.sprites(): # Update position for all alines and check if the hit a bullet
			alien.move()
			alien.checkHit(bullet_group)
			if alien.rect.centery > size[1] - 50 or alien.rect.colliderect(ship.rect):
				#If any alien gets to the bottomb of the screen or collides with the player ship,
				#stop the game loop and return 0 (loose)
				loop = False			
				return 0

		if not alien_group.sprites():
			#If there are no more aliens, stop the game loop and return 1 (win)
			loop = False		
			return 1

		#ship.anim()
		fire.anim()
		all_sprites.clear(screen, background) #clear all the sprites to draw them again
		dirtyRects = all_sprites.draw(screen) #Save all the rects of the sprites that need redrawing
		pygame.display.update(dirtyRects) #Redraw all rects in dirtyRects

		clock.tick(60)