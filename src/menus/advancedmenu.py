import pygame as pg
from pygame.locals import *

from src.menus.menu import Menu
from src.constants import Const, stop


class AdvancedOptionsMenu(Menu):

	def __init__(self):
		super().__init__()
		self.currentMenu = "Advanced"
		self.center = self.display.get_width() / 2 - len(self.currentMenu) * 4

		self.items = [
					"Filters: ON" if Const.filters else "Filters: OFF",
					"Scanlines: ON" if Const.crtEffect else "Scanlines: OFF",
					"Inversion: %d" % Const.inversion,
					"Red channel: %d" % Const.redChannel,
					"Green channel: %d" % Const.greenChannel,
					"Blue channel: %d" % Const.blueChannel]

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
						self.scroll.play()
						Const.filters = not Const.filters
						self.items[0] = "Filters: ON" if Const.filters else "Filters: OFF"
						Const.replaceConfig(8, "{:04x}".format(Const.filters))

					elif self.counter == 1 and Const.filters:
						self.scroll.play()
						Const.crtEffect = not Const.crtEffect
						self.items[1] = "Scanlines: ON" if Const.crtEffect else "Scanlines: OFF"
						Const.replaceConfig(5, "{:04x}".format(Const.crtEffect))

					elif self.counter == 2 and Const.filters:
						self.scroll.play()
						Const.inversion = (Const.inversion - 1) & 0xff
						self.items[2] = "Inversion: %d" % Const.inversion
						Const.replaceConfig(4, "{:04x}".format(Const.inversion))

					elif self.counter == 3 and Const.filters:
						self.scroll.play()
						Const.redChannel = (Const.redChannel - 1) & 0xff
						self.items[3] = "Red channel: %d" % Const.redChannel
						Const.replaceConfig(6, "{:04x}".format(Const.redChannel))

					elif self.counter == 4 and Const.filters:
						self.scroll.play()
						Const.greenChannel = (Const.greenChannel - 1) & 0xff
						self.items[4] = "Green channel: %d" % Const.greenChannel
						Const.replaceConfig(9, "{:04x}".format(Const.greenChannel))

					elif self.counter == 5 and Const.filters:
						self.scroll.play()
						Const.blueChannel = (Const.blueChannel - 1) & 0xff
						self.items[5] = "Blue channel: %d" % Const.blueChannel
						Const.replaceConfig(7, "{:04x}".format(Const.blueChannel))


				if event.key in self.input.rightKeys:
					if self.counter == 0:
						self.scroll.play()
						Const.filters = not Const.filters
						self.items[0] = "Filters: ON" if Const.filters else "Filters: OFF"
						Const.replaceConfig(8, "{:04x}".format(Const.filters))

					elif self.counter == 1 and Const.filters:
						self.scroll.play()
						Const.crtEffect = not Const.crtEffect
						self.items[1] = "Scanlines: ON" if Const.crtEffect else "Scanlines: OFF"
						Const.replaceConfig(5, "{:04x}".format(Const.crtEffect))

					elif self.counter == 2 and Const.filters:
						self.scroll.play()
						Const.inversion = (Const.inversion + 1) & 0xff
						self.items[2] = "Inversion: %d" % Const.inversion
						Const.replaceConfig(4, "{:04x}".format(Const.inversion))

					elif self.counter == 3 and Const.filters:
						self.scroll.play()
						Const.redChannel = (Const.redChannel + 1) & 0xff
						self.items[3] = "Red channel: %d" % Const.redChannel
						Const.replaceConfig(6, "{:04x}".format(Const.redChannel))

					elif self.counter == 4 and Const.filters:
						self.scroll.play()
						Const.greenChannel = (Const.greenChannel + 1) & 0xff
						self.items[4] = "Green channel: %d" % Const.greenChannel
						Const.replaceConfig(9, "{:04x}".format(Const.greenChannel))

					elif self.counter == 5 and Const.filters:
						self.scroll.play()
						Const.blueChannel = (Const.blueChannel + 1) & 0xff
						self.items[5] = "Blue channel: %d" % Const.blueChannel
						Const.replaceConfig(7, "{:04x}".format(Const.blueChannel))

				if event.key == K_ESCAPE:
					self.running = False
					self.goBack.play()

	def menuUpdate(self):
		self.display.blit(self.font.render(self.currentMenu), (self.center, 4))

		y = 32
		for i in range(len(self.items)):
			if i == self.counter:
				self.display.blit(self.font.render("> " + self.items[i] + " <", None, pg.Color("yellow")),
					(self.display.get_width() / 2 - len(self.items[i]*8) / 2 - 16, y))
			else:
				self.display.blit(self.font.render(self.items[i], None, pg.Color("gray")), (self.display.get_width() / 2 - len(self.items[i]*8) / 2, y))
			y += 8

		self.display.blit(self.font.render("Be careful :)", None, pg.Color("dimgray")), (28, 88))