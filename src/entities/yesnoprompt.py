import pygame as pg
from pygame.locals import *

from src.menus.menu import Menu
from src.constants import stop


class YesNoPrompt(Menu):

	def __init__(self):
		super().__init__()
		self.currentMenu = "Are you sure?"
		self.center = self.display.get_width() / 2 - len(self.currentMenu) * 4
		self.state = None

		self.items = ["Yes", "No"]

	def eventHandler(self):
		for event in pg.event.get():
			if event.type == QUIT:
				stop()

			if event.type == KEYDOWN:
				if event.key == K_F12:
					self.takeScreenshot()					

				if event.key in self.input.leftKeys and self.currentMenu in self.interactiveMenus:
					self.counter -= 1
					if self.counter == -1:
						self.counter = len(self.items) - 1
					self.scroll.play()

				if event.key in self.input.rightKeys and self.currentMenu in self.interactiveMenus:
					self.counter += 1
					if self.counter == len(self.items):
						self.counter = 0
					self.scroll.play()

				if event.key == K_RETURN:
					self.select.play()
					if self.counter == 0:
						self.state = True
					if self.counter == 1:
						self.state = False

				if event.key == K_ESCAPE:
					self.running = False
					self.goBack.play()

	def menuUpdate(self):
		self.display.blit(self.font.render(self.currentMenu, pg.Color("black"), pg.Color("white")), (self.center, 4))

		if self.state != None:
			self.running = False

		x = 32
		for i in range(len(self.items)):
			if i == self.counter:
				self.display.blit(self.font.render("> " + self.items[i] + " <", None, pg.Color("yellow")),
					(x, 64))
			else:
				self.display.blit(self.font.render(self.items[i], None, pg.Color("gray")), (x+8, 64))
			x += 64