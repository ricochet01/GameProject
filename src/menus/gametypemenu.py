import pygame as pg
from pygame.locals import *

from src.menus.menu import Menu
from src.constants import stop
from src.menus.gameconfigmenu import GameConfigMenu
from src.menus.mptypemenu import MultiplayerTypeMenu


class GameTypeMenu(Menu):

	def __init__(self):
		super().__init__()
		self.currentMenu = "Game type"
		self.center = self.display.get_width() / 2 - len(self.currentMenu) * 4
		self.items = ["Singleplayer", "Local", "Online"]

	def eventHandler(self):
		for event in pg.event.get():
			if event.type == QUIT:
				stop()

			if event.type == KEYDOWN:
				if event.key == K_F12:
					self.takeScreenshot()
					
				if event.key == K_ESCAPE:
					self.goBack.play()
					self.running = False

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

				if event.key == K_RETURN:
					self.select.play()
					if self.counter == 0:
						gameConfigScreen = GameConfigMenu()
						gameConfigScreen.main()
						if gameConfigScreen.newGame:
							self.running = False

					if self.counter == 1:
						mpTypeScreen = MultiplayerTypeMenu()
						mpTypeScreen.main()


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

