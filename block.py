#! /usr/bin/python

import pygame
from pygame.locals import *
from entity import *
from load import *

class Block(Entity):
	def __init__(self, block, x, y, image):
		Entity.__init__(self)
		self.load = Load()
		self.block = block
		self.image = image
		#self.image, _ = self.load.image("%s.png" % block, 0)
		self.rect = pygame.Rect(x, y, 64, 64)
		self.type = "block"
		self.player = False

	def update(self):
		pass

