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
		pygame.key.set_repeat(10,100)
		self.player = None
		
	def check_events(self):
		up, down, running, left, right, melt, pause, weapon, shoot = False, False, False, False, False, False, False, False, False
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
			if event.type == KEYDOWN and event.key == K_RETURN and self.state == "main_menu":
				self.state = "play"
				self.state_running = False
				return 
			if event.type == KEYUP and self.state == "play":
				pause = True
			if event.type == KEYDOWN and event.key == K_a and self.state == "play":
				weapon = True
		keys = pygame.key.get_pressed()
		if self.state == "play":
			if keys[K_UP]:
				up = True
			if keys[K_DOWN]:
				down = True
			if keys[K_SPACE]:
				running = True
			if keys[K_LEFT]:
				left = True
			if keys[K_RIGHT]:
				right = True
			if keys[K_LSHIFT]:	
				melt = True
			if keys[K_s]:
				shoot = True

			self.player.update(up, running, down, left, right, melt, pause, weapon, shoot)

	def main_menu(self):
		while self.state_running == True:
			self.timer.tick(60)
			self.check_events()

	def play(self):	
		world = World(18, 18, 20, 20)
		world.generate_world(10)
		self.player = Player("player", world, 9, 16, 10, 10)
		world.load_maps(9,16)
		entities = pygame.sprite.Group()
		camera = Camera(complex_camera, 18*20*64, 18*20*64)
		while self.state_running == True:
			self.timer.tick(60)
			self.screen.fill((150,255,255))
			self.check_events()
			self.player.update()
			for m in world.get_open_maps():
				for block in m.blocks:
					entities.add(block)
			entities.add(self.player)
			camera.update(self.player, WIDTH, HEIGHT)			
			for e in entities:
				self.screen.blit(e.image, camera.apply(e))
			text = Text(None, 36)
			text.set_text("Jack:", 1, (255,255,255))
			text.set_position(50,50)
			text.draw(self.screen)
			if self.player.weapon != None:
				text.set_text("Weapon: %s" % self.player.weapon, 1, (255,255,255))
				text.set_position(50, 86)
				text.draw(self.screen)
				if self.player.weapon == "torch":
					text.set_text("Oil: %s" % self.player.oil_amount, 1, (255, 255, 255))
				if self.player.weapon == "pistol":
					text.set_text("Bullets: %s" % self.player.pistol_bullets, 1, (255,255,255))
				if self.player.weapon == "assault-rifle":
					text.set_text("Bullets: %s" % self.player.assault_rifle_bullets, 1, (255, 255, 255))
				text.set_position(50, 122)
				text.draw(self.screen)
			pygame.display.flip()
			


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
