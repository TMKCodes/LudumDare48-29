#! /usr/bin/python

import os, sys, random
import pygame
from pygame.locals import *
from block import *

class Map(object):
	def __init__(self, surface, x, y, width, height):
		self.surface = surface
		self.x = x
		self.y = y
		self.width = width
		self.height = height
		self.blocks = pygame.sprite.Group()
		self.generated = False
		print "Map initialized", self.x, self.y

	def draw(self, screen):
		self.blocks.draw(screen)

	def get_width(self):
		return self.width*64

	def get_height(self):
		return self.height*64

	def get_block_top(self, x, y):
		for block in self.blocks.sprites():
			if block.rect.x == x and block.rect.y == y-64:
				return block
		return False

	def get_block_bottom(self, x, y):
		for block in self.blocks.sprites():
			if block.rect.x == x and block.rect.y == y+64:
				return block
		return False

	def get_block_left(self, x, y):
		for block in self.blocks.sprites():
			if block.rect.x == x-64 and block.rect.y == y:
				return block
		return False

	def get_block_right(self, x, y):
		for block in self.blocks.sprites():
			if block.rect.x == x+64 and block.rect.y == y:
				return block;
		return False

	def get_blocks(self):
		return self.blocks

	def generate_atmosphere(self):
		self.generated = True

	def generate_surface(self):
		for x in range(0, self.width):
			for y in range(self.height/2, self.height):
				self.generate_block(x, y)
		self.generated = True

	def generate_beneath_surface(self):
		for x in range(0, self.width):
			for y in range(0, self.height):
				self.generate_block(x, y)
		self.generated = True

	def generate_block(self, x, y):
		#print "Generate block", self.x*self.width*64+x*64, self.y*self.height*64+y*64	
		ice = random.randint(0, 4)
		if ice == 1:
			self.blocks.add(Block("ice-block", self.x*self.width*64+x*64, self.y*self.height*64+y*64))
		elif ice == 2:
			self.blocks.add(Block("ice-two-block", self.x*self.width*64+x*64, self.y*self.height*64+y*64))
		elif ice == 3:
			close_block = "diff"
			for block in self.blocks.sprites():
				if block.rect.y == self.height*(y-1):
					if block.block != "ice-block" and block.block != "ice-two-block":
						close_block == "same"
				if block.rect.x == self.width*(x-1):
					if block.block != "ice-block" and block.block != "ice-two-block":
						close_block == "same"		
			if close_block == "same":
				odd_ice = random.randint(0, 10)
				if odd_ice <= 4:
					if odd_ice > 0 and odd_ice <= 2:
						self.blocks.add(Block("ice-block", self.x*self.width*64+x*64, self.y*self.height*64+y*64))
					else:
						self.blocks.add(Block("ice-two-block", self.x*self.width*64+x*64, self.y*self.height*64+y*64))
				else:
					self.blocks.add(Block("oil-pocket-block", self.x*self.width*64+x*64, self.y*self.height*64+y*64))
			else: 
				odd_ice = random.randint(0, 10)
				if odd_ice <= 8:
					if odd_ice > 0 and odd_ice <= 4:
						self.blocks.add(Block("ice-block", self.x*self.width*64+x*64, self.y*self.height*64+y*64))
					else:
						self.blocks.add(Block("ice-two-block", self.x*self.width*64+x*64, self.y*self.height*64+y*64))
				else:
					self.blocks.add(Block("oil-pocket-block", self.x*self.width*64+x*64, self.y*self.height*64+y*64))
								
