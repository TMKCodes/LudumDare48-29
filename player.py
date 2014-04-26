#! /usr/bin/python

import pygame
from pygame.locals import *
from entity import *
from load import *

class Player(Entity):
	def __init__(self, sprite_name, world, mapx, mapy, x, y):
		Entity.__init__(self)
		self.load = Load()
		self.mapx = mapx
		self.mapy = mapy
		self.world = world
		self.xvel = 0
		self.yvel = 0
		self.onGround = False
		self.rect = pygame.Rect(mapx*self.world.width*64+(x+1)*64, mapy*self.world.height*64+(y+1)*64, 64, 64)
		self.lastx = x
		self.lasty = y
		self.lastimage = None
		self.sprite_name = sprite_name
		self.load_image("%s-front.png" % self.sprite_name)
 	
	def load_image(self, name):
		self.image, _ = self.load.image(name, -1)

	def update(self, event=None):
		self.xvel = 0
		self.yvel = 0
		#print "Player pos", self.mapx, self.mapy, self.rect.x, self.rect.y
		if event == "up":
			if self.onGround: self.yvel -= 11
		if event == "running":
			self.xvel += 12
		if event == "down": 
			self.lastimage = "front"
			self.load_image("%s-front.png" % self.sprite_name)
		if event == "left":
			self.xvel += -8
		if event == "right":
			self.xvel += 8
		if not self.onGround:
			self.yvel += 0.3
			if self.yvel > 100: self.yvel == 100
		if not (event == "left" or event == "right"):
			self.xvel = 0
		if event == "pause":
			if self.lastimage == "walk-right-right-leg" or self.lastimage == "walk-right-left-leg":
				self.lastimage = "stand-right"
				self.load_image("%s-stand-right.png" % self.sprite_name)
			elif self.lastimage == "walk-left-left-leg" or self.lastimage == "walk-left-right-leg":
				self.lastimage = "stand-left"
				self.load_image("%s-stand-left.png" % self.sprite_name)
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
		'''
		m = self.world.get_current_map(self.mapx, self.mapy) 
		if m != False:
			if self.rect.x > m.get_width():
				self.world.load_maps(self.rect.x, self.rect.y)
				# self.lastx = 0
			elif self.rect.x < 0:
				self.world.load_maps(self.rect.x, self.rect.y)
				# self.lastx = m.get_width()
			elif self.rect.y > m.get_height(): 
				self.world.load_maps(self.rect.x, self.rect.y)
				# self.lasty = 0
			elif self.rect.x < 0:
				self.world.load_maps(self.rect.x, self.rect.y)
				# self.lasty = m.get_height()
		else:
			print "Failed to get current map at", self.mapx, self.mapy
		'''
	def collide(self, xvel, yvel):
		maps = self.world.get_open_maps()
		for m in maps:	
			for block in m.blocks.sprites():		
				if pygame.sprite.collide_rect(self, block):
					if xvel > 0:
						self.rect.right = block.rect.left
						print "collide right"
					if xvel < 0:
						self.rect.left = block.rect.right
						print "collide left"
					if yvel > 0:
						self.rect.bottom = block.rect.top
						print "collide bottom"
						if block.block == "ice-block" or block.block == "ice-two-block" or block.block == "oil-pocket-block":
							self.onGround = True
					if yvel < 0:
						print "collide top"
						self.rect.top = block.rect.bottom
