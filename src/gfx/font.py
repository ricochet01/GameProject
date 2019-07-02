import pygame as pg
from pygame.locals import *


class Font:

	def __init__(self, sheet):
		self.chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZ[]|@_ " + \
					"0123456789.,!?'\"-+=/\\%()<>:;&*{}"
		self.charArray = {}

		self.legalChars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz!\"%&/()=?*'+0123456789[]{}@|\\.,;:-_<> "

		y = 30
		x = 0
		for i in range(len(self.chars)):
			if x == 32:
				x = 0
				y += 1

			self.charArray[self.chars[i]] = sheet.get(x, y, 8, 8, pg.Color("black"))
			x += 1

	def render(self, msg, bgColor=None, letterColor=None):
		msg = msg.upper()
		surf_width = len(msg) << 3
		surf_height = 8

		if bgColor == pg.Color("white"):
			raise ValueError("Argument background color cannot be full white! Use 1 bit down on any color channel!")

		if bgColor == None:
			area = pg.Surface((surf_width, surf_height), DOUBLEBUF | HWSURFACE | SRCALPHA, 32).convert_alpha()
		else:
			area = pg.Surface((surf_width, surf_height), DOUBLEBUF | HWSURFACE).convert()
			area.fill(bgColor)

		for c in range(len(msg)):
			area.blit(self.charArray[msg[c]], (c << 3, 0))

		if letterColor != None:
			image_pixelarray = pg.PixelArray(area)
			image_pixelarray.replace(pg.Color("white"), letterColor)
			image_pixelarray.close()

		return area

