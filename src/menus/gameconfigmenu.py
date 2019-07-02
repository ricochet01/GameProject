import pygame as pg
from pygame.locals import *
import json

from src.game import Game
from src.menus.menu import Menu
from src.constants import stop


class GameConfigMenu(Menu):

	def __init__(self):
		super().__init__()
		self.currentMenu = "Game configuration"
		self.center = self.display.get_width() / 2 - len(self.currentMenu) * 4
		self.newGame = False

		with open("cfg/gameconfig.json", "r") as f:
			self.data = json.load(f)

		self.difficulties = ["Easy", "Medium", "Hard"]
		self.densities = [0.01, 0.02, 0.03, 0.04, 0.05, 0.06, 0.07, 0.08, 0.09, 0.1]
		self.sizes = [[32, 32], [64, 64]]

		self.difficulty = self.data["Difficulty"]
		if self.difficulty not in self.difficulties:
			self.difficulty = "Easy"
			self.data["Difficulty"] = self.difficulty
			with open("cfg/gameconfig.json", "w") as f:
				json.dump(self.data, f, indent=4)


		self.density = self.data["Density"]
		if self.density not in self.densities:
			self.density = 0.05
			self.data["Density"] = self.density
			with open("cfg/gameconfig.json", "w") as f:
				json.dump(self.data, f, indent=4)


		self.size = self.data["Size"]
		if self.size not in self.sizes:
			self.size = [64, 64]
			self.data["Size"] = self.size
			with open("cfg/gameconfig.json", "w") as f:
				json.dump(self.data, f, indent=4)


		self.timer = self.data["Time limit"]
		if self.timer < 0 or self.timer > 255:
			self.timer = 60
			self.data["Time limit"] = self.timer
			with open("cfg/gameconfig.json", "w") as f:
				json.dump(self.data, f, indent=4)

		self.items = [
					"Difficulty: %s" % self.difficulty,
					"Density: " + str(int(self.density*100)) + "%",
					"Size: %dx%d" % (self.size[0], self.size[1]),
					"Time limit: %d s" % self.timer,
					"Play!"]

		self.varSetup()

	def varSetup(self):
		self.difCounter = self.difficulties.index(self.difficulty)
		self.denCounter = self.densities.index(self.density)
		self.sizeCounter = self.sizes.index(self.size)

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

				if event.key == K_RETURN and self.counter == 4:
					with open("cfg/gameconfig.json", "w") as f:
						json.dump(self.data, f, indent=4)
					self.newGame = True
					game = Game()
					game.main()
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

				if event.key in self.input.leftKeys:
					if self.counter == 0:
						self.difCounter -= 1
						if self.difCounter == -1:
							self.difCounter = len(self.difficulties) - 1
						self.difficulty = self.difficulties[self.difCounter]
						self.data["Difficulty"] = self.difficulty
						self.items[0] = "Difficulty: %s" % self.difficulty
						self.scroll.play()

					if self.counter == 1:
						self.denCounter -= 1
						if self.denCounter == -1:
							self.denCounter = len(self.densities) - 1
						self.density = self.densities[self.denCounter]
						self.data["Density"] = self.density
						self.items[1] = "Density: " + str(int(self.density*100)) + "%"
						self.scroll.play()
						
						
					if self.counter == 2:
						self.sizeCounter -= 1
						if self.sizeCounter == -1:
							self.sizeCounter = len(self.sizes) - 1
						self.size = self.sizes[self.sizeCounter]
						self.data["Size"] = self.size
						self.items[2] = "Size: %dx%d" % (self.size[0], self.size[1])
						self.scroll.play()

					if self.counter == 3:
						self.timer = (self.timer - 1) & 0xff
						self.data["Time limit"] = self.timer
						self.items[3] = "Time limit: %d s" % self.timer
						self.scroll.play()

				if event.key in self.input.rightKeys:
					if self.counter == 0:
						self.difCounter += 1
						if self.difCounter == len(self.difficulties):
							self.difCounter = 0
						self.difficulty = self.difficulties[self.difCounter]
						self.data["Difficulty"] = self.difficulty
						self.items[0] = "Difficulty: %s" % self.difficulty
						self.scroll.play()

					if self.counter == 1:
						self.denCounter += 1
						if self.denCounter == len(self.densities):
							self.denCounter = 0
						self.density = self.densities[self.denCounter]
						self.data["Density"] = self.density
						self.items[1] = "Density: " + str(int(self.density*100)) + "%"
						self.scroll.play()
						
					if self.counter == 2:
						self.sizeCounter += 1
						if self.sizeCounter == len(self.sizes):
							self.sizeCounter = 0
						self.size = self.sizes[self.sizeCounter]
						self.data["Size"] = self.size
						self.items[2] = "Size: %dx%d" % (self.size[0], self.size[1])
						self.scroll.play()

					if self.counter == 3:
						self.timer = (self.timer + 1) & 0xff
						self.data["Time limit"] = self.timer
						self.items[3] = "Time limit: %d s" % self.timer
						self.scroll.play()



	def menuUpdate(self):
		self.display.blit(self.font.render(self.currentMenu, None, pg.Color("white")), (self.center, 4))

		y = 32
		for i, key in zip(range(len(self.items)), self.items):
			if i == self.counter:
				self.display.blit(self.font.render(">" + key + "<", None, pg.Color("yellow")),
					(self.display.get_width() / 2 - len(key) * 4 - 8, y))
			else:
				self.display.blit(self.font.render(key, None, pg.Color("gray")),
					(self.display.get_width() / 2 - len(key) * 4, y))
			y += 8
