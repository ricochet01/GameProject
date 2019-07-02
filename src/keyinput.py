import pygame as pg
from pygame.locals import *


class KeyInput:

	def __init__(self):
		pg.key.set_repeat(500, 50)

		self.releaseAll()
		self.keys = pg.key.get_pressed()

		self.upKeys = [K_UP, K_w, K_KP8]
		self.downKeys = [K_DOWN, K_s, K_KP2]
		self.leftKeys = [K_LEFT, K_a, K_KP4]
		self.rightKeys = [K_RIGHT, K_d, K_KP6]

	def hasFocus(self):
		return pg.key.get_focused()

	def releaseAll(self):
		self.left = False
		self.right = False
		self.up = False
		self.down = False
		self.use = False
		self.back = False

	def tick(self):
		self.keys = pg.key.get_pressed()

		self.use = True if self.keys[K_RETURN] else False
		self.left = True if self.keys[K_LEFT] or self.keys[K_a] or self.keys[K_KP4] else False
		self.right = True if self.keys[K_RIGHT] or self.keys[K_d] or self.keys[K_KP6] else False
		self.up = True if self.keys[K_UP] or self.keys[K_w] or self.keys[K_KP8] else False
		self.down = True if self.keys[K_DOWN] or self.keys[K_s] or self.keys[K_KP2] else False
		self.back = True if self.keys[K_ESCAPE] else False





