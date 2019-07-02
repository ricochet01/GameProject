import pygame as pg
from pygame.locals import *


class SpriteSheet:

	def __init__(self, path):
		self.sheet = pg.image.load(path)

	def get(self, xTile, yTile, w, h, clrkey=None, xFlip=False, yFlip=False):
		imgRect = pg.Rect(xTile << 3, yTile << 3, w, h)
		img = pg.Surface(imgRect.size, HWSURFACE | DOUBLEBUF).convert()
		img.blit(self.sheet, (0, 0), imgRect)

		if clrkey != None:
			img.set_colorkey(clrkey, RLEACCEL)

		if xFlip != 0 or yFlip != 0:
			img = pg.transform.flip(img, xFlip, yFlip)

		return img


