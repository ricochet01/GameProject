import pygame as pg
from pygame.locals import *

from src.menus.menu import Menu
from src.menus.aboutmenu import AboutMenu
from src.menus.howtomenu import HowToPlayMenu
from src.menus.optionsmenu import OptionsMenu
from src.menus.highscoremenu import HighScoresMenu
from src.menus.gametypemenu import GameTypeMenu
from src.constants import Const, stop


class MainMenu(Menu):

	def __init__(self):
		super().__init__()
		self.items = ["Play", "Options", "High Scores", "About", "How to play", "Quit"]
		self.currentMenu = "Main menu"

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
					if self.counter == self.items.index("Play"):
						gameTypeScreen = GameTypeMenu()
						gameTypeScreen.main()
						self.soundSetup()

					if self.counter == self.items.index("Options"):
						optionsScreen = OptionsMenu()
						optionsScreen.main()
						self.soundSetup()

					if self.counter == self.items.index("High Scores"):
						hiScoreScreen = HighScoresMenu()
						hiScoreScreen.main()

					if self.counter == self.items.index("About"):
						aboutScreen = AboutMenu()
						aboutScreen.main()

					if self.counter == self.items.index("How to play"):
						howToPlayScreen = HowToPlayMenu()
						howToPlayScreen.main()

					if self.counter == self.items.index("Quit"):
						stop()

				if event.key == K_ESCAPE and self.currentMenu != "Main menu":
					self.running = False
					self.goBack.play()

	def menuUpdate(self):
		self.display.blit(self.font.render(Const.TITLE[:6], None, pg.Color("green")), (self.display.get_width() / 2 - len(Const.TITLE) * 4, 8))
		self.display.blit(self.font.render(Const.TITLE[6:], None, pg.Color("red")), (self.display.get_width() / 2 - len(Const.TITLE) * 4 + 48, 8))

		self.titleY = self.display.get_height() / 2 - len(self.items) * 4
		for i in range(len(self.items)):
			if i == self.counter:
				self.display.blit(self.font.render("> " + self.items[i] + " <", None, pg.Color("yellow")),
					(self.display.get_width() / 2 - len(self.items[i]*8) / 2 - 16, self.titleY))
			else:
				self.display.blit(self.font.render(self.items[i]), (self.display.get_width() / 2 - len(self.items[i]*8) / 2, self.titleY))
			self.titleY += 8

