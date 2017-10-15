#///////////////////////////////////////////////////////////
#
# Game clases. Contains clases for both the game and the
# menus. Contains also the groups.
#
#///////////////////////////////////////////////////////////

import pygame, color, settings, random

# alien_group = pygame.sprite.Group() #Group for alien objects
# bullet_group = pygame.sprite.Group() #Group for bullet objects
# sfx_group = pygame.sprite.LayeredDirty() #Group for sfx objects
# all_sprites = pygame.sprite.LayeredDirty() #Group for all objects

IMAGES_SOURCE = 'images/'


def spriteImages(spritesheet, size):

	# Function for loading a list of images from a main image or 
	# spritesheet. Takes a string with the image to load and a
	# tuple with the size of the images to be returned

	sheet = pygame.image.load(IMAGES_SOURCE+spritesheet).convert_alpha()
	sheet_size = sheet.get_size()
	columns = int(sheet_size[0] / size[0])
	rows = int(sheet_size[1] / size[1])
	images = []
	image_rect = pygame.Rect(0,0,size[0],size[1])

	for row in range(0, rows):
		image_rect.y = (size[1] * row)
		for column in range(0, columns):
			image_rect.x = (size[0] * column)
			image = pygame.Surface(size)
			image.blit(sheet,(0,0),area=image_rect)
			images.append(image.convert_alpha())
		image_rect.x = 0
		
	return images


#Main menu classes

class Button(pygame.sprite.DirtySprite):

	# Class for the buttons in menus. 
	# Parameters:
	# 	screen: screen object in use
	# 	cords: tuple with cordinates x,y where the button should be centered
	# 	font: font of the text, default: None
	# 	fontSize(optional): integer with size of the font, default: 10
	#	color: tuple with rgb value of the color for the font, default: (0,0,0)
	#	action: function to call when the button is pressed, default: None

	def __init__(self, screen, cords, text='', font=None, fontSize=10, color=(0,0,0), action=None):
		super().__init__()
		self.center = cords
		self.color = color
		self.action = action
		self.fontSize = fontSize
		self.font = font
		self.screen = screen

		self.textObject = pygame.font.Font(font, fontSize)
		self.image = self.textObject.render(text,0,color)
		self.rect = self.image.get_rect(size=self.textObject.size(text),center=self.center)

	# def draw(self):
	# 	self.screen.blit(self.image,(self.rect.x,self.rect.y))

	def action(self):
		if self.action != None:
			self.action()


#Game classes

class Sfx(pygame.sprite.DirtySprite):

	# Class for animated or static sfx. 
	# Parameters:
	# 	sprite_image: string with the image or spritesheet to use
	# 	loc: tuple with cordinates x,y of the topleft of the sfx. Default: (0,0)
	# 	parent_rect: rectangle that the sfx should follow. Default: None
	#   			 if None or nothing is passed, the sfx will stay at the corfinates stablished by the loc parameter
	# 	speed: integer with the speed of the animation in miliseconds, Default: 10
	#	loop: sets if the animation should loop (!=0) or run only once (0). Default: 0
	#		  if 0, the object will be killed after running.
	#	size: tuple with size of the sfx, Default:(8,8)

	def __init__(self, sprite_image, loc=(0,0), parent_rect=None, speed=10, loop=0, size=(8,8), rot=0):
		super().__init__()
		self.images = spriteImages(sprite_image, size)
		if rot != 0:
			for i in range(0,len(self.images)):
				 self.images[i] = pygame.transform.rotate(self.images[i],rot)
		self.image = self.images[0]
		if parent_rect == None:
			self.rect = self.image.get_rect()
			self.rect.x = loc[0]
			self.rect.y = loc[1]
		else:
			self.rect = parent_rect
		self.speed = speed
		self.size = size
		self.loop = loop
		self.frame = 0
		self.last_frame = pygame.time.get_ticks()

	def anim(self):

		#If the diference beetween the time at the last frame and the current time is equal or
		#greater than the set speed, change frame. If loop is set to 0, kill the sfx after
		#it finishes looping

		now = pygame.time.get_ticks()
		if (now - self.last_frame) >= self.speed:
			self.frame = self.frame + 1
			if self.frame > (len(self.images)-1):
				if self.loop == 0:
					self.kill()
				else:
					self.frame = 0
			self.image = self.images[self.frame]
			self.last_frame = pygame.time.get_ticks()
			self.dirty = 1


