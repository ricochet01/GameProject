import pygame as pg
from pygame.locals import *

from src.menus.menu import Menu
from src.menus.advancedmenu import AdvancedOptionsMenu
from src.constants import Const, stop


class OptionsMenu(Menu):

	def __init__(self):
		super().__init__()
		self.currentMenu = "Options"
		self.center = self.display.get_width() / 2 - len(self.currentMenu) * 4

		self.resSelected = Const.SCALE - 3

		self.resolutions = ["480x360", "640x480", "800x600", "960x720",
							"1120x840", "1280x960", "1440x1080"]

		self.playerColors = [pg.Color("red"), pg.Color("blue"), pg.Color("green"),
							pg.Color("magenta"), pg.Color("orangered"), pg.Color("white"),
							pg.Color("orange"), pg.Color("yellow"), pg.Color("purple"),
							pg.Color("darkred"), pg.Color("gray")]
		
		self.items = ["Audio:" + str(int(Const.volume)) + "%",
					"Window:%s" % self.resolutions[self.resSelected],
					"Fullscreen:ON" if Const.fullscreen else "Fullscreen:OFF",
					"Player color: ",
					"Advanced",
					"Apply"]

	def eventHandler(self):
		for event in pg.event.get():
			if event.type == QUIT:
				stop()

			if event.type == KEYDOWN:
				if event.key == K_F12:
					self.takeScreenshot()

				if event.key in self.input.upKeys:
					self.counter -= 1
					if self.counter == -1:
						self.counter = len(self.items) - 1
					self.scroll.play()

				if event.key in self.input.downKeys:
					self.counter += 1
					if self.counter == len(self.items):
						self.counter = 0
					self.scroll.play()

				if event.key in self.input.leftKeys:
					if self.counter == 0:
						if Const.volume >= 1:
							Const.volume -= 1
							self.scroll.play()
						self.items[0] = "Audio:" + str(int(Const.volume)) + "%"

						self.soundSetup()
						Const.replaceConfig(0, "{:04x}".format((Const.volume<<8)+86))

					elif self.counter == 1:
						self.resSelected -= 1
						if self.resSelected == -1:
							self.resSelected = len(self.resolutions) - 1
						self.items[1] = "Window:%s" % self.resolutions[self.resSelected]
						self.scroll.play()

					elif self.counter == 2:
						Const.fullscreen = not Const.fullscreen
						self.items[2] = "Fullscreen:ON" if Const.fullscreen else "Fullscreen:OFF"
						self.scroll.play()

					elif self.counter == 3:
						Const.playerColor -= 1
						if Const.playerColor == -1:
							Const.playerColor = len(self.playerColors) - 1
						Const.replaceConfig(3, "{:04x}".format((Const.playerColor<<8)+67))
						self.scroll.play()

				if event.key in self.input.rightKeys:
					if self.counter == 0:
						if Const.volume <= 99:
							Const.volume += 1
							self.scroll.play()
						self.items[0] = "Audio:" + str(int(Const.volume)) + "%"

						self.soundSetup()
						Const.replaceConfig(0, "{:04x}".format((Const.volume<<8)+86))


					elif self.counter == 1:
						self.resSelected += 1
						if self.resSelected == len(self.resolutions):
							self.resSelected = 0
						self.items[1] = "Window:%s" % self.resolutions[self.resSelected]
						self.scroll.play()

					elif self.counter == 2:
						Const.fullscreen = not Const.fullscreen
						self.items[2] = "Fullscreen:ON" if Const.fullscreen else "Fullscreen:OFF"
						self.scroll.play()

					elif self.counter == 3:
						Const.playerColor += 1
						if Const.playerColor == len(self.playerColors):
							Const.playerColor = 0
						Const.replaceConfig(3, "{:04x}".format((Const.playerColor<<8)+67))
						self.scroll.play()

					# elif self.counter == 4:
					# 	Const.inversion = (Const.inversion + 1) & 0xff
					# 	self.items[4] = "Inversion: %d" % Const.inversion
					# 	Const.replaceConfig(4, "{:04x}".format(Const.inversion))

				if event.key == K_ESCAPE:
					self.running = False
					self.goBack.play()

				if event.key == K_RETURN and self.counter == 4:
					self.select.play()
					advancedScreen = AdvancedOptionsMenu()
					advancedScreen.main()

				if event.key == K_RETURN and self.counter == len(self.items) - 1:
					Const.SCALE = self.resSelected + 3
					Const.WINDOW_SIZE = (Const.WIDTH * Const.SCALE, Const.HEIGHT * Const.SCALE)
					if Const.fullscreen:
						Const.win = pg.display.set_mode(Const.WINDOW_SIZE, FULLSCREEN | DOUBLEBUF | HWSURFACE)
					else:
						Const.win = pg.display.set_mode(Const.WINDOW_SIZE, DOUBLEBUF | HWSURFACE)

					Const.replaceConfig(2, "{:04x}".format((Const.fullscreen<<8)+77))
					Const.replaceConfig(1, "{:04x}".format(((self.resSelected + 3)<<8)+94))


					self.select.play()

	def menuUpdate(self):
		self.display.blit(self.font.render(self.currentMenu, None, pg.Color("white")), (self.center, 4))

		y = 32
		for i in range(len(self.items)):
			if i == self.counter:
				self.display.blit(self.font.render("> " + self.items[i] + " <", None, pg.Color("yellow")),
					(self.display.get_width() / 2 - len(self.items[i]*8) / 2 - 16, y))
			else:
				self.display.blit(self.font.render(self.items[i], None, pg.Color("gray")), (self.display.get_width() / 2 - len(self.items[i]*8) / 2, y))
			y += 8

		pg.draw.rect(self.display, self.playerColors[Const.playerColor], pg.Rect(128, 56, 8, 8))
