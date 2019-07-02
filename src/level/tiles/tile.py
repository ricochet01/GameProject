import pygame as pg

from src.entities.entity import Entity


class Tile(Entity):

	def __init__(self, x, y, w, h, sprite, newColors, type, solid, id):
		super().__init__(x, y, w, h, sprite, newColors)
		self.type = type
		self.solid = solid
		self.id = id

	def draw(self, surface, xo, yo):
		surface.blit(self.sprite, (self.hitbox.x - xo, self.hitbox.y - yo))

