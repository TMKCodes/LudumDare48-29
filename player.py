#! /usr/bin/python

import pygame
from pygame.locals import *
from entity import *
from bullet import *
from load import *

class Player(Entity):
	def __init__(self, sprite_name, world, entities, mapx, mapy, x, y):
		Entity.__init__(self)
		self.load = Load()
		self.mapx = mapx
		self.mapy = mapy
		self.world = world
		self.entities = entities
		self.xvel = 0
		self.yvel = 0
		self.onGround = False
		self.rect = pygame.Rect(mapx*self.world.mwidth*64+(x*64), mapy*self.world.mheight*64+(y*64), 64, 64)
		self.lastx = x
		self.lasty = y
		self.lastimage = None
		self.sprite_name = sprite_name
		self.load_image("%s-front.png" % self.sprite_name)
 		self.weapon = None
		self.oil_amount = 100
		self.pistol_bullets = 200
		self.assault_rifle_bullets = 100
		self.type = "alive"
		self.player = True
		self.game_complete = False
		self.jump_sound = self.load.sound("jump.wav")
		self.assault_rifle_sound = self.load.sound("assault-rifle.wav")
		self.collision_sound = self.load.sound("collision.wav")
		self.jump_sound = self.load.sound("jump.wav")
		self.melt_sound = self.load.sound("melt.wav")
		self.pistol_sound = self.load.sound("pistol.wav")
		self.radio_sound = self.load.sound("radio.wav")
		self.facing = None
	def load_image(self, name):
		self.image, _ = self.load.image(name, -1)

	def update(self, up=False, running=False, down=False, left=False, right=False, melt=False, pause=False, weapon=False, shoot=False):
		#print "Player pos", self.mapx, self.mapy, self.rect.x, self.rect.y
		run = 0
		if up == True:
			self.facing = "up"
			if self.onGround: 
				self.yvel -= 10	
				self.jump_sound.play()
		if running == True:
			run = 5
		if down == True: 
			self.facing = "down"
			self.lastimage = "front"
			self.load_image("%s-front.png" % self.sprite_name)
		if left == True:
			self.facing = "left"
			self.xvel += -(8 + run)
		if right == True:
			self.facing = "right"
			self.xvel += 8 + run
		if melt == True:
			if self.weapon == "torch":
				for m in self.world.get_open_maps():
					if m != False:
						if self.facing == "up":
							block = m.get_block_top(self.rect.x, self.rect.y)
							if block != False:
								if block.block == "oil-pocket-block":	
									self.oil_amount += 10
								if self.oil_amount >= 5:
									self.melt_sound.play()
									self.oil_amount -= 5;
									block.kill()
						elif self.facing == "down":
							block = m.get_block_bottom(self.rect.x, self.rect.y)
							if block != False:
								if block.block == "oil-pocket-block":
									self.oil_amount += 10
								if self.oil_amount >= 5:
									self.melt_sound.play()
									self.oil_amount -= 5;
									block.kill()
						elif self.facing == "left":
							block = m.get_block_left(self.rect.x, self.rect.y)
							if block != False:
								if block.block == "oil-pocket-block":
									self.oil_amount += 10
								if self.oil_amount >= 5:
									self.melt_sound.play()
									self.oil_amount -= 5;
									block.kill()
						elif self.facing == "right":
							block = m.get_block_right(self.rect.x, self.rect.y)
							if block != False:
								if block.block == "oil-pocket-block":
									self.oil_amount += 10
								if self.oil_amount >= 5:
									self.melt_sound.play()
									self.oil_amount -= 5;
									block.kill()	
		if not self.onGround:
			self.yvel += 0.1
			if self.yvel > 100: self.yvel == 100
		if not (left == True or right == True):
			self.xvel = 0
		if pause == True:
			if self.lastimage == "walk-right-right-leg" or self.lastimage == "walk-right-left-leg":
				self.lastimage = "stand-right"
				self.load_image("%s-stand-right.png" % self.sprite_name)
			elif self.lastimage == "walk-left-left-leg" or self.lastimage == "walk-left-right-leg":
				self.lastimage = "stand-left"
				self.load_image("%s-stand-left.png" % self.sprite_name)
		if weapon == True:
			if self.weapon == None:
				self.weapon = "torch"
				print "Set weapon torch"
			elif self.weapon == "torch":
				self.weapon = "pistol"
				print "Set weapon pistol"
			elif self.weapon == "pistol":
				self.weapon = "assault-rifle"
				print "Set weapon assault-rifle"
			elif self.weapon == "assault-rifle":
				self.weapon = "radio"
				print "Set weapon radio"
			elif self.weapon == "radio":
				self.weapon = None
				print "Set weapon none"
		if shoot == True:
			if self.weapon != None:
				if self.weapon == "radio":
					radio_usable = True
					for m in self.world.get_open_maps():
						for block in m.blocks.sprites():
							if block.rect.x == self.rect.x:
								print "block %s,%s blocked radio." % (block.rect.x, block.rect.y)
								radio_usable = False
							if block.rect.y == self.rect.y:
								print "block %s,%s blocked radio." % (block.rect.x, block.rect.y)
								radio_usable = False
					if radio_usable == True:
						if self.onGround:
							self.radio_sound.play()
							print "Completed the game."
							self.game_complete = True
				elif self.weapon == "pistol":
					if self.pistol_bullets >= 1:
						if self.facing == "left" or self.facing == "right":
							self.pistol_sound.play()
							direction = self.facing
							self.pistol_bullets -= 1
							self.entities.add(Bullet(self.world, self.entities, self.mapx, self.mapy, self.rect.x, self.rect.y, direction))
				elif self.weapon == "assault-rifle":
					if self.assault_rifle_bullets >= 1:
						if self.facing == "left" or self.facing == "right":
							self.assault_rifle_sound.play()	
							direction = self.facing
							self.assault_rifle_bullets -= 1
							self.entities.add(Bullet(self.world, self.entities, self.mapx, self.mapy, self.rect.x, self.rect.y, direction))
		self.rect.left += self.xvel
		self.collide(self.xvel, 0)
		self.rect.top += self.yvel
		self.onGround = False;
		self.collide(0, self.yvel)
		cat = 8
		self.newimage = None
		if self.rect.x >= self.lastx + cat:
			if self.lastimage != "walk-right-right-leg" and self.lastimage != "walk-right-left-leg":
				self.newimage = "walk-right-right-leg"
			if self.lastimage == "walk-right-right-leg":
				self.newimage = "walk-right-left-leg"
			elif self.lastimage == "walk-right-left-leg":
				self.newimage = "walk-right-right-leg"
		elif self.rect.x <= self.lastx - cat:
			if self.lastimage != "walk-left-left-leg" and self.lastimage != "walk-left-right-leg":
				self.newimage = "walk-left-left-leg"
			elif self.lastimage == "walk-left-left-leg":
				self.newimage = "walk-left-right-leg"
			elif self.lastimage == "walk-left-right-leg":
				self.newimage = "walk-left-left-leg"
		if self.newimage != None:
			self.lastx = self.rect.x
			self.lasty = self.rect.y
			self.lastimage = self.newimage;
			img = "%s-%s.png" % (self.sprite_name, self.newimage)
			self.load_image(img)
	def collide(self, xvel, yvel):
		maps = self.world.get_open_maps()
		for m in maps:	
			for block in m.blocks.sprites():		
				if pygame.sprite.collide_rect(self, block):
					if xvel > 0:
						self.collision_sound.play()
						self.rect.right = block.rect.left
						#print "collide right"
						self.facing = "right"
						self.load_image("%s-stand-right.png" % self.sprite_name)
					if xvel < 0:
						self.collision_sound.play()
						self.rect.left = block.rect.right
						#print "collide left"
						self.facing = "left"
						self.load_image("%s-stand-left.png" % self.sprite_name)
					if yvel > 0:
						self.rect.bottom = block.rect.top
						#print "collide bottom"
						#print "block", block.block
						if block.block == "ice-block" or block.block == "ice-two-block" or block.block == "oil-pocket-block":
							self.onGround = True
					if yvel < 0:
						self.collision_sound.play()
						#print "collide top"
						self.rect.top = block.rect.bottom
						yvel = 0
