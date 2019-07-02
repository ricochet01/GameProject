import pygame as pg

from src.menus.menu import Menu


class ScoreDetails(Menu):

	def __init__(self, data, name):
		super().__init__()
		self.data = data
		self.name = name
		self.currentMenu = "Details"
		self.center = self.display.get_width() / 2 - len(self.currentMenu) * 4

	def menuUpdate(self):
		self.display.blit(self.font.render(self.currentMenu, None, pg.Color("white")), (self.center, 4))

		self.display.blit(self.font.render("Name: " + self.name, None, pg.Color("gray")), (8, 20))
		self.display.blit(self.font.render("Score: " + str(self.data["Score"]), None, pg.Color("gray")), (8, 28))

		self.display.blit(self.font.render("Difficulty: ", None, pg.Color("gray")), (8, 36))
		if self.data["Difficulty"] == "Easy":
			self.display.blit(self.font.render("Easy", None, pg.Color("darkgreen")), (104, 36))
		elif self.data["Difficulty"] == "Medium":
			self.display.blit(self.font.render("Medium", None, pg.Color("gold")), (104, 36))
		elif self.data["Difficulty"] == "Hard":
			self.display.blit(self.font.render("Hard", None, pg.Color("darkred")), (104, 36))

		self.display.blit(self.font.render("Map density: " + str(int(self.data["Density"]*100)) + "%", None, pg.Color("gray")), (8, 44))
		self.display.blit(self.font.render("Map size: %dx%d" % (self.data["Size"][0], self.data["Size"][1]),
			None, pg.Color("gray")), (8, 52))
		self.display.blit(self.font.render("Time limit: " + str(self.data["Time limit"]) + " s", None, pg.Color("gray")), (8, 60))
		self.display.blit(self.font.render("Date: " + self.data["Date"], None, pg.Color("gray")), (8, 68))
		self.display.blit(self.font.render("Time: " + self.data["Time"], None, pg.Color("gray")), (8, 76))