class Ship(pygame.sprite.DirtySprite):

	# Class for main player ship. 
	# Parameters:
	# 	locx: x cordinate for the topleft corner
	# 	locy: y cordinate for the topleft corner


	def __init__(self, loc=(0,0)):
		super().__init__()
		self.image_list = spriteImages('ship_sheet.png', (32,32))
		self.image = self.image_list[0]
		self.rect = self.image.get_rect()
		self.rect.x = loc[0]
		self.rect.y = loc[1]
		self.frame = 1

		self.speedx = 0
		self.speedy = 0
		self.speed_left = 0
		self.speed_right = 0

	def move(self):
		self.speedx = self.speed_right - self.speed_left
		if (self.speedx + self.rect.left) <= 0 or (self.speedx + self.rect.right) >= settings.size[1]:
			self.speedx = 0
		self.rect.x = self.rect.x + self.speedx
		self.dirty = 1

	def action(self, event):
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_RIGHT:
				self.speed_right = 2
			if event.key == pygame.K_LEFT:
				self.speed_left = 2
			if event.key == pygame.K_SPACE:
				bullet = Bullet(1,(self.rect.centerx, self.rect.centery - (self.rect.height/2 + 10)))
				return bullet

		if event.type == pygame.KEYUP:
			if event.key == pygame.K_RIGHT:
				self.speed_right = 0
			if event.key == pygame.K_LEFT:
				self.speed_left = 0

		
class Bullet(pygame.sprite.DirtySprite):

	# Class for bullets. Currently only used for the main player ship.. 
	# Parameters:
	# 	locx: x cordinate for the topleft corner
	# 	locy: y cordinate for the topleft corner

	speed = -5 #Global variable for bullet speed
	damage = 1 #Global variable for bullet damage

	def __init__(self,direction, loc=(0,0)):
		super().__init__()
		#self.image = pygame.image.load(IMAGES_SOURCE+'bullet.png')
		self.direction = direction
		if direction >= 1:
			self.speed = Bullet.speed
			rot = 0
		else:
			self.speed = -Bullet.speed
			rot = 180
		self.origin = None
		self.image = pygame.Surface((16,16))
		self.image.set_alpha(100)
		self.rect = self.image.get_rect()
		self.rect.centerx = loc[0]
		self.rect.centery = loc[1]
		self.anim = Sfx('bullet_sheet.png', parent_rect=self.rect, speed=100, loop=1, size=(16,16), rot=rot)


	def move(self):
		self.rect.y = self.rect.y + self.speed
		#self.anim.rect = self.rect
		if (self.rect.y < -self.rect.height) or (self.rect.y > 640): #Dissapear if it hits the top of the screen
			self.anim.kill()
			self.kill()
		self.dirty = 1

	def kill(self):
		self.anim.kill()
		super().kill()

	# def draw(self):
	# 	super.draw()
	# 	self.anim.draw()

