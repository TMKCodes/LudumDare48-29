#! /usr/bin/python

import os, sys
import pygame
from pygame.locals import *


class Text:
	def __init__(self, filename, size):
		if pygame.font:
			self.font = pygame.font.Font(None, 36)
	def set_text(self, text, antialias, color, background=None):
		if background == None:
			self.text = self.font.render(text, antialias, color)
		else:
			self.text = self.font.render(text, antialias, color, background)
	
	def set_position(self, height, width):
		self.position = self.text.get_rect(topleft = (height, width))
	
	def draw(self, screen):
		 screen.blit(self.text, self.position)
