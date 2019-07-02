import pygame as pg

from src.entities.alert import Alert


class GameOverPrompt(Alert):

	def __init__(self, x, y, w, h, sprites, newColors, msgColor, msg):
		super().__init__(x, y, w, h, sprites, newColors, msgColor, msg)

	def render(self, surface, font):
		self.drawOutline()

		y = 8
		for m in self.msg:
			tempSurf = pg.Surface((self.w-16, 8)).convert()
			tempSurf.fill(self.msgColor)
			tempSurf.blit(font.render(m, self.msgColor, pg.Color("white")), (tempSurf.get_width()/2 - len(m)*4, 0))
			self.area.blit(tempSurf, (8, y))
			y += 8

		surface.blit(self.area, (self.x, self.y))

		