#! /usr/bin/python

import pygame
from pygame.locals import *
from entity import *
from load import *

class Player(Entity):
	def __init__(self, x, y):
		Entity.__init(self)
		self.load = Load()

	def load_image(name):
		self.image, self.rect = self.load.image(name, -1)
	
	def load_sound(name):
		return self.load.sound(name)		
