import pygame as pg
from pygame.locals import *

import random


class Level:

	@staticmethod
	def levelToArray(path):
		level = []
		levelAlt = []
		with open(path + ".txt", "r") as f:
			layout = f.read()

		layout = layout.splitlines()
		for layer in layout:
			levelAlt.append(layer)

		for layer in levelAlt:
			newLayer = []
			for tile in layer:
				newLayer.append(tile)
			level.append(newLayer)

		return level

	@staticmethod
	def generateLevel(w, h, density):
		level = []
		grassOdds = 1.0 - density

		for y in range(h):
			layer = []
			for x in range(w):
				layer.append(str(random.choices(population=["1", "2"], weights=[grassOdds, density]))[2])	# For some reason, I have to turn it into a string,
			level.append(layer)																			# Since it returns a one item array as a string...

		return level

	@staticmethod
	def render(surface, tiles, w, h, xOffset, yOffset, player, sheet, score):
		tileRects = []
		for tile in tiles:
			if tile.type == "flower":
				tiles, score = tile.draw(surface, xOffset, yOffset, player, tiles, sheet, score)
				continue
			if (tile.x - 8) <= xOffset + (w - 4) and (tile.x + 8) >= xOffset:
				if (tile.y - 8) <= yOffset + (h - 4) and (tile.y + 8) >= yOffset:
					if tile.type != "flower":
						tile.draw(surface, xOffset, yOffset)
					if tile.solid:
						tileRects.append(tile.hitbox)
							
		return tiles, score, tileRects
		