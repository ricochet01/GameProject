import pygame as pg
from pygame.locals import *

from src.menus.menu import Menu
from src.menus.optionsmenu import OptionsMenu
from src.entities.yesnoprompt import YesNoPrompt
from src.constants import stop

class PauseMenu(Menu):

	def __init__(self):
		super().__init__()
		self.parentVal = None
		self.currentMenu = "Paused"
		self.items = ["Resume", "Options", "Back to menu", "Quit to desktop"]
		self.center = self.display.get_width() / 2 - len(self.currentMenu) * 4

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
						self.running = False

					if self.counter == 1:
						optionsScreen = OptionsMenu()
						optionsScreen.main()
						self.soundSetup()

					if self.counter == 2:
						yesnoScreen = YesNoPrompt()
						yesnoScreen.main()
						if yesnoScreen.state:
							self.parentVal = True
							self.running = False

					if self.counter == 3:
						yesno = YesNoPrompt()
						yesno.main()
						if yesno.state:
							stop()

				if event.key == K_ESCAPE:
					self.running = False
					self.goBack.play()

	def menuUpdate(self):
		self.display.blit(self.font.render(self.currentMenu, None, pg.Color("white")), (self.center, 4))

		self.titleY = self.display.get_height() / 2 - len(self.items) * 4
		for i in range(len(self.items)):
			if i == self.counter:
				self.display.blit(self.font.render("> " + self.items[i] + " <", None, pg.Color("yellow")),
					(self.display.get_width() / 2 - len(self.items[i]*8) / 2 - 16, self.titleY))
			else:
				self.display.blit(self.font.render(self.items[i], None, pg.Color("gray")),
					(self.display.get_width() / 2 - len(self.items[i]*8) / 2, self.titleY))
				
			self.titleY += 8