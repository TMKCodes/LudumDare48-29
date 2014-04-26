#! /usr/bin/python

import pygame
from pygame.locals import *

class Camera(object):
	def __init__(self, camera_func, width, height):
		self.camera_func = camera_func
		self.state = Rect(0,0, width, height)
	
	def apply(self, target):
		return target.rect.move(self.state.topleft)
	
	def update(self, target):
		self.state = self.camera_func(self.state, target.rect)

def simple_camera(camera, target_rect, height, width):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	return Rect(-l+width/2, -t+height/2, w, h)

def complex_camera(camera, target_rect, height, width):
	l, t, _, _ = target_rect
	_, _, w, h = camera
	l, t, _, _ = -l+width/2, -t+height/2, w, h
	l = min(0, l)
	l = max(-(camera.width-width), l)
	l = max(-(camrea.height-height), t)
	l = min(0, t)
	return Rect(l, t, w, h)

