#! /usr/bin/python

import os, sys, random
import pygame
from pygame.locals import *
from load import *
from map import *
from block import *

class World:
	def __init__(self, width, height, mwidth, mheight):
		self.width = width
		self.height = height
		self.mwidth = mwidth
		self.mheight = mheight
		self.maps = []
		self.open_maps = []
		self.load = Load()
		self.ice_block, _ = self.load.image("ice-block.png", 0);
		self.ice_two_block, _ = self.load.image("ice-block.png", 0);
		self.oil_pocket_block, _  = self.load.image("oil-pocket-block.png", 0);
		self.blocks = [self.ice_block, self.ice_two_block, self.oil_pocket_block]
		print "World initialized"

	def load_maps(self, x, y):
		print "World loading maps"
		self.open_maps = []
		for m in self.maps:
			if (m.x == x and m.y == y)  or (m.x == x-1 and m.y == y-1) or (m.x == x-1 and m.y == y) or (m.x == x-1 and m.y == y+1) or (m.x == x and m.y == y-1) or (m.x == x and m.y == y+1) or (m.x == x+1 and m.y == y-1) or (m.x == x+1 and m.y == y) or (m.x == x+1 and m.y == y+1): 
				if m.generated == False:
					if x < self.surface:
						m.generate_atmosphere()
					elif x == self.surface:
						m.generate_surface()
					else:
						m.generate_beneath_surface()
				#print "Appending map", m.x, m.y
				self.open_maps.append(m)
						
	def get_open_maps(self):
		return self.open_maps

	def get_current_map(self, x, y):
		for m in self.open_maps:
			if m.x == x and m.y == y:
				return m
		return False

	def draw(self, screen):
		for m in self.open_maps:
			m.draw(screen)

	def generate_world(self, surfacePercent):
		print "World generation started"
		self.surface = self.width * float(surfacePercent / float(100))
		print "Surface", self.surface
		for x in range(0, self.width+1):
			for y in range(0, self.height+1):
				#print "Generating map for world location", x, ",", y
				if x < self.surface:
					#print "Generating atmosphere map"
					new_map = Map("Atmosphere", x, y, self.mwidth, self.mheight, self.blocks)
					self.maps.append(new_map)
				elif x == self.surface:
					#print "Generating surface map"
					new_map = Map("surface", x, y, self.mwidth, self.mheight, self.blocks)
					self.maps.append(new_map)
				elif x > self.surface:
					#print "Generating beneath the surface map"
					new_map = Map("beneath", x, y, self.mwidth, self.mheight, self.blocks)
					self.maps.append(new_map)
		print "World generation finished"
					
