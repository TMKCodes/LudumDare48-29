#! /usr/bin/python

import os, sys
import pygame
from pygame.locals import *


class Text:
	def __init__(filename, size):
		if pygame.font:
			self.font = pygame.font.Font(None, 36)
	def set_text(text, antialias, color, background):
		self.text = self.font.render(text, antialias, color, background)
	
	def set_position(height, width):
		self.position = text.get_rect(centerx = (height, width))
	
	def draw(screen):
		 screen.blit(self.text, self.position)
