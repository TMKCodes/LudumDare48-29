#! /usr/bin/python

import pygame
from pygame.locals import *
from entity import *
from load import *

class Bullet(Entity):
	def __init__(self, world, entities, mapx, mapy, x, y, direction):
		Entity.__init__(self)
		self.load = Load()
		self.mapx = mapx
		self.mapy = mapy
		self.world = world
		self.entities = entities
		self.xvel = 0
		self.yvel = 0
		self.direction = direction
		self.rect = pygame.Rect(mapx*self.world.mwidth*64+(x*64), mapy*self.world.mheight*64+(y*64), 64, 64)
		self.load_image("bullet-%s.png" % direction);
		self.type = "bullet"
		self.player = False
	
	def load_image(self, name):
		self.image, _ = self.load.image(name, -1)
	
	def update(self):
		if self.direction == "left":
			self.xvel += 15
		elif self.direction == "right":
			self.yvel -= 15
		
		self.rect.left += self.xvel
		self.collide(self.xvel, 0)
	
	def end_animation(self):
		pass

	def collide(self, xvel, yvel):
		for entity in self.entities.sprites():
			if pygame.sprite.collide_rect(self, block):
				if xvel > 0:
					self.rect.right = entity.rect.left
					self.end_animation()
				if xvel < 0:
					self.rect.left = entity.rect.right
					self.end_animation()
				if entity.type == "alive" and entity.player != True:
					entity.kill();	

