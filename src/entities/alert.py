import pygame as pg
from pygame.locals import *

from src.entities.entity import Entity


class Alert(Entity):

	oldColors = [(64, 64, 64), (128, 128, 128), (255, 255, 255)]

	def __init__(self, x, y, w, h, sprites, newColors, msgColor, msg):
		super().__init__(x, y, w, h, sprites, newColors)
		self.sprites = sprites
		self.msgColor = msgColor
		self.msg = msg

		self.area = pg.Surface((self.w, self.h), HWSURFACE | DOUBLEBUF).convert()
		self.area.set_colorkey(pg.Color("black"))
		self.ticks = 0

	def tick(self):
		if not self.ticks > 60:
			self.ticks += 1
		else:
			self.ticks = 0

	def drawOutline(self):
		self.area.blit(self.sprites[0], (0, 0))
		self.area.blit(pg.transform.flip(self.sprites[0], True, False), (self.area.get_width()-8, 0))
		self.area.blit(pg.transform.flip(self.sprites[0], False, True), (0, self.area.get_height()-8))
		self.area.blit(pg.transform.flip(self.sprites[0], True, True), (self.area.get_width()-8, self.area.get_height()-8))

		for xu in range(8, self.area.get_width()-8, 8):
			self.area.blit(self.sprites[1], (xu, 0))
		for xd in range(8, self.area.get_width()-8, 8):
			self.area.blit(pg.transform.flip(self.sprites[1], False, True), (xd, self.area.get_height()-8))

		for yl in range(8, self.area.get_height()-8, 8):
			self.area.blit(pg.transform.rotate(self.sprites[1], 90), (0, yl))
		for yr in range(8, self.area.get_height()-8, 8):
			self.area.blit(pg.transform.rotate(self.sprites[1], 270), (self.area.get_width()-8, yr))

	def render(self, surface, font):
		self.drawOutline()

		self.alert_text = font.render(self.msg, self.msgColor, pg.Color("white") if self.ticks < 30 else pg.Color("dimgray"))
		self.area.blit(self.alert_text, (8, 8))

		surface.blit(self.area, (self.x, self.y))
