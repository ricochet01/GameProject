import pygame as pg
from pygame.locals import *

import sys


pg.mixer.pre_init(44100, -16, 2, 512)
pg.init()


class Const:
	def getFileContent():
		try:
			with open("cfg/config.dat", "r") as f:
				l = [line.rstrip() for line in f]
		except FileNotFoundError as e:
			with open("cfg/config.dat", "w") as f:
				l = ["6456", "035e", "004d", "0043"]
				for item in l:
					f.write(item + "\n")
		finally:
			return l

	@classmethod
	def replaceConfig(cls, old, new):
		items = cls.content

		cls.content[old] = new
		try:
			with open("cfg/config.dat", "w") as f:
				for item in cls.content:
					f.write(str(item) + "\n")
		except IOError as e:
			print(e)


	content = getFileContent()

	WIDTH = 160
	HEIGHT = 120
	SCALE = (int(content[1], 16) >> 8)
	TITLE = "Untitled"

	if not isinstance(SCALE, int):
		raise ValueError("Scale must be an integer!")

	WINDOW_SIZE = (WIDTH * SCALE, HEIGHT * SCALE)

	fullscreen = (int(content[2], 16) >> 8)
	if fullscreen:
		flags = FULLSCREEN | DOUBLEBUF | HWSURFACE
	else:
		flags = HWSURFACE | DOUBLEBUF
		
	win = pg.display.set_mode(WINDOW_SIZE, flags)
	pg.display.set_caption(TITLE)

	icon = pg.image.load("res/icon.ico")
	pg.display.set_icon(icon)

	volume = (int(content[0], 16) >> 8)

	playerColor = (int(content[3], 16) >> 8)

	gameType = "Singleplayer"

	inversion = int(content[4], 16)
	crtEffect = int(content[5], 16)
	redChannel = int(content[6], 16)
	blueChannel = int(content[7], 16)
	filters = int(content[8], 16)



def stop():
	pg.quit()
	sys.exit()
	

clock = pg.time.Clock()
fps = 60
