import pygame as pg
from pygame.locals import *

import json

from src.menus.menu import Menu
from src.entities.yesnoprompt import YesNoPrompt
from src.menus.scoredetails import ScoreDetails
from src.constants import stop

		
class HighScoresMenu(Menu):

	def __init__(self):
		super().__init__()
		self.currentMenu = "High scores"
		self.center = self.display.get_width() / 2 - len(self.currentMenu) * 4
		self.change = 0

		with open("cfg/data.json", "r") as f:
			data = json.load(f)
			tempArray = []
			for d in data:
				tempArray.append(d)
				
		self.items = sorted(tempArray, key=lambda k: k["Score"], reverse=True)

		self.allNames = []
		for i in range(len(self.items)):
			self.allNames.append(self.items[i]["Name"])

	def eventHandler(self):
		for event in pg.event.get():
			if event.type == QUIT:
				stop()

			if event.type == KEYDOWN:
				if event.key == K_F12:
					self.takeScreenshot()

				if event.key in self.input.upKeys and self.currentMenu in self.interactiveMenus and len(self.items) > 1:
					self.counter -= 1
					if self.counter == -1:
						self.counter = len(self.items) - 1
					self.scroll.play()

				if event.key in self.input.downKeys and self.currentMenu in self.interactiveMenus and len(self.items) > 1:
					self.counter += 1
					if self.counter == len(self.items):
						self.counter = 0
					self.scroll.play()

				if event.key == K_RETURN:
					self.select.play()
					scoreDetailsScreen = ScoreDetails(self.items[self.counter], self.allNames[self.counter])
					scoreDetailsScreen.main()

				if event.key == K_ESCAPE and self.currentMenu != "Main menu":
					self.running = False
					self.goBack.play()

				if event.key == K_x and len(self.allNames) != 0:
					self.select.play()
					yesNoScreen = YesNoPrompt()
					yesNoScreen.main()
					if yesNoScreen.state:
						del self.items[self.counter]
						del self.allNames[self.counter]

						with open("cfg/data.json", "w") as f:
							json.dump(self.items, f, indent=4)

			
	def menuUpdate(self): # Jesus fucking christ this took forever to make...
		self.display.blit(self.font.render(self.currentMenu, None, pg.Color("white")), (self.center, 4))
		self.display.blit(self.font.render("Press X to delete", None, pg.Color("darkred")), (12, 16))

		if self.counter >= len(self.allNames):
			self.counter = len(self.allNames) - 1

		if self.counter <= 4 or len(self.allNames) <= 9:
			self.change = 0
			self.slice = self.allNames[:9]
		elif self.counter >= 5 and self.counter <= len(self.allNames) - 5:
			self.change = self.counter - 4
			self.slice = self.allNames[self.change:self.change+9]
		else:
			self.change = len(self.allNames) - 9
			self.slice = self.allNames[len(self.allNames)-9:]

		y = 32
		for i, key in zip(range(self.change + 1, len(self.allNames) + 1), self.slice):
			if self.counter == i - 1:
				self.display.blit(self.font.render(">" + str(i) + "." + self.allNames[i-1] + ":" + str(self.items[i-1]["Score"]) + "<",
					None, pg.Color("yellow")), (0, y))
			else:
				self.display.blit(self.font.render(str(i) + "." + self.allNames[i-1] + ":" + str(self.items[i-1]["Score"]),
					None, pg.Color("gray")), (8, y))
			y += 8
