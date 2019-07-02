import pygame as pg
from pygame.locals import *

from src.menus.menu import Menu
from src.network.server import Server


class MultiplayerTypeMenu(Menu):

	def __init__(self):
		super().__init__()
		self.currentMenu = "Select one"
		self.center = self.display.get_width() / 2 - len(self.currentMenu) * 4
		self.items = ["Host", "Join"]

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

				if event.key == K_RETURN:
					self.select.play()
					if self.counter == 0:
						pass
						# server = Server()
						# server.run()

					if self.counter == 1:
						pass

				if event.key == K_ESCAPE:
					self.running = False
					self.goBack.play()


	def menuUpdate(self):
		self.display.blit(self.font.render(self.currentMenu, None, pg.Color("white")), (self.center, 4))

		y = 32
		for i, key in zip(range(len(self.items)), self.items):
			if i == self.counter:
				self.display.blit(self.font.render("> " + key + " <", None, pg.Color("yellow")),
					(self.display.get_width() / 2 - len(key) * 4 - 16, y))
			else:
				self.display.blit(self.font.render(key, None, pg.Color("gray")),
					(self.display.get_width() / 2 - len(key) * 4, y))
			y += 16