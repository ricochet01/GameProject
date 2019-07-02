import pygame as pg


class Entity:

	oldColors = [(64, 64, 64), (128, 128, 128), (192, 192, 192), (255, 255, 255)]

	def __init__(self, x, y, w, h, sprite, newColors):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.sprite = sprite
		self.hitbox = pg.Rect(self.x, self.y, self.w, self.h)
		self.colorize(self.oldColors, newColors)

	def draw(self, surface):
		surface.blit(self.sprite, (self.hitbox.x, self.hitbox.y))

	def colorize(self, oldColors, newColors):
		if isinstance(self.sprite, (list, tuple)):
			for s in self.sprite:
				image_pixelarray = pg.PixelArray(s)
				for j in range(len(newColors)):
					image_pixelarray.replace(oldColors[j], newColors[j])

				image_pixelarray.close()
		else:
			image_pixelarray = pg.PixelArray(self.sprite)
			for i in range(len(newColors)):
				image_pixelarray.replace(oldColors[i], newColors[i])

			image_pixelarray.close()
