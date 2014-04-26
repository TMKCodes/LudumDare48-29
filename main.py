#! /usr/bin/python

import os, sys
import pygame
from pygame.locals import *
from load import *
from camera import *
from entity import *
from player import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sounds disabled'

WIDTH = 640
HEIGHT = 480

class Engine:
	def __init__(self, width, height):
		self.width = width
		self.height = height
		pygame.init()
		self.screen = pygame.display.set_mode((self.width, self.height))
		self.load = Load()

if __name__ == "__main__":
	game = Engine(WIDTH, WIDTH)

