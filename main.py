#! /usr/bin/python

import os, sys
import pygame
from pygame.locals import *
from load import *
from camera import *
from entity import *
from player import *
from text import *
from world import *

if not pygame.font: print 'Warning, fonts disabled'
if not pygame.mixer: print 'Warning, sounds disabled'

WIDTH = 1024
HEIGHT = 920

class Engine:
	def __init__(self, width, height):
		self.screen_width = width
		self.screen_height = height
		pygame.init()
		self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
		pygame.display.set_caption("LudumDare 49 compo 29")
		self.load = Load()
		self.state = "main_menu"
		self.running = True
		self.state_running = True
		self.timer = pygame.time.Clock()
		self.bg = pygame.Surface((64,64)).convert()
		self.bg.fill(pygame.Color("#000000"))
		pygame.key.set_repeat(10,10)

	def draw_bg(self):
		for y in range(64):
			for x in range(64):
				self.screen.blit(self.bg, (x * 64, y *64))		

	def check_events(self):
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == KEYDOWN and event.key == K_RETURN and self.state == "main_menu":
				self.state = "play"
				self.state_running = False
			if event.type == KEYDOWN and event.key == K_UP and self.state == "play":
				self.player.update("up")
			if event.type == KEYDOWN and event.key == K_DOWN and self.state == "play":
				self.player.update("down")
			if event.type == KEYDOWN and event.key == K_SPACE and self.state == "play":
				self.player.update("running")
			if event.type == KEYDOWN and event.key == K_LEFT and self.state == "play":
				self.player.update("left")
			if event.type == KEYDOWN and event.key == K_RIGHT and self.state == "play":
				self.player.update("right")
			if event.type == KEYUP and self.state == "play":
				self.player.update("pause")

	def main_menu(self):
		while self.state_running == True:
			self.timer.tick(60)
			self.check_events()

	def play(self):	
		world = World(18, 18)
		world.generate_world(10, 20,20)
		self.player = Player("player", world, 9, 16, 10, 10)
		world.load_maps(9,16)
		entities = pygame.sprite.Group()
		camera = Camera(complex_camera, 18*20*64, 18*20*64)
		while self.state_running == True:
			self.timer.tick(60)
			self.check_events()
			self.player.update()
			self.draw_bg()
			for m in world.get_open_maps():
				for block in m.blocks:
					entities.add(block)
			entities.add(self.player)
			camera.update(self.player, WIDTH, HEIGHT)
			for e in entities:
				self.screen.blit(e.image, camera.apply(e))
			pygame.display.update()
			


if __name__ == "__main__":
	game = Engine(WIDTH, HEIGHT)
	while game.running == True:
		print game.state
		print game.state_running
		if game.state == "main_menu":
			print "Started main menu"
			game.main_menu()
		elif game.state == "play":
			print "Started play"
			game.play()
		game.state_running = True
