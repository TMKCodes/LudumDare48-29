#! /usr/bin/python

import pygame
from pygame.locals import *
from entity import *
from load import *

class Block(Entity):
	def __init__(self, block, x, y):
		Entity.__init__(self)
		self.load = Load()
		self.block = block
		self.image, _ = self.load.image("%s.png" % block, 0)
		print "Block initiatet at",x, y
		self.rect = pygame.Rect(x, y, 64, 64)

	def update(self):
		pass

