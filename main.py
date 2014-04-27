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
		pygame.display.set_caption("Frozen Solid: Ludum Dare 49 competition 29")
		self.load = Load()
		self.state = "main_menu"
		self.running = True
		self.state_running = True
		self.timer = pygame.time.Clock()
	#	pygame.key.set_repeat(100,100)
		self.player = None
		self.exit_question = False
		
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
			if event.type == KEYDOWN and (event.key == K_ESCAPE or event.key == K_q) and self.state == "play":
				self.exit_question = True
			if event.type == KEYDOWN and event.key == K_n and self.state == "play" and self.exit_question == True:
				self.exit_question = False
			elif event.type == KEYDOWN and event.key == K_n and self.state == "ending":
				sys.exit()
			if event.type == KEYDOWN and event.key == K_y and self.state == "play" and self.exit_question == True:
				self.state_running = False
				self.state = "ending"
			elif event.type == KEYDOWN and event.key == K_y and self.state == "ending":
				self.state_running = False	
				self.exit_question = False
				self.state = "play"
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
			self.screen.fill((150,255,255))
			self.check_events()
			text = Text(None, 36)
			text.set_text("Welcome to play Frozen Solid.", 1, (0,0,0))
			text.set_position("center",(WIDTH/2, HEIGHT/2-(36*4)))
			text.draw(self.screen)
			text.set_text("Press RETURN to start the game.", 1, (0,0,0))
			text.set_position("center", (WIDTH/2, HEIGHT/2-(36*3)))
			text.draw(self.screen)
			text.set_text("Arrow keys to move the character.", 1, (0,0,0))
			text.set_position("center", (WIDTH/2, HEIGHT/2-(36*2)))
			text.draw(self.screen)
			text.set_text("A switches weapon.", 1, (0,0,0))
			text.set_position("center", (WIDTH/2, HEIGHT/2-36))
			text.draw(self.screen)
			text.set_text("S shoots.", 1, (0,0,0))
			text.set_position("center", (WIDTH/2, HEIGHT/2))
			text.draw(self.screen)
			text.set_text("SPACE jumps.", 1, (0,0,0))
			text.set_position("center", (WIDTH/2, HEIGHT/2+36))
			text.draw(self.screen)
			text.set_text("LSHIFT uses torch.", 1, (0,0,0))
			text.set_position("center", (WIDTH/2, HEIGHT/2+(36*2)))
			text.draw(self.screen)


			pygame.display.flip()

	def play(self):	
		world = World(9, 9, 20, 20)
		world.generate_world(10)
		entities = pygame.sprite.Group()
		self.player = Player("player", world, entities, 8, 8, 10, 10)
		world.load_maps(8,8)
		camera = Camera(complex_camera, 18*20*64, 18*20*64)
		while self.state_running == True:
			self.timer.tick(60)
			self.screen.fill((150,255,255))
			self.check_events()
			for m in world.get_open_maps():
				for block in m.blocks:
					entities.add(block)
			entities.add(self.player)
			#for bullet in self.player.bullets:
			#	entities.add(bullet)
			for e in entities:
				e.update()	
			camera.update(self.player, WIDTH, HEIGHT)			
			for e in entities:
				self.screen.blit(e.image, camera.apply(e))
			if self.exit_question == False:
				text = Text(None, 36)
				text.set_text("Jack:", 1, (0,0,0))
				text.set_position("topleft", (50,50))
				text.draw(self.screen)
				if self.player.weapon != None:
					text.set_text("Weapon: %s" % self.player.weapon, 1, (0,0,0))
					text.set_position("topleft", (50, 86))
					text.draw(self.screen)
					if self.player.weapon == "torch":
						text.set_text("Oil: %s" % self.player.oil_amount, 1, (0,0,0))
					if self.player.weapon == "pistol":
						text.set_text("Bullets: %s" % self.player.pistol_bullets, 1, (0,0,0))
					if self.player.weapon == "assault-rifle":
						text.set_text("Bullets: %s" % self.player.assault_rifle_bullets, 1, (0,0,0))
					text.set_position("topleft",(50, 122))
					text.draw(self.screen)
			else:
				text = Text(None, 36)
				text.set_text("Are you sure you want to quit? Y/N", 1, (0,0,0))
				text.set_position("center", (WIDTH/2,HEIGHT/2))
				text.draw(self.screen)
			pygame.display.flip()
			if self.player.game_complete == True:
				self.state = "ending"
				self.state_running == False
			entities = pygame.sprite.Group()
	def ending(self):
		while self.state_running == True:
			self.timer.tick(60)
			self.check_events()
			self.screen.fill((150, 255, 255))
			text = Text(None, 36)
			if self.player.game_complete == True:
				text.set_text("Congratulations you have successfully completed the game. Do you want to replay ? Y/N", 1, (0,0,0))
			else:
				text.set_text("The game has ended. Do you want to replay? Y/N", 1, (0,0,0))

			text.set_position("center", (WIDTH/2,HEIGHT/2))
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
		elif game.state == "ending":
			print "Started ending"
			game.ending()
		game.state_running = True
