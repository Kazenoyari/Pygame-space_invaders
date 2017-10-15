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


def newLevel(level,alien_group,sprite_group):
	for i in range(1,5):
		for f in range(1,10):
			alien = Alien(loc=(5 + (f*42), (50 * i)+(20 * (level-1))), sway=50)
			alien_group.add(alien)

	for alien in alien_group:
		sprite_group.add(alien)

def run(screen,clock,size):

	#Flag for running the game. Set to 0 or False to end the game
	loop = True
	#FLags for pause menu logic
	pause = False
	exit_pause = False
	start_pause = False

	level = 1
	score = 0

	pause_snapshot = pygame.Surface((128,128))
	pause_image = pygame.image.load("images/pause.png").convert_alpha()

	#Creation of game objects

	alien_group = pygame.sprite.Group() #Group for alien objects
	player_bullets = pygame.sprite.Group() #Group for bullet objects
	alien_bullets = pygame.sprite.Group()
	shield_group = pygame.sprite.Group()
	sfx_group = pygame.sprite.LayeredDirty() #Group for sfx objects
	all_sprites = pygame.sprite.LayeredDirty() #Group for all objects

	ship = Ship(loc=((settings.size[0] / 2)-50,(settings.size[1] - 150)))
	all_sprites.add(ship)


	Shield.createShield(shield_group,loc=(25,(settings.size[1] - 250)))
	Shield.createShield(shield_group,loc=((settings.size[0] / 2)-75,(settings.size[1] - 250)))
	Shield.createShield(shield_group,loc=(settings.size[0]-175,(settings.size[1] - 250)))
	for shield in shield_group:
		all_sprites.add(shield)
	
	#Bacground for dirty rectangle clear function

	background = pygame.Surface(screen.get_size())
	background = background.convert()
	background.fill((0, 0, 0))

	levelText = TextSprite('Level ' + str(level), loc=(settings.size[0]/2, 25), centered=True)
	all_sprites.add(levelText)
	scoreText = TextSprite('Score: ' + str(score), loc=(25, 17))
	all_sprites.add(scoreText)

	newLevel(level, alien_group, all_sprites)

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
			    		if len(player_bullets.sprites()):
			    			reaction.kill()
			    		else:
				    		player_bullets.add(reaction)
				    		sfx_group.add(reaction.anim)
				    		all_sprites.add(reaction)
				    		all_sprites.add(reaction.anim)

		if not pause and not exit_pause:
			ship.move()
			for bullet in player_bullets.sprites(): # Update position of all player bullets
				bullet.move()
			for bullet in alien_bullets.sprites(): # Update position of all enemy bullets
				bullet.move()
			for block in all_sprites.sprites():
				if type(block) is Shield:
					block.checkHit(player_bullets)
					block.checkHit(alien_bullets)
			for alien in alien_group.sprites(): # Update position for all alines and check if the hit a bullet
				alien.move()
				shoot = alien.shoot()
				if type(shoot) is Bullet:
					alien_bullets.add(shoot)
					sfx_group.add(shoot.anim)
					all_sprites.add(shoot)
					all_sprites.add(shoot.anim)
				if alien.checkHit(player_bullets):
					score += 10
					scoreText.changeText('Score: ' + str(score))
				alien.checkHit(shield_group):
				if alien.rect.centery > (settings.size[1] - 50) or alien.rect.colliderect(ship.rect) or  pygame.sprite.spritecollide(ship, alien_bullets, True):
					#If any alien gets to the bottomb of the screen or collides with the player ship,
					#stop the game loop and return 0 (loose)
					loop = False			
					return 0

			if not alien_group.sprites(): #If there are no more aliens
				level += 1
				if level > 10:
					#If reached level 10, stop the game loop and return 1 (win)
					loop = False		
					return 1
				else:
					newLevel(level, alien_group, all_sprites)
					levelText.changeText('Level ' + str(level))

		if start_pause: #Saves the state of the screen affected by the pause menu before pausing
			pause_rect = pause_image.get_rect()
			pause_rect.topleft = ((settings.size[0] / 2)-64,200)
			display_screen = pygame.display.get_surface()
			pause_snapshot.blit(display_screen,(0,0), area=pause_rect) 


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