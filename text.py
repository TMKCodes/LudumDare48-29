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
	
	def set_position(self, type, pos):
		if type == "topleft":
			self.position = self.text.get_rect(topleft = pos)
		elif type == "center":
			self.position = self.text.get_rect(center = pos)
	
	def draw(self, screen):
		 screen.blit(self.text, self.position)
