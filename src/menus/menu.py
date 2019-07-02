import pygame as pg
from pygame.locals import *

import datetime
import random
import numpy as np

from src.constants import *
from src.keyinput import KeyInput
from src.entities.alert import Alert
from src.gfx.font import Font
from src.gfx.spritesheet import SpriteSheet
from src.level.level import Level
from src.entities.mob import Mob
from src.level.tiles.tile import Tile
from src.level.tiles.flowertile import FlowerTile


class Menu:

	layout = Level.levelToArray("res/bg")
	tiles = []

	flowerObjects = []
	flowerColors = ["red", "yellow", "green"]

	sheet = SpriteSheet("res/sheet.png")

	i = 0
	for y, layer in enumerate(layout):
		for x, t in enumerate(layer):
			if t == "1":
				tiles.append(Tile(x << 3, y << 3, 8, 8, sheet.get(random.randint(0, 3), 0, 8, 8, pg.Color("black")),
					[pg.Color(49, 127, 52), pg.Color("green")], "grass", False, i))
			elif t == "2":
				flower = FlowerTile(x << 3, y << 3, 8, 8, sheet.get(4, 0, 8, 8),
					[pg.Color(49, 127, 52), pg.Color(0, 112, 0), pg.Color("red"), pg.Color(200, 200, 200)],
					"flower", False, i, random.choice(flowerColors), "Easy")
				tiles.append(flower)
				flowerObjects.append(flower)
			elif t == "3":
				tiles.append(Tile(x << 3, y << 3, 8, 8, sheet.get(random.randint(0, 3), 0, 8, 8, pg.Color("black")),
					[pg.Color(85, 0, 0), pg.Color("gray")], "dirt", False, i))
			
			i += 1

	def __init__(self):
		self.display = pg.Surface((Const.WIDTH, Const.HEIGHT), HWSURFACE | DOUBLEBUF).convert()

		self.bottomSurf = pg.Surface((Const.WIDTH, Const.HEIGHT), HWSURFACE | DOUBLEBUF)

		self.overlay = pg.Surface((Const.WIDTH, Const.HEIGHT), HWSURFACE | SRCALPHA, 32).convert()
		self.overlay.set_alpha(128)

		self.counter = 0
		self.interactive = True
		self.interactiveMenus = [
								"Main menu",
								"High scores",
								"Options",
								"Paused",
								"Are you sure?",
								"Game configuration",
								"Select one",
								"Advanced"]

		self.items = []

		self.currentMenu = "Main menu"
		
		self.input = KeyInput()
		self.font = Font(self.sheet)

		self.setup()

	def soundSetup(self):
		self.scroll = pg.mixer.Sound("res/scroll.wav")
		self.select = pg.mixer.Sound("res/select.wav")
		self.goBack = pg.mixer.Sound("res/goback.wav")
		self.sfx = [self.scroll, self.select, self.goBack]
		for sound in self.sfx:
			sound.set_volume(Const.volume/100)

	def setup(self):
		self.guiSetup()
		self.soundSetup()

		self.p = Mob(-10, -10, 16, 16, pg.Surface((16, 16)), pg.Color("gray"))

		self.scanlines = pg.Surface((160, 120), DOUBLEBUF | HWSURFACE | SRCALPHA, 32).convert_alpha()
		for y in range(0, 160, 2):
			line = pg.Surface((160, 1), DOUBLEBUF | HWSURFACE | SRCALPHA, 32).convert_alpha()
			line.fill(pg.Color(0, 0, 0))
			self.scanlines.blit(line, (0, y))

	def guiSetup(self):
		alertMsg = "Click to play!"
		alertWidth = (16 + len(alertMsg) * 8)
		alertColor = pg.Color("darkred")
		self.alert = Alert(self.display.get_width()/2 - alertWidth/2, self.display.get_height()/2 - 12, 16 + len(alertMsg)*8, 24,
							[self.sheet.get(0, 1, 8, 8, pg.Color("black")).copy(), self.sheet.get(1, 1, 8, 8, pg.Color("black")).copy()],
							[(64, 64, 64), (128, 128, 128), alertColor], alertColor, alertMsg)

	def start(self):
		self.running = True

	def update(self):
		clock.tick(fps)
		self.alert.tick()

		# self.display.fill(pg.Color("black"))
		Level.render(self.bottomSurf, self.tiles, Const.WIDTH, Const.HEIGHT, 0, 0, self.p, self.sheet, 0)

	def takeScreenshot(self):
		screenshot = pg.transform.scale(pg.surfarray.make_surface(self.pixels).copy(), Const.WINDOW_SIZE)
		current = datetime.datetime.now()
		imgname = "screenshot-" + current.strftime("%d-%m-%Y-%H-%M-%S") + ".png"
		scrnsht_file = pg.image.save(screenshot, "screenshots/" + imgname)

	# Override this method to add things to the menu
	def menuUpdate(self):
		pass

	def eventHandler(self):
		for event in pg.event.get():
			if event.type == QUIT:
				stop()

			if event.type == KEYDOWN:
				if event.key == K_F12:
					self.takeScreenshot()					

				if event.key in self.input.upKeys and self.currentMenu in self.interactiveMenus:
					self.counter -= 1
					if self.counter == -1:
						self.counter = len(self.items) - 1
					self.scroll.play()

				if event.key in self.input.downKeys and self.currentMenu in self.interactiveMenus:
					self.counter += 1
					if self.counter == len(self.items):
						self.counter = 0
					self.scroll.play()

				if event.key == K_RETURN and self.currentMenu == "Main menu":
					self.select.play()

				if event.key == K_ESCAPE and self.currentMenu != "Main menu":
					self.running = False
					self.goBack.play()

	def renderAlert(self):
		if not self.input.hasFocus():
			self.input.releaseAll()
			self.alert.render(self.display, self.font)

	def render(self):
		self.renderAlert()

		if Const.crtEffect and Const.filters:
			self.scanlines.set_alpha(64)
			self.display.blit(self.scanlines, (0, 0))

		self.overlay.set_alpha(192)

		self.filter = pg.surfarray.array3d(self.display)
		self.pixels = np.array(self.filter)

		if Const.filters:
			if Const.redChannel:
				self.pixels[:,:,1:] = Const.redChannel
			if Const.blueChannel:
				self.pixels[:,:,2:] = Const.blueChannel
			if Const.inversion:
				self.pixels ^= Const.inversion

		Const.win.blit(pg.transform.scale(pg.surfarray.make_surface(self.pixels), Const.WINDOW_SIZE), (0, 0))

		self.display.blit(self.bottomSurf, (0, 0))
		self.display.blit(self.overlay, (0, 0))

		pg.display.flip()

	def main(self):
		self.start()
		while self.running:
			self.update()

			self.eventHandler()
			self.menuUpdate()

			self.render()