class Alien(pygame.sprite.DirtySprite):

	# Class for aliens.
	# Parameters:
	# 	locx: x cordinate for the topleft corner
	# 	locy: y cordinate for the topleft corner
	# 	sway: amount of pixels the alien moves to the left and the right


	def __init__(self, loc=(0,0), sway=0):
		super().__init__()
		#self.image = pygame.image.load(IMAGES_SOURCE+'alien.png')
		self.frame = 0
		self.images =  spriteImages('alien_sheet.png',(25,24))
		self.image = self.images[self.frame]
		self.rect = self.image.get_rect()
		self.rect.x = loc[0]
		self.rect.y = loc[1]

		self.speed = 6
		self.health = 1
		self.pivot = self.rect.centerx #Center of the origin of the aline. Pivot for the swaying movement
		self.sway = sway
		self.last_move = pygame.time.get_ticks()

	def move(self):
		now = pygame.time.get_ticks()
		if (now - self.last_move) >= 600:
			self.last_move = pygame.time.get_ticks()
			self.rect.x = self.rect.x + self.speed
			if self.rect.left > (self.pivot + self.sway) or self.rect.left < (self.pivot - self.sway):
				self.speed = -self.speed
				self.rect.y = self.rect.y + 6
			if self.frame == len(self.images)-1:
				self.frame = 0
			else:
				self.frame = self.frame + 1
			self.image = self.images[self.frame]
			self.dirty = 1

	def shoot(self):
		if random.randint(0, 5000) > 4999:
			bullet = Bullet(0,(self.rect.centerx, self.rect.centery + (self.rect.height/2 + 10)))
			return bullet

	def checkHit(self, bullet_group):
		if pygame.sprite.spritecollide(self, bullet_group, True): #Kill it if it collides with  bullet
			self.kill()
			return True
		else:
			return False


class Shield(pygame.sprite.DirtySprite):

	def __init__(self, loc=(0,0), corner=None):
		super().__init__()
		self.health = 5
		self.images =  spriteImages('shield_sheet.png',(25,25))
		#self.image = pygame.Surface((25,25))
		#self.image.fill(color.WHITE)

		if corner != None:
			self.frame = 5
			if corner == 'right':
				for i in range(0,len(self.images)):
					self.images[i] = pygame.transform.flip(self.images[i],1,0)
		else:
			self.frame = 0

		self.image = self.images[self.frame]
		self.rect = self.image.get_rect()
		self.rect.x = loc[0]
		self.rect.y = loc[1]

	def checkHit(self, bullet_group):
		if pygame.sprite.spritecollide(self, bullet_group, True): #Kill it if it collides with  bullet
			self.health -= 1
			if not (self.health):
				self.kill()
			else:
				self.frame += 1
				self.image = self.images[self.frame]
				self.dirty = 1

	def createShield(group,loc=(0,0)):
		group.add(Shield(loc=(loc[0] + (25),loc[1]), corner="left"))
		group.add(Shield(loc=(loc[0] + (25*2),loc[1])))
		group.add(Shield(loc=(loc[0] + (25*3),loc[1])))
		group.add(Shield(loc=(loc[0] + (25*4),loc[1]), corner="right"))
		group.add(Shield(loc=(loc[0] + (25),loc[1]+25)))
		group.add(Shield(loc=(loc[0] + (25*4),loc[1]+25)))



class TextSprite(pygame.sprite.DirtySprite): #Class for creating text with sprite characteristics

	def __init__(self,text, loc=(0,0), centered=False,fontSize=25,color=(255,255,255)):
		super().__init__()
		self.font = pygame.font.Font(None, fontSize)
		self.fontSize = fontSize
		self.text = text
		self.color = color
		self.image = self.font.render(text,0,color)
		self.loc = loc
		self.centered = centered
		if centered:
			self.rect = self.image.get_rect(center=loc)
		else:
			self.rect = self.image.get_rect(topleft=loc)

	def changeFont(self, font):
		self.font = pygame.font.Font(font, self.fontSize);
		self.recalculate()

	def changeSize(self, newSize):
		self.font.size(newSize)
		self.recalculate()

	def changeText(self, text):
		self.text = text
		self.recalculate()

	def changeColor(self, color):
		self.color = color
		self.image = self.font.render(self.text,0,color)
		self.dirty = 1

	def recalculate(self):
		self.image = self.font.render(self.text,0,self.color)
		if self.centered:
			self.rect = self.image.get_rect(center=self.loc)
		else:
			self.rect = self.image.get_rect(topleft=self.loc)
		self.dirty = 1



############# NOTES ##############################################

# Blit(source,dest,area=rect)
# 	source: image from where to copy
#	dest: cordinates for where the drwing should start in the image you are copying to.
#		  origin is at (0,0) and is the topleft corner
#	area: rectangle that selects a part of the source to copy from